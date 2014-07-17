from sopy.nidaba import bp
from sopy.ext.views import template


@bp.route('/')
@template('nidaba/index.html')
def index():
    items = 2

    return {'items': items}



