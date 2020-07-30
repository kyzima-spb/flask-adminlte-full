from adminlte_base.contrib import forms
from flask import current_app, url_for
from flask_wtf import FlaskForm
from werkzeug import routing
from wtforms.fields import SelectField
from wtforms.validators import ValidationError


class MenuLinkForm(FlaskForm, forms.MenuLinkForm):
    endpoint = SelectField(
        label='Endpoint name',
        description='The absolute name of the endpoint.'
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        del self.endpoint_args

        choices = [('', 'Allow empty')]

        for route in current_app.url_map.iter_rules():
            if 'GET' in route.methods:
                text = ', '.join(route.arguments)
                choices.append((route.endpoint, f'{route.endpoint}({text})'))

        self.endpoint.choices = choices

    def validate_endpoint_kwargs(self, field):
        endpoint = self.endpoint.data
        data = field.data.splitlines()

        if endpoint and data:
            kwargs = dict(map(str.strip, param.split('=')) for param in data)

            try:
                url_for(endpoint, **kwargs)
            except routing.BuildError as err:
                raise ValidationError(err)


LoginForm = type('LoginForm', (FlaskForm, forms.LoginForm), {})
ResetPasswordForm = type('ResetPasswordForm', (FlaskForm, forms.ResetPasswordForm), {})
