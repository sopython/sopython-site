from flask import Blueprint

bp = Blueprint('auth', __name__)


@bp.record_once
def register(state):
    from sopy.auth import views
