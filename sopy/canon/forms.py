from flask_wtf import Form
from wtforms.fields import StringField, TextAreaField
from wtforms.fields.core import BooleanField
from wtforms.validators import InputRequired
from wtforms.widgets.core import TextArea
from sopy.ext.forms import SeparatedField


class CanonItemForm(Form):
    title = StringField(validators=[InputRequired()])
    excerpt = TextAreaField()
    body = TextAreaField()
    tags = SeparatedField()
    question_links = SeparatedField('Questions', pattern=r'[\r\n]+', separator='\n', sort=True, widget=TextArea())


class CanonItemEditorForm(CanonItemForm):
    draft = BooleanField(description='Draft items are only visible to editors and any logged in user with a direct link.')
    community = BooleanField(description='Community items are editable by any logged in user.')
