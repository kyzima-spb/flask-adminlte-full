from adminlte_base.contrib.sqla import create_entity_menu_item, create_entity_menu
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.hybrid import hybrid_property

from .extensions import bcrypt


db = SQLAlchemy()

MenuItem = create_entity_menu_item(db)
Menu = create_entity_menu(db)


class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True)
    email = Column(String(50), unique=True, nullable=False)
    _password = Column(String(500), name='password', nullable=False)
    active = Column(Boolean, default=False, nullable=False)
    firstname = Column(String(255), default='', nullable=False)
    lastname = Column(String(255), default='', nullable=False)
    locale = Column(String(20), default='', nullable=False)

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = bcrypt.generate_password_hash(value).decode('utf-8')

    def get_full_name(self):
        return f'{self.firstname} {self.lastname}'.strip() or self.email
