from flask import url_for
from sopy import db
from sopy.ext.models import IDModel
from sopy.sodata.models import SOQuestion
from sopy.tags.models import HasTags


class CanonItem(HasTags, IDModel):
    title = db.Column(db.String, nullable=False)
    excerpt = db.Column(db.String, nullable=False, default='')
    body = db.Column(db.String, nullable=False, default='')

    def __str__(self):
        return self.title

    questions = db.relationship(SOQuestion, lambda: canon_item_so_question)

    @property
    def detail_url(self):
        return url_for('canon.detail', id=self.id)

    @property
    def update_url(self):
        return url_for('canon.update', id=self.id)

    @property
    def delete_url(self):
        return url_for('canon.delete', id=self.id)


canon_item_so_question = db.Table(
    'canon_item_so_question',
    db.Column('canon_item_id', db.Integer, db.ForeignKey(CanonItem.id), primary_key=True),
    db.Column('so_question_id', db.Integer, db.ForeignKey(SOQuestion.id), primary_key=True)
)
