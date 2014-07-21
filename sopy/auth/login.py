from functools import wraps
from flask import session, g, request
from werkzeug.local import LocalProxy
from sopy import db
from sopy.auth import bp
from sopy.ext.views import redirect_for


class UserMixin(object):
    """Placeholders for all the attributes a user object should have."""

    id = None
    superuser = False

    _groups = set()
    groups = set()

    authenticated = True
    anonymous = False

    def has_group(self, group):
        raise NotImplementedError


class AnonymousUser(UserMixin):
    """Has no permissions.  Used when no user is logged in."""

    authenticated = False
    anonymous = True

    def has_group(self, group):
        return False


def login_user(user):
    """Add the user to the session.

    :param user: user instance to log in
    """
    session['user_id'] = user.id
    g.current_user = user


def logout_user():
    """Remove the user from the session."""
    #TODO: invalidate token with api
    session.pop('user_id', None)
    g.current_user = AnonymousUser()


@bp.before_app_request
def load_user():
    """Get the user from the session and store it as the current user.

    If no user was loaded, an anonymous user is stored.
    """
    user_id = session.get('user_id')

    if user_id is None:
        g.current_user = AnonymousUser()
    else:
        from sopy.auth.models import User

        user = User.query.options(db.joinedload(User._groups)).get(user_id)
        g.current_user = user if user is not None else AnonymousUser()


def _get_current_user():
    """Get the current user, or an anonymous user if no user is set."""
    try:
        return g.current_user
    except AttributeError:
        return AnonymousUser()


current_user = LocalProxy(_get_current_user)
"""Proxy to the current user."""


def has_group(group):
    """Check if the current user is in the group."""
    return current_user.has_group(group)


@bp.app_context_processor
def auth_context():
    """Add auth-related values to the template context.

    * current_user
    """
    return {
        'current_user': current_user,
        'has_group': has_group,
    }


def login_required(func):
    """Redirect to the login page if the current user is anonymous."""
    @wraps(func)
    def check_auth(*args, **kwargs):
        if current_user.anonymous:
            return redirect_for('auth.login', next=request.path)

        return func(*args, **kwargs)

    return check_auth


def group_required(group):
    """Redirect to the login page if the current user is not in the group.

    If they are logged in but don't have permission, don't try to log in, it will result in an infinite loop.
    """
    def decorator(func):
        @wraps(func)
        def check_auth(*args, **kwargs):
            if current_user.authenticated:
                return redirect_for('index')

            if not current_user.has_group(group):
                return redirect_for('auth.login', next=request.path)

            return func(*args, **kwargs)

        return check_auth

    return decorator
