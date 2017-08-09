from flask import render_template, redirect, request, url_for, flash, session
from flask_login import current_user, login_user, login_required, logout_user
from . import auth
from ..models import User
from .forms import LoginForm, RegistrationForm
from .. import db
from ..email import send_email


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('密码或用户名错误')
    return render_template('auth/login.html.j2', current_user=current_user, form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('你已经退出')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if form.password.data != form.password2.data:
            flash('密码不相等，请重新输入')
            return redirect(url_for('auth.register'))
        elif User.query.filter_by(email=form.email.data).first():
            flash('邮箱已注册，请重新输入')
            return redirect(url_for('auth.register'))
        elif User.query.filter_by(username=form.username.data).first():
            flash('用户名已注册，请重新输入')
            return redirect(url_for('auth.register'))
        else:
            user = User(email=form.email.data,
                        username=form.username.data,
                        password=form.password.data)
            db.session.add(user)
            db.session.commit()
            token = user.generate_confirmation_token()
            send_email(user.email, '确认你的账户', 'auth/email/confirm',
                       user=user, token=token)
            flash('你现在可以登录了，有一封邮件已经邮寄到你的邮箱了')
            return redirect(url_for('auth.login'))
    return render_template('auth/register.html.j2', form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('你已经确认你的账户')
    else:
        flash('确认失败')
    return redirect(url_for('main.index'))


@auth.before_app_request
def before_request():
    if current_user.is_authenticated \
            and not current_user.confirmed \
            and request.endpoint[:5] != 'auth.' \
            and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html.j2')

# -----------------------------------------------------------------------------


def send_token_email(title, flash_massage, template, current_user=current_user):
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, title,
               template, user=current_user, token=token)
    flash(flash_massage)


@auth.route('/confirm')
@login_required
def resend_confirmation():
    send_token_email('确认你的账户', '一份新的邮件已经被送到你的邮箱里了', 'auth/email/confirm')
    return redirect(url_for('main.index'))


@auth.route('/manage')
@login_required
def manage_auth():
    return render_template('auth/manage.html.j2')
