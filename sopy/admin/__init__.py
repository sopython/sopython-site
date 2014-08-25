from flask import Blueprint

bp = Blueprint('admin', __name__)


@bp.record_once
def register(state):
    from sopy.admin import views
