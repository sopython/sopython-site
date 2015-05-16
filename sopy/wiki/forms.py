from flask_wtf import Form
import re
from markupsafe import Markup
from wtforms.fields import TextAreaField, BooleanField
from wtforms.validators import DataRequired, ValidationError
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

        existing = WikiPage.query.filter_by(title=title).first()

        # check existing title when creating new page
        # skip if existing page is current page when editing
        if existing is not None and (self.obj is None or self.obj.id != existing.id):
            raise ValidationError(Markup('<a href="{}">A page with this title</a> already exists.  Rename or delete it before continuing.'.format(existing.detail_url)))


class WikiPageEditorForm(WikiPageForm):
    draft = BooleanField(description='Draft items are only visible to editors and any logged in user with a direct link.')
    community = BooleanField(description='Community items are editable by any logged in user.')
