from flask import Blueprint

bp = Blueprint('sodata', __name__)


@bp.record_once
def register(state):
    from sopy.sodata import models
