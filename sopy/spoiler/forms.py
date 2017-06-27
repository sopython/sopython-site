from flask_wtf import Form
from wtforms import TextAreaField
from wtforms.validators import InputRequired

class SpoilerForm(Form):
    message = TextAreaField(validators=[InputRequired()])
