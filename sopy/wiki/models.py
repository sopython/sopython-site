from datetime import datetime
from flask import url_for
from sopy import db
from sopy.auth.models import User
from sopy.ext.models import IDModel


class WikiPage(IDModel):
    title = db.Column('title', db.String, nullable=False, unique=True)
    body = db.Column(db.String, nullable=False)
    updated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    draft = db.Column(db.Boolean, nullable=False, default=False)
    community = db.Column(db.Boolean, nullable=False, default=False)
    author_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    redirect_id = db.Column(db.Integer, db.ForeignKey('wiki_page.id'))

    author = db.relationship(User)
    redirect = db.relationship(lambda: WikiPage, remote_side=lambda: (WikiPage.id,), backref='redirects')

    def __str__(self):
        return self.title

    @property
    def detail_url(self):
        return url_for('wiki.detail', title=self.title)

    @property
    def update_url(self):
        return url_for('wiki.update', title=self.title)

    @property
    def delete_url(self):
        return url_for('wiki.delete', title=self.title)
