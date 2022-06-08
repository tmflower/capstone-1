from flask import Flask, render_template, redirect, flash, session, request, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from psycopg2 import IntegrityError
from models import db, connect_db, User, Word
from secret import KEY
from forms import NewUserForm, UserLoginForm
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

# db.drop_all()
# db.create_all()

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

    return render_template('login.html', form=form)


@app.route('/logout')
def user_logout():
    """Allows user to log out."""
    session.pop("user_id")
    return redirect('/')


@app.route('/game/info')
def game_overview():
    """Displays instructions/rules for game and start button."""
    return render_template('game-info.html')


@app.route('/game/play')
def game_play():
    """Initiates game by getting a random word from Words API with the given parameters"""

    querystring = {"lettersmin":"6","lettersMax":"10","syllablesMin":"2","syllablesMax":"6","frequencymin":"2.00","frequencymax":"5.00","hasDetails":"definitions", "hasDetails":"synonyms", "random":"true"}
    
    response = requests.request("GET", BASE_URL, headers=HEADERS, params=querystring)
    data = response.json()
    print(data)

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
    score = session['score']

    return render_template('/game-play.html', word=mystery_word, synonyms=synonyms, score=score)


@app.route('/game/check-guess', methods=["GET","POST"])
def check_guess():
    """Checks if user has guessed the word and provide feedback accordingly"""
    guess = request.args['guess']
    return jsonify(guess)


@app.route('/game/get-score', methods=["POST"])
def get_score():
    """Get final score when game ends"""    
    output = request.get_json()
    print(f"**************************************{output}")
    result = json.loads(output)
    print(f"#######################################{result}")
    score = result['score']
    session['score'] = score
    print(f"@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@{score}")
    print(f"Session score is ${session['score']}%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
    return result


@app.route('/game/finish')
def show_stats():
    """Displays feedback and game stats when user guesses word correctly or time runs out."""
    word = session['word']
    print(f"WORD is {word}******************************************")
    score = session['score']
    print(f"SCORE is {score}********************************")
    return render_template('game-finish.html', score=score, word=word)