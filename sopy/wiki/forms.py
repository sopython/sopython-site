from flask_wtf import Form
from wtforms.fields import StringField, TextAreaField, BooleanField
from wtforms.validators import InputRequired


class WikiPageForm(Form):
    title = StringField(validators=[InputRequired()])
    body = TextAreaField()


class WikiPageEditorForm(WikiPageForm):
    draft = BooleanField(description='Draft items are only visible to editors and any logged in user with a direct link.')
    community = BooleanField(description='Community items are editable by any logged in user.')
