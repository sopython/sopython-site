from flask import redirect
from flask_wtf import Form
from sopy import db
from sopy.auth.login import group_required, current_user, login_required, require_group, has_group
from sopy.ext.views import template, redirect_for
from sopy.wiki import bp
from sopy.wiki.forms import WikiPageForm, WikiPageEditorForm
from sopy.wiki.models import WikiPage


@bp.route('/')
@template('wiki/index.html')
def index():
    pages = WikiPage.query.order_by(WikiPage.title)

    if not has_group('editor'):
        pages = pages.filter(db.not_(WikiPage.draft))

    pages = pages.all()

    return {'pages': pages}


@bp.route('/<title>/')
@template('wiki/detail.html')
def detail(title):
    page = WikiPage.query.filter(WikiPage.title == title).first_or_404()

    return {'page': page}


@bp.route('/create', endpoint='create', methods=['GET', 'POST'])
@bp.route('/<title>/update', methods=['GET', 'POST'])
@template('wiki/update.html')
@login_required
def update(title=None):
    page = WikiPage.query.filter(WikiPage.title == title).first_or_404() if title is not None else None

    if not (page is None or page.draft or page.community):
        require_group('editor')

    form = WikiPageEditorForm(obj=page) if has_group('editor') else WikiPageForm(obj=page)

    if form.validate_on_submit():
        if page is None:
            page = WikiPage()
            db.session.add(page)

        form.populate_obj(page)
        page.author = current_user
        db.session.commit()

        return redirect(page.detail_url)

    return {'page': page, 'form': form}



@bp.route('/<title>/delete', methods=['GET', 'POST'])
@template('wiki/delete.html')
@group_required('editor')
def delete(title):
    page = WikiPage.query.filter(WikiPage.title == title).first_or_404()
    form = Form()

    if form.validate_on_submit():
        db.session.delete(page)
        db.session.commit()

        return redirect_for('wiki.index')

    return {'page': page, 'form': form}
