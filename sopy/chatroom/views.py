from flask import redirect
from sopy.chatroom import bp
from sopy.ext.views import template, redirect_for


@bp.route('/')
@template('chatroom/index.html')
def index():
    items = 2

    return {'items': items}



