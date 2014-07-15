from flask import Flask, render_template
from flask_alembic import Alembic
from flask_alembic.cli.click import cli as alembic_cli
from sopy.ext.sqlalchemy import SQLAlchemy
from sopy.ext.views import template

alembic = Alembic()
db = SQLAlchemy()


def create_app(info=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('sopy.config.defaults')
    app.config.from_pyfile('config.py', True)

    app.cli.add_command(alembic_cli, 'db')

    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True

    alembic.init_app(app)
    db.init_app(app)

    from sopy.ext import views

    views.init_app(app)

    from sopy import tags, sodata, canon, salad

    app.register_blueprint(tags.bp, url_prefix='/tags')
    app.register_blueprint(sodata.bp, url_prefix='/sodata')
    app.register_blueprint(canon.bp, url_prefix='/canon')
    app.register_blueprint(salad.bp, url_prefix='/salad')

    from sopy.salad.models import Salad

    @app.route('/')
    @template('index.html')
    def index():
        return {'wod': Salad.word_of_the_day()}

    return app

if __name__ == '__main__':
    app = create_app()

    app.run(debug=True)