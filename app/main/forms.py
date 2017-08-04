from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required


class TryFrom(FlaskForm):
    name = StringField('please input your name', validators=[
                       Required(message=u'邮箱不能为空')])
    submit = SubmitField(label='submit')
