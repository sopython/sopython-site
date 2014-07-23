from flask import Blueprint

bp = Blueprint('pages', __name__)


@bp.record_once
def register(state):
    from sopy.pages import views
