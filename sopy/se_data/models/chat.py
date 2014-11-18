from sopy import db
from sopy.ext.models import IDModel
from sopy.se_data.models import SEUser


class ChatMessage(IDModel):
    user_id = db.Column(db.Integer, db.ForeignKey(SEUser.id), nullable=False)
    se_id = db.Column(db.Integer, nullable=False)
    ts = db.Column(db.DateTime, nullable=False)
    message = db.Column(db.String, nullable=False)

    user = db.relationship(SEUser, backref='chat_messages')
