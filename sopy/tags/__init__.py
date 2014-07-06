from flask import Blueprint

bp = Blueprint('tags', __name__)


@bp.record_once
def register(state):
    from sopy.tags import models
