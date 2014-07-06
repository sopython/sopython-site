from sopy import db
from sopy.ext.models import IDModel
from sopy.sodata.models import SOQuestion
from sopy.tags.models import HasTags


class CanonItem(HasTags, IDModel):
    title = db.Column(db.String, nullable=False)
    body = db.Column(db.String, nullable=False, default='')

    questions = db.relationship(SOQuestion, lambda: canon_item_so_question)


canon_item_so_question = db.Table(
    'canon_item_so_question',
    db.Column('canon_item_id', db.Integer, db.ForeignKey(CanonItem.id), primary_key=True),
    db.Column('so_question_id', db.Integer, db.ForeignKey(SOQuestion.id), primary_key=True)
)
