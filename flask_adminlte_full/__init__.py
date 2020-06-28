import os
import pkg_resources

from adminlte_base import (
    AbstractManager, FlashedMessage, ThemeColor, ThemeLayout, DEFAULT_SETTINGS, FlashedMessageLevel
)
from adminlte_base import filters
from flask import (
    Blueprint, current_app, url_for, request,
    render_template, get_flashed_messages, flash
)
# from flask_assets import Environment, Bundle
from flask_gravatar import Gravatar
from flask_login import current_user
from werkzeug.exceptions import HTTPException


class Flash(object):
    def _log(self, message, level):
        return flash(message, level)

    def debug(self, message):
        return self._log(message, FlashedMessageLevel.DEBUG)

    def error(self, message):
        return self._log(message, FlashedMessageLevel.ERROR)

    def info(self, message):
        return self._log(message, FlashedMessageLevel.INFO)

    def success(self, message):
        return self._log(message, FlashedMessageLevel.SUCCESS)

    def warning(self, message):
        return self._log(message, FlashedMessageLevel.WARNING)


class Manager(AbstractManager):
    def create_url(self, endpoint, *endpoint_args, **endpoint_kwargs):
        return url_for(endpoint, **endpoint_kwargs)

    def get_flash_messages(self):
        for level, message in get_flashed_messages(with_categories=True):
            yield FlashedMessage(level, message, level)

    def static(self, filename):
        asset = url_for('adminlte_full.static', filename=filename)

        if os.path.exists(current_app.static_folder + asset):
            return current_app.static_url_path + asset

        return asset


class AdminLTE(object):
    def __init__(self, app=None):
        self.app = app
        self.manager = Manager()
        self.flash = Flash()
        self.gravatar = Gravatar(default='mp')

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        if not hasattr(app, 'extensions'):
            app.extensions = {}

        app.extensions['adminlte_full'] = self

        for name, value in DEFAULT_SETTINGS.items():
            app.config.setdefault(name, value)

        # assets.init_app(app)
        self.gravatar.init_app(app)
        self.manager.user_getter(self.user_getter)
        self.manager.home_page = app.config['ADMINLTE_HOME_PAGE']

        self.register_blueprint(app)

        if not app.debug:
            app.register_error_handler(HTTPException, self.error_page)

        for name in filters.__all__:
            app.jinja_env.filters.setdefault(name, getattr(filters, name))

        @app.context_processor
        def processors():
            return dict(
                adminlte=self.manager,
                adminlte_user=self.manager.user,
                ThemeColor=ThemeColor,
                ThemeLayout=ThemeLayout,
            )

        if not hasattr(app.jinja_env, 'install_gettext_callables'):
            app.jinja_env.add_extension('jinja2.ext.i18n')
            app.jinja_env.install_null_translations(True)

    def error_page(self, err):
        """Page for all HTTP errors."""
        template = f'adminlte_full/http_error_page.html'
        context = {
            'status_code': err.code,
            'status_message': err.name,
            'details': err.get_description(),
        }
        return render_template(template, **context), err.code

    def register_blueprint(self, app):
        """Registers Blueprint."""
        app.register_blueprint(Blueprint(
            'adminlte_full',
            __name__,
            static_folder='static',
            template_folder=pkg_resources.resource_filename('adminlte_base', 'templates'),
            static_url_path='/adminlte_full'
        ))

    def user_getter(self):
        """Returns the current user."""
        return current_user, current_app.config['ADMINLTE_USER_MAPPING']
