from flask import Blueprint

bp = Blueprint('transcript', __name__)


@bp.record_once
def register(state):
    from sopy.transcript import views
