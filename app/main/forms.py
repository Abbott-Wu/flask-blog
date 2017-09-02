from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import Required


class TryFrom(FlaskForm):
    name = StringField('please input your name', validators=[
                       Required(message=u'邮箱不能为空')])
    submit = SubmitField(label='submit')


class PostForm(FlaskForm):
    main_title = StringField('标题')
    second_title = StringField('副标题(可选)')
    img = StringField('图像链接(可选)')
    first_look = TextAreaField('文章预览')
    body = TextAreaField('文章内容')
    submit = SubmitField('提交')
