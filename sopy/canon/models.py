from flask import url_for
from sqlalchemy.ext.associationproxy import association_proxy
from sopy import db
from sopy.auth.models import User
from sopy.ext.models import IDModel
from sopy.se_data.models import SEQuestion
from sopy.tags.models import HasTags


class CanonItem(HasTags, IDModel):
    title = db.Column(db.String, nullable=False)
    excerpt = db.Column(db.String, nullable=False, default='')
    body = db.Column(db.String, nullable=False, default='')
    updated_by_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)

    updated_by = db.relationship(User)

    def __str__(self):
        return self.title

    questions = db.relationship(SEQuestion, lambda: canon_item_se_question, collection_class=set)
    question_links = association_proxy('questions', 'link', creator=SEQuestion.se_load)

    @property
    def detail_url(self):
        return url_for('canon.detail', id=self.id)

    @property
    def update_url(self):
        return url_for('canon.update', id=self.id)

    @property
    def delete_url(self):
        return url_for('canon.delete', id=self.id)


canon_item_se_question = db.Table(
    'canon_item_se_question',
    db.Column('canon_item_id', db.Integer, db.ForeignKey(CanonItem.id), primary_key=True),
    db.Column('se_question_id', db.Integer, db.ForeignKey(SEQuestion.id), primary_key=True)
)
