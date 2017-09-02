from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from .. models import User


class LoginForm(FlaskForm):
    email = StringField('Email')
    password = PasswordField('密码')
    remember_me = BooleanField()
    submit = SubmitField('登录')


class RegistrationForm(FlaskForm):
    email = StringField('Email')
    username = StringField('Username')
    password = PasswordField('password')
    password2 = PasswordField('confirm password')
    submit = SubmitField('Register')
