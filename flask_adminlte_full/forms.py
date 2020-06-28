from adminlte_base.contrib import forms
from flask_wtf import FlaskForm


LoginForm = type('LoginForm', (FlaskForm, forms.LoginForm), {})
ResetPasswordForm = type('ResetPasswordForm', (FlaskForm, forms.ResetPasswordForm), {})
