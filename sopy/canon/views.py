from flask import redirect, render_template
from flask_wtf import FlaskForm
from sopy import db
from sopy.auth.login import group_required, current_user, login_required, require_group, has_group
from sopy.canon import bp
from sopy.canon.forms import CanonItemForm, CanonItemEditorForm, CanonSearchForm
from sopy.canon.models import CanonItem
from sopy.ext.forms import PaginationForm
from sopy.ext.views import redirect_for


@bp.route('/')
def index():
    form = CanonSearchForm()
    pg = PaginationForm.auto(form.apply())

    return render_template('canon/index.html', form=form, pg=pg)


@bp.route('/<id_slug:id>/')
def detail(id):
    item = CanonItem.query.get_or_404(id)

    return render_template('canon/detail.html', item=item)


@bp.route('/create', endpoint='create', methods=['GET', 'POST'])
@bp.route('/<int:id>/update', methods=['GET', 'POST'])
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

        item.updated_by = current_user
        form.populate_obj(item)
        db.session.commit()

        return redirect(item.detail_url)

    return render_template('canon/update.html', item=item, form=form)


@bp.route('/<int:id>/delete', methods=['GET', 'POST'])
@group_required('editor')
def delete(id):
    item = CanonItem.query.get_or_404(id)
    form = FlaskForm()

    if form.validate_on_submit():
        db.session.delete(item)
        db.session.commit()

        return redirect_for('canon.index')

    return render_template('canon/delete.html', item=item, form=form)
