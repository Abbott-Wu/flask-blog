from datetime import datetime
from flask import render_template, session, redirect, url_for, flash, current_app, request, abort
from flask_login import current_user, login_required
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


@main.route('/write', methods=['GET', 'POST'])
@admin_required
def write():
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
    return render_template('write.html.j2', form=form)


ALLOWED_EXTENSIONS = set(['txt', 'md'])


@main.route('/upload', methods=['GET', 'POST'])
@admin_required
def upload():
    form = UploadForm()
    if request.method == 'POST':
        file = request.files['markdown_file']
        md = ''
        if file and allowed_file(file.filename):
            md = file.read()
        post = Post(title=form.main_title.data,
                    body=bytes.decode(md),
                    second_title=form.second_title.data,
                    img=form.img.data,
                    first_look=form.first_look.data,
                    author=current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        flash('文章已经提交')
        return redirect(url_for('main.index'))
    form.main_title.data='title'
    return render_template('upload.html.j2', form=form)


@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit(id):
    post = Post.query.get_or_404(id)
    form = PostForm()
    if current_user.can(Permission.ADMINISTER) and \
            current_user != post.author:
        abort(403)
    if form.validate_on_submit():
        post.title = form.main_title.data
        post.second_title = form.second_title.data
        post.first_look = form.first_look.data
        post.img = form.img.data
        post.body = form.body.data
        db.session.add(post)
        db.session.commit()
        flash('文章已经提交')
        return redirect(url_for('main.post', id=post.id))
    form.main_title.data = post.title
    form.second_title.data = post.second_title
    form.first_look.data = post.first_look
    form.img.data = post.img
    form.body.data = post.body
    return render_template('write.html.j2', form=form, need=None)

#
@main.route('/post/<int:id>')
def post(id):
    post = Post.query.get_or_404(id)
    return render_template('post.html.j2', post=post)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
