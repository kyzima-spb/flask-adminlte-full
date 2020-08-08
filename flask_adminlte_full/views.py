from functools import partial

from adminlte_base.core import AbstractMenuFormFactory, AbstractMenuModelFactory
from flask import current_app, Blueprint, redirect, url_for, abort
from flask_useful.views import MethodView
from flask_useful.utils import make_redirect


__all__ = ('create_menu_blueprint',)


class BaseView(MethodView):
    form_factory: AbstractMenuFormFactory = None
    model_factory: AbstractMenuModelFactory = None


class Links(BaseView):
    def get(self):
        links = self.model_factory.create_link_query().all()
        names = {"id", "title", "type", "endpoint", "url"}
        data = []

        for link in links:
            data.append({name: getattr(link, name) for name in names})

        return {'data': data}


class LinkCreate(BaseView):
    template_name = 'adminlte_full/menus/links/create.html'
    link_post_redirect = None

    def get(self):
        form = self.form_factory.create_link_form()
        return self.render_template(form=form)

    def post(self):
        form = self.form_factory.create_link_form()

        if form.validate_on_submit():
            link = self.model_factory.create_link()
            form.populate_obj(link)
            link.save()
            return self.link_post_redirect(link)

        return self.render_template(form=form)


class LinkEdit(BaseView):
    template_name = 'adminlte_full/menus/links/edit.html'
    link_post_redirect = None

    def get(self, id):
        link = self.model_factory.create_item_query().get(id) or abort(404)
        form = self.form_factory.create_link_form(link)
        return self.render_template(form=form)

    def post(self, id):
        link = self.model_factory.create_item_query().get(id) or abort(404)
        form = self.form_factory.create_link_form(link)

        if form.validate_on_submit():
            form.populate_obj(link)
            link.save()
            return self.link_post_redirect(link)

        return self.render_template(form=form)


class MenuDashboard(BaseView):
    template_name = 'adminlte_full/menus/index.html'

    def get(self):
        form = self.form_factory.create_menu_form()
        all_menus = self.model_factory.create_menu_query().all()
        return self.render_template(all_menus=all_menus, form=form)


class MenuCreate(BaseView):
    template_name = 'adminlte_full/menus/create.html'
    menu_post_redirect = None

    def post(self):
        form = self.form_factory.create_menu_form()

        if form.validate_on_submit():
            menu = self.model_factory.create_menu()
            form.populate_obj(menu)
            menu.save()
            return self.menu_post_redirect(menu)

        return self.render_template(form=form)


class MenuShow(BaseView):
    template_name = 'adminlte_full/menus/menu.html'

    def get(self, id):
        menu = self.model_factory.create_menu_query().get(id) or abort(404)
        menu_form = self.form_factory.create_menu_form(obj=menu)
        menu_item_form = self.form_factory.create_item_form()
        return self.render_template(
            menu=menu, menu_form=menu_form, menu_item_form=menu_item_form
        )


class MenuEdit(BaseView):
    template_name = 'adminlte_full/menus/edit.html'

    def post(self, id):
        menu = self.model_factory.create_menu_query().get(id) or abort(404)
        form = self.form_factory.create_menu_form(obj=menu)

        if form.validate_on_submit():
            form.populate_obj(menu)
            menu.save()
            return redirect(url_for('.edit', id=id))

        return self.render_template(form=form, menu=menu)


class MenuItemCreate(BaseView):
    template_name = 'adminlte_full/menus/items/create.html'

    def post(self, id):
        menu = self.model_factory.create_menu_query().get(id) or abort(404)
        form = self.form_factory.create_item_form()

        if form.validate_on_submit():
            item = self.model_factory.create_item(
                menu=menu,
                link=form.link.data,
                parent=form.parent.data,
                before=form.before.data
            )
            item.save()
            return redirect(url_for('.edit', id=id))

        return self.render_template(form=form, menu=menu)


class MenuItemEdit(BaseView):
    template_name = 'adminlte_full/menus/items/edit.html'

    def get(self, menu_id, link_id):
        item = self.model_factory.create_item_query().get(menu_id, link_id) or abort(404)
        form = self.form_factory.create_item_form(obj=item)
        return self.render_template(form=form, menu=item.menu)

    def post(self, menu_id, link_id):
        item = self.model_factory.create_item_query().get(menu_id, link_id) or abort(404)
        form = self.form_factory.create_item_form(obj=item)

        if form.validate_on_submit():
            item.link = form.link.data
            item.parent = form.parent.data
            item.before = form.before.data
            item.save()
            return redirect(url_for('.edit', id=menu_id))

        return self.render_template(form=form, menu=item.menu)


def create_menu_blueprint(name, import_name, model_factory, form_factory, url_prefix):
    bp = Blueprint(name, import_name, url_prefix=url_prefix)

    BaseView.form_factory = form_factory
    BaseView.model_factory = model_factory

    LinkCreate.link_post_redirect = LinkEdit.link_post_redirect = partial(make_redirect, {
        'Save': f'{name}.links_edit',
        'Save and Create': f'{name}.links_create',
        'Save and Close': f'{name}.index',
    })
    MenuCreate.menu_post_redirect = partial(make_redirect, {
        'Save': f'{name}.index',
        'Save and Edit': f'{name}.show',
    })

    bp.add_url_rule('/', view_func=MenuDashboard.as_view('index'))
    bp.add_url_rule('/', view_func=MenuCreate.as_view('create'))
    bp.add_url_rule('/<int:id>', view_func=MenuShow.as_view('show'))
    bp.add_url_rule('/<int:id>', view_func=MenuEdit.as_view('edit'))
    bp.add_url_rule('/<int:id>/items', view_func=MenuItemCreate.as_view('items'))
    bp.add_url_rule('/<int:menu_id>/items/<int:link_id>', view_func=MenuItemEdit.as_view('items_edit'))
    bp.add_url_rule('/links', view_func=Links.as_view('links'))
    bp.add_url_rule('/links/create', view_func=LinkCreate.as_view('links_create'))
    bp.add_url_rule('/links/<int:id>', view_func=LinkEdit.as_view('links_edit'))

    return bp
