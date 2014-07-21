from flask import Blueprint

bp = Blueprint('sodata', __name__)


@bp.record_once
def register(state):
    from sopy.se_data import models
