from flask import url_for
from sopy import db
from sopy.ext.models import IDModel
from sopy.se_data.models import ChatMessage


class Transcript(IDModel):
    title = db.Column(db.String, nullable=False)
    ts = db.Column(db.DateTime, nullable=False)
    body = db.Column(db.String, nullable=False, default='')

    messages = db.relationship(ChatMessage, lambda: transcript_message, order_by=ChatMessage.id, cascade='all')

    def __str__(self):
        return self.title

    @property
    def detail_url(self):
        return url_for('transcript.detail', id=self)

    @property
    def update_url(self):
        return url_for('transcript.update', id=self.id)

    @property
    def delete_url(self):
        return url_for('transcript.delete', id=self.id)


transcript_message = db.Table(
    'transcript_message',
    db.Column('transcript_id', db.Integer, db.ForeignKey(Transcript.id), primary_key=True),
    db.Column('message_id', db.Integer, db.ForeignKey(ChatMessage.id), primary_key=True)
)
