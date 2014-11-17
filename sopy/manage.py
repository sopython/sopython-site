import click
from flask import current_app
from flask.cli import FlaskGroup, with_appcontext
from sopy import create_app

cli = FlaskGroup(create_app=create_app)


@cli.command('shell')
@click.option('--plain', is_flag=True, help='Use a plain shell even if iPython is installed.')
@with_appcontext
def shell_command(plain=False):
    """Run a Python shell in the app context."""

    try:
        import IPython
    except ImportError:
        IPython = None

    if IPython is not None and not plain:
        IPython.embed(banner1='', user_ns=current_app.make_shell_context())
    else:
        import code

        code.interact(banner='', local=current_app.make_shell_context())
