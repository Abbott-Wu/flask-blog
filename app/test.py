from flask import Flask, render_template, session, redirect, flash, url_for
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from flask_mail import Mail, Message
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from threading import Thread
import os

# 初始化部分
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = '8cd9fa38-6467-426e-a685-7c9f1f937864'
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# 邮件
app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[flasky]'
app.config['FLASKY_MAIL_SENDER'] = 'Flasky Admin <wu13231423396@outlook.com>'
app.config['MAIL_SERVER'] = 'smtp-mail.outlook.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['FLASKY_ADMIN'] = os.environ.get('FLASKY_ADMIN')
# 定义/声明分界线
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
manager = Manager(app)
migrate = Migrate(app, db)
mail = Mail(app)
# 初始化部分

# 命令行部分


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)
# 命令行部分

# 邮件部分


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template, **kwargs):
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,
                  sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html.j2', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr
# 邮件部分
# 数据库部分


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    def __repr__(self):
        return '<Role %r>' % self.name
    users = db.relationship('User', backref='role', lazy='dynamic')


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)

    def __repr__(self):
        return '<User %r>' % self.username
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
# 数据库部分

# 表单部分


class TryFrom(FlaskForm):
    name = StringField('please input your name', validators=[
                       Required(message=u'邮箱不能为空')])
    submit = SubmitField(label='submit')
# 表单部分

# 路由部分


@app.route('/')
def index():
    return render_template('home.html.j2')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404page.html.j2'), 404


@app.route('/try', methods=['GET', 'POST'])
def TryWTF():
    form = TryFrom()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user:
            session['known'] = True
        else:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
            if app.config['FLASKY_ADMIN']:
                send_email(app.config['FLASKY_ADMIN'],
                           'New User', 'mail/new_user', user=user)
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('TryWTF'))
    return render_template('flask-wtfTry.html.j2', form=form, name=session.get('name'), known=session.get('known', False))
# 路由部分


if __name__ == '__main__':
    manager.run()
