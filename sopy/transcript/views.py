from flask import render_template, redirect
from flask_wtf import Form
from sopy import db
from sopy.auth.login import group_required
from sopy.ext.views import redirect_for
from sopy.transcript import bp
from sopy.transcript.forms import CreateTranscriptForm, UpdateTranscriptForm
from sopy.transcript.models import Transcript


@bp.route('/')
def index():
    items = Transcript.query.options(db.subqueryload('messages').joinedload('user')).order_by(Transcript.ts.desc()).all()
    return render_template('transcript/index.html', items=items)


@bp.route('/<id_slug:id>/')
def detail(id):
    item = Transcript.query.options(db.subqueryload('messages').joinedload('user')).get_or_404(id)
    return render_template('transcript/detail.html', item=item)


@bp.route('/create', endpoint='create', methods=['GET', 'POST'])
@bp.route('/<int:id>/update', methods=['GET', 'POST'])
@group_required('Dark Council')
def update(id=None):
    item = Transcript.query.options(db.subqueryload('messages').joinedload('user')).get_or_404(id) if id is not None else None
    was_empty = id is None or not item.messages
    form = CreateTranscriptForm(obj=item) if was_empty else UpdateTranscriptForm(obj=item)

    if form.validate_on_submit():
        if item is None:
            item = Transcript()
            db.session.add(item)

        form.populate_obj(item)
        choose_messages = was_empty and item.messages
        db.session.commit()
        return redirect(item.update_url if choose_messages else item.detail_url)

    return render_template('transcript/update.html', item=item, form=form)


@bp.route('/<int:id>/delete', methods=['GET', 'POST'])
@group_required('Dark Council')
def delete(id):
    item = Transcript.query.get_or_404(id)
    form = Form()

    if form.validate_on_submit():
        db.session.delete(item)
        db.session.commit()
        return redirect_for('transcript.index')

    return render_template('transcript/delete.html', item=item, form=form)
