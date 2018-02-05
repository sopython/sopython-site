from flask_wtf import FlaskForm
from wtforms import TextAreaField
from wtforms.validators import InputRequired

class SpoilerForm(FlaskForm):
    message = TextAreaField(validators=[InputRequired()])
