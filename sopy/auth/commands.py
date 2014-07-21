import click
from sopy import db
from sopy.auth.models import User, Group


@click.group()
def cli():
    """Manage users and groups."""
    pass


@cli.command()
@click.argument('user_id')
def load_user(user_id):
    """Get a user from Stack Overflow."""
    user = User.se_load(user_id)
    db.session.commit()
    click.echo('Loaded user {}'.format(user.display_name))


@cli.command()
@click.option('-r', '--remove', is_flag=True)
@click.argument('user_id')
@click.argument('group_name')
def set_group(user_id, group_name, remove=False):
    """Add a user to a group."""
    user = User.query.filter_by(id=user_id).one()
    group = Group.query.filter_by(name=group_name).one()

    if not remove:
        user._groups.add(group)
    else:
        user._groups.discard(group)

    db.session.commit()


@cli.command()
@click.option('-r', '--remove', is_flag=True)
@click.argument('user_id')
def set_superuser(user_id, remove=False):
    """Make a user a superuser."""
    user = User.query.filter_by(id=user_id).one()
    user.superuser = not remove
    db.session.commit()
