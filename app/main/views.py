from datetime import datetime
from flask import render_template, session, redirect, url_for, flash
from flask_login import current_user

from . import main
from .forms import TryFrom,PostForm
from .. import db
from ..models import User,Permission,Post
from ..decorators import admin_required


@main.route('/')
def index():
    return render_template('home.html.j2')

@main.route('/edit', methods=['GET','POST'])
@admin_required
def edit():
    form = PostForm()
    if current_user.can(Permission.WRITE_ARTICLES) and \
            form.validate_on_submit():
        post=Post(body=form.body.data,
                    author=current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        flash('文章已经提交')
        return render_template('home.html.j2')
    return render_template('edit.html.j2',form=form)

@main.route('/try', methods=['GET', 'POST'])
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
            if current_app.config['FLASKY_ADMIN']:
                send_email(current_app.config['FLASKY_ADMIN'],
                           'New User', 'mail/new_user', user=user)
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('main.TryWTF'))
    return render_template('flask-wtfTry.html.j2',
                           form=form, name=session.get('name'),
                           known=session.get('known', False),
                           current_time=datetime.utcnow())
