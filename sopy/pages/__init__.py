from flask import Blueprint

bp = Blueprint('pages', __name__)


@bp.record_once
def register(state):
    from sopy.pages import views

    # alias /pages/chatroom to /chatroom
    state.app.add_url_rule('/chatroom', 'pages.page', view_func=views.page, defaults={'name': 'chatroom'})
