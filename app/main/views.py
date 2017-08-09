from datetime import datetime
from flask import render_template, session, redirect, url_for
from flask_login import current_user

from . import main
from .forms import TryFrom
from .. import db
from ..models import User


@main.route('/')
def index():
    return render_template('home.html.j2')


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
