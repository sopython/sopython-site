from flask import Flask
from flask import render_template
from flask_alembic import Alembic
from flask_alembic.cli.click import cli as alembic_cli
from flask_babel import Babel
from sopy.ext.sqlalchemy import SQLAlchemy

__version__ = '1.4'

alembic = Alembic()
babel = Babel()
db = SQLAlchemy()


def create_app(info=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('sopy.config.defaults')
    app.config.from_pyfile('config.py', True)

    app.cli.add_command(alembic_cli, 'db')

    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True

    alembic.init_app(app)
    babel.init_app(app)
    db.init_app(app)

    from sopy.ext import views

    views.init_app(app)

    from sopy import auth, tags, se_data, canon, salad, wiki, pages, admin

    app.register_blueprint(auth.bp, url_prefix='/auth')
    app.register_blueprint(tags.bp, url_prefix='/tags')
    app.register_blueprint(se_data.bp, url_prefix='/se_data')
    app.register_blueprint(canon.bp, url_prefix='/canon')
    app.register_blueprint(salad.bp, url_prefix='/salad')
    app.register_blueprint(wiki.bp, url_prefix='/wiki')
    app.register_blueprint(pages.bp, url_prefix='/pages')
    app.register_blueprint(admin.bp, url_prefix='/admin')

    from sopy.ext.views import template

    @app.route('/')
    @template('index.html')
    def index():
        from sopy.salad.models import Salad

        return {'wod': Salad.word_of_the_day()}

    @app.errorhandler(403)
    def forbidden(e):
        return render_template('errors/403.html'), 403

    @app.errorhandler(404)
    def not_found(e):

        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500

    return app
