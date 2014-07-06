from flask import Blueprint

bp = Blueprint('canon', __name__)


@bp.record_once
def register(state):
    from sopy.canon import models
