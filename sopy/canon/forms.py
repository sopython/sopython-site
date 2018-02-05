from flask import request
from flask_wtf import FlaskForm
from wtforms import Form as BaseForm
from wtforms.fields import TextAreaField
from wtforms.fields.core import BooleanField
from wtforms.validators import InputRequired
from wtforms.widgets.core import TextArea
from sopy import db
from sopy.auth.login import has_group
from sopy.canon.models import CanonItem
from sopy.ext.forms import SeparatedField, StripStringField
from sopy.tags.models import Tag


class CanonItemForm(FlaskForm):
    title = StripStringField(validators=[InputRequired()])
    excerpt = TextAreaField()
    body = TextAreaField()
    tags = SeparatedField()
    question_links = SeparatedField('Questions', pattern=r'[\r\n]+', separator='\n', sort=True, widget=TextArea())


class CanonItemEditorForm(CanonItemForm):
    draft = BooleanField(description='Draft items are only visible to editors and any logged in user with a direct link.')
    community = BooleanField(description='Community items are editable by any logged in user.')


class CanonSearchForm(BaseForm):
    q = StripStringField()

    def __init__(self, formdata=None, *args, **kwargs):
        if formdata is None:
            formdata = request.args.copy()

        super(CanonSearchForm, self).__init__(formdata, *args, **kwargs)

    @classmethod
    def query(cls):
        query = CanonItem.query.order_by(CanonItem.title)

        if not has_group('editor'):
            query = query.filter(db.not_(CanonItem.draft))

        return query

    def apply(self, query=None):
        self.validate()
        query = query if query is not None else self.query()

        if not self.q.data:
            return query

        tags = []
        terms = []

        for token in self.q.data.split():
            if token.startswith('[') and token.endswith(']'):
                tags.append(token[1:-1])
            elif token.startswith('is:'):
                flag = token[3:]

                if flag == 'draft':
                    query = query.filter(CanonItem.draft)
                elif flag == 'community':
                    query = query.filter(CanonItem.community)
            else:
                terms.append(token)

        if tags:
            tag_q = db.session.query(db.func.unnest(tags).label('name')).subquery()
            tag_count = db.session.query(CanonItem.id, db.func.count(CanonItem.id).label('tags')
            ).join(CanonItem._tags).filter(Tag.name.in_(tag_q)
            ).group_by(CanonItem.id).subquery()

            query = query.join((tag_count, tag_count.c.id == CanonItem.id)).filter(tag_count.c.tags >= len(tags))

        if terms:
            tsvector = db.func.to_tsvector('english', (CanonItem.title + ' ' + CanonItem.excerpt + ' ' + CanonItem.body))
            tsquery = ' & '.join(terms)
            query = query.filter(tsvector.match(tsquery, postgresql_regconfig='english'))

        return query
