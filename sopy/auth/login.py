from functools import wraps
from flask import session, g, request
from werkzeug.local import LocalProxy
from sopy import db
from sopy.auth import bp
from sopy.ext.views import redirect_for


class UserMixin(object):
    id = None
    superuser = False

    _groups = set()
    groups = set()

    authenticated = True
    anonymous = False

    def has_group(self, group):
        raise NotImplementedError


class AnonymousUser(UserMixin):
    authenticated = False
    anonymous = True

    def has_group(self, group):
        return False


def login_user(user):
    session['user_id'] = user.id
    g.current_user = user


def logout_user():
    #TODO: invalidate token with api
    session.pop('user_id', None)
    g.current_user = AnonymousUser()


@bp.before_app_request
def load_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.current_user = AnonymousUser()
    else:
        from sopy.auth.models import User

        user = User.query.options(db.joinedload(User._groups)).get(user_id)
        g.current_user = user if user is not None else AnonymousUser()


def _get_current_user():
    try:
        return g.current_user
    except AttributeError:
        return AnonymousUser()


current_user = LocalProxy(_get_current_user)


@bp.app_context_processor
def auth_context():
    return {
        'current_user': current_user,
    }


def login_required(func):
    @wraps(func)
    def check_auth(*args, **kwargs):
        if current_user.anonymous:
            return redirect_for('auth.login', next=request.path)

        return func(*args, **kwargs)

    return check_auth


def group_required(group):
    def decorator(func):
        @wraps(func)
        def check_auth(*args, **kwargs):
            if not current_user.has_group(group):
                return redirect_for('auth.login', next=request.path)

            return func(*args, **kwargs)

        return check_auth

    return decorator
