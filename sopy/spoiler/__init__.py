from flask import Blueprint

bp = Blueprint('spoiler', __name__)


@bp.record_once
def register(state):
    from sopy.spoiler import views
