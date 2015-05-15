from flask import Blueprint

bp = Blueprint('pages', __name__)


@bp.record_once
def register(state):
    from sopy.pages import views

    state.app.add_url_rule('/chatroom', None, views.page, defaults={'name': 'chatroom'})
