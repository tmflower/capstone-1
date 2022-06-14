from flask import Flask, render_template, redirect, flash, session, request, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from psycopg2 import IntegrityError
from models import db, connect_db, User, Word, Users_Words
from secret import KEY
from forms import NewUserForm, UserLoginForm, WordForm
from sqlalchemy.exc import IntegrityError
import requests, json

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///wordgame'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'mochi'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

BASE_URL = "https://wordsapiv1.p.rapidapi.com/words/"

HEADERS = {
	"X-RapidAPI-Host": "wordsapiv1.p.rapidapi.com",
	"X-RapidAPI-Key": KEY
}


@app.route('/')
def home_page():
    """Displays landing page with option to log in or play without logging in."""
    return render_template('home.html')


@app.route('/signup', methods=["GET", "POST"])
def user_signup():
    """Allows a new user to sign up for a free account when a unique username and valid password is submitted."""
    form = NewUserForm()
    if form.validate_on_submit():
        try:
            username = form.username.data
            password = form.password.data

            user = User.signup(username, password)
            db.session.add(user)
            db.session.commit()

            session["user_id"] = user.id

            flash(f"You have created an account, {username}!", "success")
            return redirect('/game/info')

        except IntegrityError:
            flash("Sorry, that username is already taken. Please try another one.", "warning")
            form.username.data = ""
            form.password.data = ""
        
    return render_template('signup.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def user_login():
    """Allows user who has already signed up to log in with valid username and password"""
    form = UserLoginForm()

    if form.validate_on_submit():        
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        
        if user:
            session["user_id"] = user.id
            flash(f"You are logged in, {username}!", "success")
            return redirect('/game/info')

        else:
            flash("Username or password not valid. Please try again.", "danger")
            form.username.data = ""
            form.password.data = ""

    return render_template('login.html', form=form)


@app.route('/logout')
def user_logout():
    """Allows user to log out."""
    flash("You've signed out!", "warning")
    session.pop("user_id")    
    return redirect('/')


@app.route('/game/info')
def game_info():
    """Displays instructions/rules for game and start button."""
    return render_template('game-info.html')


@app.route('/game/play')
def game_play():
    """Initiates game by getting a random word from Words API with the given parameters"""

    querystring = {"lettersmin":"6","lettersMax":"10","syllablesMin":"2","syllablesMax":"5","frequencymin":"2.00","frequencymax":"5.00","hasDetails":"definitions", "hasDetails":"synonyms", "random":"true"}
    
    response = requests.request("GET", BASE_URL, headers=HEADERS, params=querystring)
    data = response.json()
    print(data)

    if " " in data['word'] or "-" in data['word']:
        return redirect('/game/play')
    try:
        mystery_word = Word(
        word = data['word'], 
        pos = data['results'][0]['partOfSpeech'], 
        syllable_count = data['syllables']['count'], 
        definition = data['results'][0]['definition'],
        synonyms = data['results'][0]['synonyms']
        )

        db.session.add(mystery_word)
        db.session.commit()

        synonyms = data['results'][0]['synonyms']
        session['word'] = mystery_word.word
        session['word_id'] = mystery_word.id
        # score = session['score']
    
    except IntegrityError:
        return redirect('/game/play')
        
    return render_template('/game-play.html', word=mystery_word, synonyms=synonyms)


@app.route('/game/check-guess', methods=["GET","POST"])
def check_guess():
    """Checks if user has guessed the word and provide feedback accordingly"""
    guess = request.args['guess']
    return jsonify(guess)


@app.route('/game/get-score', methods=["POST"])
def get_score():
    """Get final score when game ends"""    
    output = request.get_json()
    result = json.loads(output)
    score = result['score']
    session['score'] = score
    return result


@app.route('/game/finish')
def show_stats():
    """Displays feedback and game stats when user guesses word correctly or time runs out."""
    word = session['word']
    score = session['score']   

    if "user_id" in session:
        user_id = session['user_id']
        user = User.query.get(user_id)
        word_id = session['word_id']
        users_words = Users_Words(user=user_id, word=word_id)
        print(f"users_words looks like this: ************************************{users_words}")
        
        db.session.add(users_words)
        db.session.commit()
        
    else:
        user = "anonymous"
    update_points()
    update_rankings()
    leaders = User.query.order_by(User.total_points.desc()).limit(5)
    
    return render_template('game-finish.html', score=score, word=word, leaders=leaders, user=user)


def update_points():
    """Adds current round score to logged-in user's running points total"""
    if "user_id" in session:
        id = session['user_id']
        u = User.query.get(id)
        u.total_points = u.total_points + session['score']
        db.session.commit()
    else:
        return redirect('/game/finish')


def update_rankings():
    """Ranks players in descending order according to greatest cumulative points earned."""
    rankings = User.query.order_by(User.total_points.desc()).all()
    for user in rankings:
        user.rank = rankings.index(user)+1
        db.session.commit()
    

@app.route('/word-info/<word>')
def show_word_info(word):
    """Provides details about the user's selected word"""
    word = Word.query.filter_by(word=word).first()
    syns = word.synonyms
    syns2 = syns.replace('{', '')
    syns3 = syns2.replace('}', '')
    synonyms = syns3.split(',') 
    return render_template('word-info.html', word=word, synonyms=synonyms)


@app.route('/word-lookup', methods=["GET", "POST"])
def lookup_word():
    """Allows user to type in a word and get definition and get information about the word"""
            
    form = WordForm()
    word = form.word.data

    existing_word = Word.query.filter(Word.word==word).first()
    if existing_word:
        word = existing_word
        return redirect (f'/word-info/{word.word}')

    if request.method == "POST":

        response = requests.request("GET", f"https://wordsapiv1.p.rapidapi.com/words/{word}", headers=HEADERS)
        data = response.json()

        try:
            word = Word(
                word=data['word'], 
                definition=data['results'][0]['definition'], 
                pos=data['results'][0]['partOfSpeech'], 
                synonyms=data['results'][0]['synonyms']
                )

            db.session.add(word)
            db.session.commit()

            if "user_id" in session:
                user_id = session['user_id']
                users_words = Users_Words(user=user_id, word=word.id)
        
                db.session.add(users_words)
                db.session.commit()
            
            return redirect (f'/word-info/{word.word}')

        except KeyError:
            flash("Sorry, we don't have all the information for this word. Please try another word.", "warning")
            
    return render_template('word-form.html', form=form, word=word)


@app.route('/word-info/<word>/delete', methods=["POST"])
def delete_word(word):
    """Allows logged-in user to delete selected word from their words list"""
    word = Word.query.filter_by(word=word).first()
    
    if "user_id" in session:        
        db.session.delete(word)
        db.session.commit()
        flash("You have deleted a word from your list.", "warning")
        return redirect('/game/play')
        
    else:
        flash("You are not authorized to access this page.", "danger")
        return redirect('/')


@app.route('/user-words')
def show_user_words():
    """Displays list of words from user's games and allows user to view more info or delete words"""
    
    user_words_list = []
    
    if "user_id" not in session:
        flash("Sorry, you must have an account to see your words.", "danger")
        return redirect('/')

    else:
        user_id = session['user_id']
        users_words = Users_Words.query.filter_by(user=user_id).all() 
        for word in users_words:
            user_word = Word.query.get(word.word)
            user_words_list.append(user_word)

        return render_template('user-words.html', list=user_words_list)