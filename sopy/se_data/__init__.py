from flask import Blueprint

bp = Blueprint('sodata', __name__)


@bp.record_once
def register(state):
    from . import commands

    state.app.cli.add_command(commands.cli, 'se')
