from flask import current_app
from flask.cli import FlaskGroup
from IPython import embed
from sopy import create_app

cli = FlaskGroup(create_app=create_app)


@cli.command('shell', short_help='Runs a shell in the app context.')
def shell_command():
    """Runs an iPython shell in the Flask application context."""
    embed(banner1='', user_ns=current_app.make_shell_context())
