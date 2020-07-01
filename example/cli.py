import json

import click
from flask.cli import AppGroup

from .models import db, Menu, MenuItem


init_group = AppGroup('init')


def create_menu_items(menu, items, parent=None):
    for i in items:
        children = i.pop('items', [])
        attrs = {'menu': menu, **i}

        if parent is not None:
            attrs['parent'] = parent

        item = MenuItem(**attrs)
        db.session.add(item)
        db.session.commit()

        if children:
            create_menu_items(menu, children, item)


@init_group.command()
def sqla():
    """Инициализирует базу данных минимальными данными, необходимыми для ее работы."""

    data = json.load(click.open_file('data/menu.json'))

    for menu in data.get('menu'):
        items = menu.pop('items', [])

        menu = Menu(**menu)
        db.session.add(menu)
        db.session.commit()

        if items:
            create_menu_items(menu, items)
