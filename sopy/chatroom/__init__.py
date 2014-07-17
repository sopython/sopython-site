from flask import Blueprint

bp = Blueprint('chatroom', __name__)


@bp.record_once
def register(state):
    from sopy.chatroom import views
