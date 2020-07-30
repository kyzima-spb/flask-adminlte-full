import json

import click
from flask.cli import AppGroup

from .models import db, MenuLink, Menu, MenuItem


init_group = AppGroup('init')


def create_menu_items(menu, items, parent=None):
    for attrs in items:
        children = attrs.pop('items', [])
        link = MenuLink(**attrs)
        db.session.add(link)
        db.session.commit()

        item = MenuItem(menu_id=menu.id, link=link)

        if parent is not None:
            item.parent = parent

        # menu.items.append(item)

        db.session.add(item)
        db.session.commit()

        if children:
            create_menu_items(menu, children, link)


@init_group.command()
def sqla():
    """Инициализирует базу данных минимальными данными, необходимыми для ее работы."""

    data = json.load(click.open_file('data/menu.json'))

    for menu in data.get('menu'):
        items = menu.pop('items', [])

        menu = Menu(title=menu['title'])
        db.session.add(menu)
        db.session.commit()

        if items:
            create_menu_items(menu, items)
