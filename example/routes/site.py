from flask import Blueprint, render_template, session, redirect, url_for
from flask_login import current_user

from ..extensions import adminlte, db


bp = Blueprint('site', __name__)


@bp.route('/')
def index():
    adminlte.flash.debug('SQL statements were executed.')
    adminlte.flash.info('Three credits remain in your account.')
    adminlte.flash.success('Profile details updated.')
    adminlte.flash.warning('Your account expires in three days.')
    adminlte.flash.error('Document deleted.')
    return render_template('adminlte_full/base.html')


@bp.route('/change_locale/<locale>')
def change_language(locale):
    name = adminlte.manager.get_available_languages(as_dict=True).get(locale)

    if name is None:
        adminlte.flash.error('The selected language is not supported.')
    elif current_user.is_authenticated:
        current_user.locale = locale
        db.session.commit()
        adminlte.flash.success(f'Language successfully changed to "{name}".')
    else:
        session['_current_locale'] = locale

    return redirect(url_for('blank'))


@bp.route('/terms')
def terms():
    return render_template('terms.html')
