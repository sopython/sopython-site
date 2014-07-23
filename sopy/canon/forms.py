from flask_wtf import Form
from wtforms.fields import StringField, TextAreaField
from wtforms.validators import InputRequired
from wtforms.widgets.core import TextArea
from sopy.ext.forms import SeparatedField


class CanonItemForm(Form):
    title = StringField(validators=[InputRequired()])
    excerpt = TextAreaField()
    body = TextAreaField()
    tags = SeparatedField()
    question_links = SeparatedField('Questions', pattern=r'[\r\n]+', separator='\n', sort=True, widget=TextArea())
