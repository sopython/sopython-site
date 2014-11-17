import click
from flask.cli import AppGroup
from sopy import db
from sopy.se_data.models import SEUser


@click.command(cls=AppGroup)
def cli():
    """Manage Stack Exchange data."""


@cli.command()
def update_users():
    """Update all cached users with latest data."""

    with click.progressbar(SEUser.query.all(), label='Updating user data') as bar:
        for user in bar:
            user.se_update()

    db.session.commit()
