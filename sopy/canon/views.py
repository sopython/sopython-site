from flask import redirect, abort
from flask_wtf import Form
from sqlalchemy.sql.functions import user
from sopy import db
from sopy.auth.login import group_required, current_user, login_required, require_group, has_group
from sopy.canon import bp
from sopy.canon.forms import CanonItemForm, CanonItemEditorForm, CanonSearchForm
from sopy.canon.models import CanonItem
from sopy.ext.forms import PaginationForm
from sopy.ext.views import template, redirect_for


@bp.route('/')
@template('canon/index.html')
def index():
    form = CanonSearchForm()
    pg = PaginationForm.auto(form.apply())

    return {'form': form, 'pg': pg}


@bp.route('/<id_slug:id>/')
@template('canon/detail.html')
def detail(id):
    item = CanonItem.query.get_or_404(id)

    return {'item': item}


@bp.route('/create', endpoint='create', methods=['GET', 'POST'])
@bp.route('/<int:id>/update', methods=['GET', 'POST'])
@template('canon/update.html')
@login_required
def update(id=None):
    item = CanonItem.query.get_or_404(id) if id is not None else None

    if current_user.reputation < 100 or not (item is None or item.draft or item.community):
        require_group('editor')

    form = CanonItemEditorForm(obj=item) if has_group('editor') else CanonItemForm(obj=item)

    if form.validate_on_submit():
        if item is None:
            item = CanonItem()
            db.session.add(item)

        form.populate_obj(item)
        item.updated_by = current_user
        db.session.commit()

        return redirect(item.detail_url)

    return {'item': item, 'form': form}


@bp.route('/<int:id>/delete', methods=['GET', 'POST'])
@template('canon/delete.html')
@group_required('editor')
def delete(id):
    item = CanonItem.query.get_or_404(id)
    form = Form()

    if form.validate_on_submit():
        db.session.delete(item)
        db.session.commit()

        return redirect_for('canon.index')

    return {'item': item, 'form': form}
