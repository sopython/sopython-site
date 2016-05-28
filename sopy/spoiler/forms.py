from flask_wtf import Form
from wtforms.validators import InputRequired
from sopy.ext.forms import StripTextAreaField


class SpoilerForm(Form):
    message = StripTextAreaField(validators=[InputRequired()])
