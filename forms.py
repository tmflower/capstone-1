from re import S
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired, Length

class NewUserForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=5, max=15)])
    password = StringField("Password", validators=[InputRequired(), Length(min=5, max=15)])

class UserLoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=5, max=15)])
    password = StringField("Password", validators=[InputRequired(), Length(min=5, max=15)])