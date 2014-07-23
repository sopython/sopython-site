from flask_wtf import Form
from wtforms.fields import StringField
from wtforms.validators import InputRequired


class SaladForm(Form):
    term = StringField(validators=[InputRequired()])
    definition = StringField(validators=[InputRequired()])
