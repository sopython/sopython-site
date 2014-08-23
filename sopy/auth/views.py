from urllib.parse import urlencode, parse_qs
from flask import url_for, redirect, request, session, current_app, g
import requests
from sopy import db
from sopy.auth import bp
from sopy.auth.forms import LoginForm
from sopy.auth.login import login_user, logout_user
from sopy.auth.models import User
from sopy.ext.views import redirect_for, redirect_next, template


@bp.route('/login', methods=['GET', 'POST'])
@template('auth/login.html')
def login():
    if current_app.debug and 'SE_CONSUMER_KEY' not in current_app.config:
        form = LoginForm()

        if form.validate_on_submit():
            login_user(form.user)
            db.session.commit()

            return redirect_next()

        return {'form': form}

    qs = urlencode({
        'client_id': current_app.config['SE_CONSUMER_KEY'],
        'redirect_uri': url_for('auth.authorized', next=request.args.get('next'), _external=True)
    })
    url = 'https://stackexchange.com/oauth?{}'.format(qs)

    return redirect(url)


@bp.route('/login/authorized')
def authorized():
    r = requests.post('https://stackexchange.com/oauth/access_token', {
        'client_id': current_app.config['SE_CONSUMER_KEY'],
        'client_secret': current_app.config['SE_CONSUMER_SECRET'],
        'code': request.args['code'],
        'redirect_uri': url_for('auth.authorized', next=request.args.get('next'), _external=True)
    })

    session['oauth_token'] = parse_qs(r.text)['access_token'][0]
    login_user(User.oauth_load())
    db.session.commit()

    return redirect_next()


@bp.route('/logout')
def logout():
    session.pop('oauth_token', None)
    logout_user()

    return redirect_for('index')
