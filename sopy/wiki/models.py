from datetime import datetime
from flask import url_for
from sopy import db
from sopy.auth.models import User
from sopy.ext.models import IDModel


class WikiPage(IDModel):
    title = db.Column(db.String, nullable=False)
    body = db.Column(db.String, nullable=False)
    updated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)

    author = db.relationship(User)

    @property
    def detail_url(self):
        return url_for('wiki.detail', id=self.id)

    @property
    def update_url(self):
        return url_for('wiki.update', id=self.id)

    @property
    def delete_url(self):
        return url_for('wiki.delete', id=self.id)
