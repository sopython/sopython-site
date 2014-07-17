from flask import Blueprint

bp = Blueprint('nidaba', __name__)


@bp.record_once
def register(state):
    from sopy.nidaba import views
