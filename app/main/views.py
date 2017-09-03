from datetime import datetime
from flask import render_template, session, redirect, url_for, flash, current_app, request
from flask_login import current_user
from flask_sqlalchemy import Pagination

from . import main
from .forms import TryFrom, PostForm, UploadForm
from .. import db
from ..models import User, Permission, Post
from ..decorators import admin_required


@main.route('/')
def index():
    page = request.args.get('Page')
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    return render_template('home.html.j2', posts=posts,
                           current_time=datetime.utcnow(),
                           pagination=pagination)


@main.route('/edit', methods=['GET', 'POST'])
@admin_required
def edit():
    form = PostForm()
    if current_user.can(Permission.WRITE_ARTICLES) and \
            form.validate_on_submit():
        post = Post(body=form.body.data,
                    title=form.main_title.data,
                    second_title=form.second_title.data,
                    img=form.img.data,
                    first_look=form.first_look.data,
                    author=current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        flash('文章已经提交')
        return redirect(url_for('main.index'))
    return render_template('edit.html.j2', form=form)


@main.route('/post/<int:id>')
def post(id):
    post = Post.query.get_or_404(id)
    return render_template('post.html.j2', post=post)


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

ALLOWED_EXTENSIONS = set(['txt','md'])

@main.route('/upload', methods=['GET', 'POST'])
def upload():
    form = UploadForm()
    if request.method=='POST':
        file = request.files['markdown_file']
        md=''
        if file and allowed_file(file.filename):
            with open(file, 'r') as f:
                md=f.read()
        post = Post(body=md,
                    title=form.main_title.data,
                    second_title=form.second_title.data,
                    img=form.img.data,
                    first_look=form.first_look.data,
                    author=current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        flash('文章已经提交')
        return redirect(url_for('main.index'))
    return render_template('upload.html.j2',form=form)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
