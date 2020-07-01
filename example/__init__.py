from flask import Flask, render_template, url_for, request, abort, redirect, session
from flask_login import current_user
from flask_wtf import CSRFProtect

from .extensions import adminlte, babel, login_manager
from .models import bcrypt, db, Menu, User
from .cli import init_group
from .routes import auth, demo, site


app = Flask(__name__)
app.config.from_pyfile('config.py')

CSRFProtect(app)
bcrypt.init_app(app)
db.init_app(app)
babel.init_app(app)
login_manager.init_app(app)
adminlte.init_app(app)

app.cli.add_command(init_group)

app.register_blueprint(auth.bp)
app.register_blueprint(demo.bp)
app.register_blueprint(site.bp)


@app.route('/search')
def search():
    return render_template('adminlte_full/search_results.html', q=request.args['q'])


@app.route('/profile')
def profile():
    return f'{current_user}'


# @app.route('/registration', endpoint='auth.registration')
# def registration():
#     return render_template('adminlte_full/recover_password.html')
#     return render_template('adminlte_full/forgot_password.html')


@app.route('/lockscreen.html', endpoint='auth.lockscreen', methods=['GET', 'POST'])
def lockscreen():
    return render_template('adminlte_full/lockscreen.html')


db.create_all(app=app)
