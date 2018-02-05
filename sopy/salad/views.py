from flask import request, render_template
from flask_wtf import FlaskForm
from sopy import db
from sopy.auth.login import group_required, current_user
from sopy.ext.views import redirect_for
from sopy.salad import bp
from sopy.salad.forms import SaladForm
from sopy.salad.models import Salad


@bp.route('/')
def index():
    items = Salad.query.order_by(Salad.position).all()
    wod = Salad.word_of_the_day()
    highlight = request.args.get('highlight', '')

    return render_template('salad/index.html', items=items, wod=wod, highlight=highlight)


@bp.route('/create', endpoint='create', methods=['GET', 'POST'])
@bp.route('/<int:id>/update', methods=['GET', 'POST'])
@group_required('Dark Council')
def update(id=None):
    item = Salad.query.get_or_404(id) if id is not None else None
    form = SaladForm(obj=item)

    if form.validate_on_submit():
        if item is None:
            item = Salad()
            db.session.add(item)

        item.updated_by = current_user
        form.populate_obj(item)
        db.session.commit()

        return redirect_for('salad.index')

    return render_template('salad/update.html', item=item, form=form)


@bp.route('/<int:id>/move_up', endpoint='move_up')
@bp.route('/<int:id>/move_down', endpoint='move_down', defaults={'down': True})
@group_required('Dark Council')
def move(id, down=False):
    item = Salad.query.get_or_404(id)

    if down:
        item.move_down()
    else:
        item.move_up()

    db.session.commit()

    return redirect_for('salad.index')


@bp.route('/<int:id>/delete', methods=['GET', 'POST'])
@group_required('Dark Council')
def delete(id):
    item = Salad.query.get_or_404(id)
    form = FlaskForm()

    if form.validate_on_submit():
        item.delete()
        db.session.commit()

        return redirect_for('salad.index')

    return render_template('salad/delete.html', item=item, form=form)
