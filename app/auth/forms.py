from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import InputRequired, Length, Email, EqualTo
from wtforms import ValidationError
from .. models import User


class LoginForm(FlaskForm):
    email = StringField('Email',validators=[InputRequired(message='请输入邮箱'),Email(message='请输入正确邮箱')])
    password = PasswordField('密码',validators=[InputRequired(message='请输入密码'),Length(min=8,max=32,message='请输入正确长度的密码')])
    remember_me = BooleanField()
    submit = SubmitField('登录')


class RegistrationForm(FlaskForm):
    email = StringField('Email',validators=[InputRequired(message='请输入邮箱'),Email(message='请输入正确邮箱')])
    username = StringField('用户名',validators=[InputRequired(message='请输入用户名'),Length(min=1,max=20,message='请输入正确长度的用户名')])
    password = PasswordField('密码',validators=[InputRequired(message='请输入密码'),Length(min=8,max=32,message='请输入正确长度的密码')])
    confirm = PasswordField('确认密码',validators=[InputRequired(message='请再此输入密码'),EqualTo('password',message='请与密码相同')])
    submit = SubmitField('注册')

class TryForm(FlaskForm):
    email = StringField('Email',validators=[Email(),InputRequired(message='try input'),Length(min=1,max=7,message='try Length')])
    submit = SubmitField('setup')
