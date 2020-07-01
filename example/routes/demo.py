import json

from adminlte_base import ThemeColor, ThemeLayout
from adminlte_base.data_types import PageItem
from flask import (
    Blueprint,
    session, abort, redirect, url_for,
    render_template
)


bp = Blueprint('demo', __name__)


@bp.route('/error/<int:code>')
def error_page(code):
    abort(code)


@bp.route('/UI/general')
def ui_general():
    return render_template('pages/UI/general.html')


@bp.route('/layout/<layout>.html')
def layouts_options(layout):
    layout = layout.upper().replace('-', '_')

    title = layout.title().replace('_', ' ')
    layout = getattr(ThemeLayout, layout, set())

    if ThemeLayout.TOP_NAV <= layout:
        layout |= ThemeLayout.COLLAPSED_SIDEBAR | ThemeLayout.FIXED_TOP_NAV
    else:
        layout |= ThemeLayout.DEFAULT

    return render_template('pages/layouts_options.html', layout=layout, title=title)


@bp.route('/tables/simple')
def tables_simple():
    context = {
        'task_table': {
            'headers': ['Task', 'Progress', 'Label'],
            'data': [
                {'task': 'Update software', 'progress': 55, 'color': ThemeColor.PRIMARY},
                {'task': 'Clean database', 'progress': 70, 'color': ThemeColor.WARNING},
                {'task': 'Cron job running', 'progress': 30, 'color': ThemeColor.DANGER},
                {'task': 'Fix and squish bugs', 'progress': 90, 'color': ThemeColor.SUCCESS}
            ]
        },
        'user_table': {
            'headers': {
                'id': 'ID',
                'user': 'User',
                'date': 'Date',
                'status': 'Status',
                'reason': 'Reason'
            },
            'data': json.load(open('data/users.json')),
        },
        'pages': [PageItem('&laquo;'), PageItem(1), PageItem(2), PageItem(3), PageItem('&raquo;')],
    }
    return render_template('pages/tables/simple.html', **context)


@bp.route('/tables/data')
def tables_data():
    headers = {
        'engine': 'Rendering engine',
        'browser': 'Browser',
        'platform': 'Platform(s)',
        'version': 'Engine version',
        'grade': 'CSS grade'
    }

    data = json.load(open('data/browsers.json'))
    data_dict = [dict(zip(headers, v)) for v in data]

    context = {
        'browser_table': {
            'headers': headers,
            'data': data,
            'data_dict': data_dict,
        }
    }

    return render_template('pages/tables/data.html', **context)


@bp.route('/widgets')
def widgets():
    return render_template('pages/widgets.html')
