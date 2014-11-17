from functools import wraps
from flask import session, g, request, has_request_context, abort, current_app
from werkzeug.local import LocalProxy
from sopy import db
from sopy.auth import bp
from sopy.ext.views import redirect_for


class UserMixin:
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

    if has_request_context():
        session['user_id'] = user.id

    g.current_user = user


def logout_user():
    """Remove the user from the session."""

    #TODO: invalidate token with api
    if has_request_context():
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
        from sopy.auth.models import Group, User

        # pre-load group hierarchy to avoid extra queries
        Group.query.options(db.joinedload(Group._groups)).all()

        # load user and groups
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


def has_group(*groups):
    """Check if the current user is in the group."""

    return current_user.has_group(*groups)


@bp.app_context_processor
def auth_context():
    """Add auth-related values to the template context.

    * current_user
    * has_group
    """

    return {
        'current_user': current_user,
        'has_group': has_group,
    }


class LoginError(Exception):
    """Error raised to cause a redirect to the login page."""


@bp.app_errorhandler(LoginError)
def handle_login_error(e):
    """Redirect to the login page when LoginError is raised.

    If the user is logged in but doesn't have permission, don't try to log in, it will result in an infinite loop.
    Raise 403 Forbidden instead.
    """

    if not current_user.authenticated:
        return redirect_for('auth.login', next=request.path)

    # abort(403)
    # can't raise other handled exception from error handler, results in 500
    # so simulate what flask would do
    try:
        abort(403)
    except Exception as e:
        return current_app.handle_user_exception(e)


def require_login():
    """Redirect to the login page if the user is not logged in."""

    if current_user.anonymous:
        raise LoginError()


def login_required(func):
    """Decorate a function to require the user to be logged in."""

    @wraps(func)
    def check_auth(*args, **kwargs):
        require_login()

        return func(*args, **kwargs)

    return check_auth


def require_group(*groups):
    """Redirect to the login page if the user is not in at least one of the groups."""

    if not has_group(*groups):
        raise LoginError()


def group_required(*groups):
    """Decorate a function to require the user to have at least one of the groups."""

    def decorator(func):
        @wraps(func)
        def check_auth(*args, **kwargs):
            require_group(*groups)

            return func(*args, **kwargs)

        return check_auth

    return decorator
