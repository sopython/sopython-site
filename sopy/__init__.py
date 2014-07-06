from flask import Flask
from flask_alembic import Alembic
from flask_alembic.cli.click import cli as alembic_cli
from sopy.ext.sqlalchemy import SQLAlchemy

alembic = Alembic()
db = SQLAlchemy()


def create_app(info=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('sopy.config.defaults')
    app.config.from_pyfile('config.py', True)

    app.cli.add_command(alembic_cli, 'db')

    alembic.init_app(app)
    db.init_app(app)

    from sopy import tags, sodata, canon

    app.register_blueprint(tags.bp, url_prefix='/tags')
    app.register_blueprint(sodata.bp, url_prefix='/sodata')
    app.register_blueprint(canon.bp, url_prefix='/canon')

    return app
