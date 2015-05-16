from flask import redirect, render_template, request, session, url_for
from flask_wtf import Form
from sopy import db
from sopy.auth.login import group_required, current_user, login_required, require_group, has_group
from sopy.ext.views import redirect_for
from sopy.wiki import bp
from sopy.wiki.forms import WikiPageForm, WikiPageEditorForm
from sopy.wiki.models import WikiPage


@bp.route('/')
def index():
    pages = WikiPage.query.filter(WikiPage.redirect_id.is_(None)).order_by(WikiPage.title)

    if not has_group('editor'):
        pages = pages.filter(db.not_(WikiPage.draft))

    pages = pages.all()

    return render_template('wiki/index.html', pages=pages)


@bp.route('/<wiki_title:title>')
def detail(title):
    page = WikiPage.query.filter(WikiPage.title == title).options(db.joinedload(WikiPage.redirect)).first_or_404()

    if page.redirect and 'no_redirect' not in request.args:
        session['redirect_from'] = title
        return redirect(page.redirect.detail_url)

    if 'redirect_from' in session:
        redirect_from = session['redirect_from']
        del session['redirect_from']
    else:
        redirect_from = None

    return render_template('wiki/detail.html', page=page, redirect_from=redirect_from)


@bp.route('/create', endpoint='create', methods=['GET', 'POST'])
@bp.route('/<wiki_title:title>/update', methods=['GET', 'POST'])
@login_required
def update(title=None):
    page = WikiPage.query.filter(WikiPage.title == title).first_or_404() if title is not None else None

    if current_user.reputation < 100 or not (page is None or page.draft or page.community):
        require_group('editor')

    form = WikiPageEditorForm(obj=page) if has_group('editor') else WikiPageForm(obj=page)

    if form.validate_on_submit():
        if page is None:
            page = WikiPage()
            db.session.add(page)
        else:
            page.redirect = None

            if page.title != form.title.data:
                db.session.add(WikiPage(title=page.title, body='', redirect=page, author=current_user))

        page.author = current_user
        form.populate_obj(page)
        db.session.commit()

        return redirect(page.detail_url)

    return render_template('wiki/update.html', page=page, form=form)



@bp.route('/<wiki_title:title>/delete', methods=['GET', 'POST'])
@group_required('editor')
def delete(title):
    page = WikiPage.query.filter(WikiPage.title == title).first_or_404()
    form = Form()

    if form.validate_on_submit():
        db.session.delete(page)
        db.session.commit()

        return redirect_for('wiki.index')

    return render_template('wiki/delete.html', page=page, form=form)
