from datetime import datetime, timedelta

from adminlte_base import Dropdown, Message, Notification, Task, ThemeColor, ThemeLayout, MenuLoader
from babel import Locale
from flask import request, session
from flask_adminlte_full import AdminLTE
from flask_babel import Babel
from flask_login import LoginManager, current_user

from .models import bcrypt, db, Menu, User


adminlte = AdminLTE()
babel = Babel()
login_manager = LoginManager()


@babel.localeselector
def get_locale():
    if current_user.is_anonymous or not current_user.locale:
        return session.get('_current_locale', request.accept_languages.best_match(['uk_UA', 'ru_RU', 'en_US']))
    return current_user.locale


@adminlte.manager.languages_loader
def load_languages():
    for l in ('ru_RU', 'uk_UA', 'ro_MD', 'en_US'):
        yield l, Locale.parse(l).get_display_name().title()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# @adminlte.manager.home_page_getter
# def home_page():
#     if current_user.is_anonymous:
#         return '/', 'Login'
#     return '/', 'Home'


@adminlte.manager.menu_loader
class MyMenuLoader(MenuLoader):
    def navbar_menu(self):
        data = Menu.query.filter_by(program_name='navbar_menu').first()

        if data:
            return self._create(data, request.path)

    def sidebar_menu(self):
        data = Menu.query.filter_by(program_name='main_menu').first()

        if data:
            return self._create(data, request.path)


@adminlte.manager.messages_loader
def load_messages():
    messages = Dropdown('#', 15)

    if current_user.is_authenticated:
        now = datetime.now()
        sender = current_user

        messages.add(Message(sender, 'Тестовое сообщение 1', '#', sent_at=now - timedelta(seconds=16)),)
        messages.add(Message(sender, 'Тестовое сообщение 2', '#', sent_at=now - timedelta(weeks=2)),)
        messages.add(Message(sender, 'Тестовое сообщение 3', '#'))

    return messages


@adminlte.manager.notifications_loader
def load_notifications():
    notifications = Dropdown('#', 10)
    notifications.add(Notification(
        '4 new messages',
        datetime.now() - timedelta(seconds=16),
        icon='fas fa-envelope',
        color=ThemeColor.SUCCESS
    ))
    notifications.add(Notification(
        '8 friend requests',
        datetime.now() - timedelta(hours=3),
        icon='fas fa-users'
    ))
    notifications.add(Notification(
        '3 new reports',
        icon='fas fa-file',
        color=ThemeColor.DANGER
    ))

    return notifications


@adminlte.manager.tasks_loader
def load_tasks():
    tasks = Dropdown('#')
    tasks.add(Task('Design some buttons', 20, '#'))
    tasks.add(Task('Create a nice theme', 40, '#', color=ThemeColor.SUCCESS))
    tasks.add(Task('Some task I need to do', 60, '#', color=ThemeColor.DANGER))
    tasks.add(Task('Make beautiful transitions', 80, '#', color=ThemeColor.WARNING))
    return tasks
