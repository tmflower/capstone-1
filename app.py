from flask import Flask, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from psycopg2 import IntegrityError
from models import db, connect_db, User
from secret import KEY
from forms import NewUserForm, UserLoginForm
from sqlalchemy.exc import IntegrityError

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
    """Allows a new user to sign up for a free account."""
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
            return redirect('/game')

        except IntegrityError:
            flash("Sorry, that username is already taken. Please try another one.", "warning")
        
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
            return redirect('/game')

        else:
            flash("Username or password not valid. Please try again.", "danger")

    return render_template('login.html', form=form)

@app.route('/logout')
def user_logout():
    """Allows user to log out."""
    session.pop("user_id")
    return redirect('/')


@app.route('/game')
def game_overview():
    """Displays instructions/rules for game and start button."""
    return render_template('game.html')