from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class Word(db.Model):

    __tablename__ = "words"

    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.Text, unique=True, nullable=False)
    syllable_count = db.Column(db.Integer, default=0)
    pos = db.Column(db.Text, default='Part of speech not available')
    definition = db.Column(db.Text, default='Definition not available')
    synonyms = db.Column(db.Text, default='Synonyms not available')
    antonyms = db.Column(db.Text, default='Antonyms not available')

class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    points = db.Column(db.Integer, default=0)

    @classmethod
    def signup(cls, username, password):
        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode("utf8")
        return cls(username=username, password=hashed_utf8)

    @classmethod 
    def authenticate(cls, username, password):
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False

class Users_Words(db.Model):

    __tablename__ = "users_words"

    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.ForeignKey('users.id'))
    word = db.Column(db.ForeignKey('words.id'))