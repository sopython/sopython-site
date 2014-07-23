from flask_wtf import Form
from wtforms.fields import StringField, TextAreaField
from wtforms.validators import InputRequired


class WikiPageForm(Form):
    title = StringField(validators=[InputRequired()])
    body = TextAreaField()
