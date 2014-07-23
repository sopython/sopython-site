from flask import Blueprint

bp = Blueprint('salad', __name__)


@bp.record_once
def register(state):
    from sopy.salad import views
