from flask_wtf import Form
from wtforms.validators import InputRequired
from sopy.ext.forms import StripStringField


class SaladForm(Form):
    term = StripStringField(validators=[InputRequired()])
    definition = StripStringField(validators=[InputRequired()])
