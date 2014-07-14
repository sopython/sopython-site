from flask_wtf import Form
from wtforms.fields import StringField, TextAreaField
from wtforms.validators import InputRequired


class CanonItemForm(Form):
    title = StringField(validators=[InputRequired()])
    excerpt = TextAreaField()
    body = TextAreaField()
    tags = StringField()
    questions = TextAreaField()
