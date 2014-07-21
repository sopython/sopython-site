from flask import Blueprint

bp = Blueprint('auth', __name__)


@bp.record_once
def register(state):
    from sopy.auth import login, views
    from sopy.auth.commands import cli

    state.app.cli.add_command(cli, 'auth')
