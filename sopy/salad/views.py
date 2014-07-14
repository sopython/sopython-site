from flask_wtf import Form
from sopy import db
from sopy.ext.views import template, redirect_for
from sopy.salad import bp
from sopy.salad.forms import SaladForm
from sopy.salad.models import Salad


@bp.route('/')
@template('salad/index.html')
def index():
    # order by random to toss the salad
    items = Salad.query.order_by(db.func.random()).all()

    return {'items': items}


@bp.route('/create', endpoint='create', methods=['GET', 'POST'])
@bp.route('/<int:id>/update', methods=['GET', 'POST'])
@template('salad/update.html')
def update(id=None):
    item = Salad.query.get_or_404(id) if id is not None else None
    form = SaladForm(obj=item)

    if form.validate_on_submit():
        if item is None:
            item = Salad()
            db.session.add(item)

        form.populate_obj(item)
        db.session.commit()

        return redirect_for('salad.index')

    return {'item': item, 'form': form}


@bp.route('/<int:id>/delete', methods=['GET', 'POST'])
@template('salad/delete.html')
def delete(id):
    item = Salad.query.get_or_404(id)
    form = Form()

    if form.validate_on_submit():
        db.session.delete(item)
        db.session.commit()

        return redirect_for('salad.index')

    return {'item': item, 'form': form}
