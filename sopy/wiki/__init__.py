from flask import Blueprint

bp = Blueprint('wiki', __name__)


@bp.record_once
def register(state):
    from sopy.wiki import views
