from flask_wtf import Form
import re
from wtforms.fields import TextAreaField, BooleanField
from wtforms.validators import DataRequired, ValidationError
from sopy import db
from sopy.ext.forms import StripStringField
from sopy.wiki.models import WikiPage


class WikiPageForm(Form):
    title = StripStringField(validators=[DataRequired()])
    body = TextAreaField()

    space_re = re.compile(r'\s+')
    invalid_re = re.compile(r'(^\.{1,2}$|[/_]|%[0-9a-f]{2}|&#?[0-9a-z]+?;)', re.I)

    def __init__(self, *args, **kwargs):
        self.obj = kwargs.get('obj')
        super().__init__(*args, **kwargs)

    def validate_title(self, field):
        field.data = title = self.space_re.sub(field.data, ' ').strip()
        match = self.invalid_re.search(title)

        if match:
            raise ValidationError('Invalid characters: "{}"'.format(match.group(1)))

        unique_title_q = db.session.query(db.func.count(WikiPage.id)).filter(WikiPage.title == title)

        if self.obj is not None:
            # When editing an existing page, only check *other* pages for duplicate titles.
            unique_title_q = unique_title_q.filter(WikiPage.id != self.obj.id)

        if unique_title_q.scalar():
            raise ValidationError('A page with this title already exists.')


class WikiPageEditorForm(WikiPageForm):
    draft = BooleanField(description='Draft items are only visible to editors and any logged in user with a direct link.')
    community = BooleanField(description='Community items are editable by any logged in user.')
