from flask import (
    Blueprint, current_app, session,
    redirect, url_for, abort,
    render_template, flash
)
from flask_adminlte_full.forms import LoginForm, ResetPasswordForm
from flask_login import login_user, logout_user, current_user, login_required
from itsdangerous import URLSafeTimedSerializer, SignatureExpired

from ..extensions import adminlte
from ..forms import RegistrationForm, ChangePasswordForm, RecoverPasswordForm
from ..models import db, User


bp = Blueprint('auth', __name__)


@bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()

    if form.validate_on_submit():
        current_user.password = form.password.data
        db.session.commit()
        adminlte.flash.success('Пароль был успешно изменен.')
        return redirect(url_for(current_app.config['ADMINLTE_CHANGE_PASSWORD_ENDPOINT']))

    return render_template('adminlte_full/change_password.html', form=form)


@bp.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    form = ResetPasswordForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first_or_404()

        ts = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        token = ts.dumps(form.email.data, 'registration-continue-token')

        return redirect(url_for(current_app.config['ADMINLTE_PASSWORD_RECOVER_ENDPOINT'], token=token))

    return render_template('adminlte_full/forgot_password.html', form=form)


@bp.route('/recover-password/<token>', methods=['GET', 'POST'])
def recover_password(token):
    try:
        ts = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        email = ts.loads(token, salt='registration-continue-token', max_age=86400)
    except SignatureExpired:
        adminlte.flash.error(
            'The password reset link was invalid, possibly because it has already been used.'
            'Please request a new password reset.'
        )
        return redirect(url_for(current_app.config['ADMINLTE_PASSWORD_RESET_ENDPOINT']))

    user = User.query.filter_by(email=email).first_or_404()
    form = RecoverPasswordForm()

    if form.validate_on_submit():
        user.password = form.password.data
        db.session.commit()
        adminlte.flash.success('Пароль был успешно изменен.')
        return redirect(url_for(current_app.config['ADMINLTE_LOGIN_ENDPOINT']))

    return render_template('adminlte_full/recover_password.html', form=form, validlink=True)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Аутентификация аккаунта."""
    if current_user.is_authenticated:
        return redirect(url_for('site.index'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and user.is_active and user.check_password(form.password.data):
            remember = current_app.config['ADMINLTE_REMEMBER_ME'] and form.remember_me.data
            login_user(user, remember=remember)
            return redirect(adminlte.manager.get_home_page().url)

        adminlte.flash.error('Invalid account')

    return render_template('adminlte_full/login.html', form=form)


@bp.route('/logout')
@login_required
def logout():
    """Выход пользователя."""
    logout_user()
    return redirect(url_for(current_app.config['ADMINLTE_LOGIN_ENDPOINT']))


@bp.route('/registration', methods=['GET', 'POST'])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('site.index'))

    form = RegistrationForm()

    if form.validate_on_submit():
        email = form.email.data

        user = User.query.filter_by(email=email).first()

        if user is None:
            user = User(
                email=email,
                password=form.password.data,
                firstname=form.firstname.data,
                lastname=form.lastname.data,
                active=True
            )
            db.session.add(user)
            db.session.commit()

            # adminlte.flash.success('На ваш E-Mail было отправлено письмо для завершения регистрации.')
            adminlte.flash.success('Вы успешно зарегистрировались.')
            return redirect(url_for(current_app.config['ADMINLTE_LOGIN_ENDPOINT']))
        else:
            adminlte.flash.error('Пользователь с таким E-Mail существует.')

        # form.populate_obj(person)

    return render_template('adminlte_full/register.html', form=form)


# @bp.route('/activation/<token>', methods=['GET', 'POST'])
# @access.public_required
# def activation(token):
#     """Завершение регистрации аккаунта и автоматическое подтверждение, шаг 2."""
#     if current_user.is_authenticated:
#         return redirect(url_for(index_endpoint(current_user)))
#
#     try:
#         email = ts.loads(token, salt='registration-continue-token', max_age=86400)
#     except SignatureExpired:
#         flash('Ваш токен устарел, необходимо повторно выполнить регистрацию.', 'error')
#         return redirect(url_for('auth.registration'))
#
#     account = Account.get(email=email) or abort(404)
#
#     if account.confirmed:
#         flash('Вы уже зарегистрированы, можете выполнить вход.')
#         return redirect(url_for('auth.login'))
#
#     form = RegistrationActivationForm()
#
#     if form.validate_on_submit():
#         account.set(password=form.password.data,
#                     active=True,
#                     confirmed=True,
#                     gitlab_id=form.gitlab_id)
#         flash('Регистрация успешно завершена, вы можете выполнить вход.')
#         return redirect(url_for('auth.login'))
#
#     return render_template('auth/registration_step_2.html', form=form)
