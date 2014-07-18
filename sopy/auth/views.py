from flask import url_for, request, session
from sopy import oauth_so
from sopy.auth import bp
from sopy.ext.views import redirect_for


@bp.route('/login')
def login():
    return oauth_so.authorize(url_for('auth.authorize', _external=True))


@bp.route('/login/authorize')
@oauth_so.authorized_handler
def authorize(data):
    if data is None:
        return 'Error {}: {}'.format(
            request.args['error'],
            request.args['error_description']
        )

    session['oauth_so_token'] = data['access_token']
    return redirect_for('index')


@oauth_so.tokengetter
def get_oauth_so_token():
    return session.get('oauth_so_token')


@bp.route('/logout')
def logout():
    session.pop('oauth_so_token', None)
    return redirect_for('index')
