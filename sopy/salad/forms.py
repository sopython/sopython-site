from flask_wtf import FlaskForm
from wtforms.validators import InputRequired
from sopy.ext.forms import StripStringField


class SaladForm(FlaskForm):
    term = StripStringField(validators=[InputRequired()])
    definition = StripStringField(validators=[InputRequired()])
