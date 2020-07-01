from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms.fields import (
    StringField, PasswordField, BooleanField, HiddenField, FloatField,
    FieldList, FormField, TextAreaField, RadioField,
    SubmitField
)
from wtforms import validators, ValidationError

from .models import bcrypt


class ChangePasswordForm(FlaskForm):
    """Форма смены пароля."""
    old_password = PasswordField('Old Password', validators=[
        validators.InputRequired(),
    ])
    password = PasswordField('New Password', validators=[
        validators.InputRequired(),
        validators.EqualTo('password_confirm'),
        validators.Length(min=8, max=500)
    ], description=[
        'Your password can’t be too similar to your other personal information.',
        'Ваш пароль должен содержать как минимум 8 символов.',
        'Your password can’t be a commonly used password.',
        'Your password can’t be entirely numeric.',
    ])
    password_confirm = PasswordField('Retype password', validators=[
        validators.InputRequired()
    ])

    def validate_old_password(self, field):
        if not bcrypt.check_password_hash(current_user.password, field.data):
            raise ValidationError('Wrong password.')


class RecoverPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[
        validators.InputRequired(),
        validators.EqualTo('password_confirm'),
        validators.Length(min=8, max=500)
    ], render_kw={'data-icon': 'fas fa-lock'})
    password_confirm = PasswordField('Retype password', validators=[
        validators.InputRequired()
    ], render_kw={'data-icon': 'fas fa-lock'})


class RegistrationForm(FlaskForm):
    """Форма регистрации, шаг 1: ввод E-Mail."""
    email = StringField('E-Mail', validators=[
        validators.InputRequired(),
        validators.Email(),
    ], render_kw={'data-icon': 'fas fa-envelope'})
    password = PasswordField('Password', validators=[
        validators.InputRequired(),
        validators.EqualTo('password_confirm'),
        validators.Length(min=8, max=500)
    ], render_kw={'data-icon': 'fas fa-lock'})
    password_confirm = PasswordField('Retype password', validators=[
        validators.InputRequired()
    ], render_kw={'data-icon': 'fas fa-lock'})
    firstname = StringField('Firstname', validators=[
        validators.Optional(),
        validators.Length(min=1, max=255)
    ], render_kw={'data-icon': 'fas fa-user'})
    lastname = StringField('Lastname', validators=[
        validators.Optional(),
        validators.Length(min=1, max=255)
    ], render_kw={'data-icon': 'fas fa-user'})
    agree_terms = BooleanField(validators=[
        validators.InputRequired(),
    ])
