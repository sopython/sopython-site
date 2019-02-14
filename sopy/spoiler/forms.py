from flask_wtf import FlaskForm
from wtforms import TextAreaField

class SpoilerForm(FlaskForm):
    message = TextAreaField(validators=[])
