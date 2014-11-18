from sopy import db
from sopy.ext.models import IDModel
from sopy.se_data.models import ChatMessage


class Transcript(IDModel):
    title = db.Column(db.String, nullable=False)

    messages = db.relationship(ChatMessage, lambda: transcript_message, order_by=ChatMessage.id)

    def __str__(self):
        return self.title


transcript_message = db.Table(
    'transcript_message',
    db.Column('transcript_id', db.Integer, db.ForeignKey(Transcript.id), primary_key=True),
    db.Column('message_id', db.Integer, db.ForeignKey(ChatMessage.id), primary_key=True)
)
