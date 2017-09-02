from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import Required


class TryFrom(FlaskForm):
    name = StringField('please input your name', validators=[
                       Required(message=u'邮箱不能为空')])
    submit = SubmitField(label='submit')

class PostForm(FlaskForm):
    body = TextAreaField('输入内容')
    submit=SubmitField('提交')
