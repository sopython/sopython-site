from sopy import db
from sopy.ext.models import ExternalIDModel
from sopy.tags.models import HasTags


class SOQuestion(HasTags, ExternalIDModel):
    title = db.Column(db.String, nullable=False)
    body = db.Column(db.String, nullable=False)
