from flask import redirect
from flask_wtf import Form
from sopy import db
from sopy.auth.login import group_required, current_user
from sopy.ext.views import template, redirect_for
from sopy.wiki import bp
from sopy.wiki.forms import WikiPageForm
from sopy.wiki.models import WikiPage


@bp.route('/')
@template('wiki/index.html')
def index():
    pages = WikiPage.query.order_by(WikiPage.title).all()

    return {'pages': pages}


@bp.route('/<int:id>/')
@template('wiki/detail.html')
def detail(id):
    page = WikiPage.query.get_or_404(id)

    return {'page': page}


@bp.route('/create', endpoint='create', methods=['GET', 'POST'])
@bp.route('/<int:id>/update', methods=['GET', 'POST'])
@template('wiki/update.html')
@group_required('approved')
def update(id=None):
    page = WikiPage.query.get_or_404(id) if id is not None else None
    form = WikiPageForm(obj=page)

    if form.validate_on_submit():
        if page is None:
            page = WikiPage()
            db.session.add(page)

        form.populate_obj(page)
        page.author = current_user
        db.session.commit()

        return redirect(page.detail_url)

    return {'page': page, 'form': form}



@bp.route('/<int:id>/delete', methods=['GET', 'POST'])
@template('wiki/delete.html')
@group_required('approved')
def delete(id):
    page = WikiPage.query.get_or_404(id)
    form = Form()

    if form.validate_on_submit():
        db.session.delete(page)
        db.session.commit()

        return redirect_for('wiki.index')

    return {'page': page, 'form': form}
