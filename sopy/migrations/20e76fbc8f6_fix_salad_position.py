"""fix salad position

Revision ID: 20e76fbc8f6
Revises: 4afdfb8648
Create Date: 2014-07-21 22:06:44.827834
"""

# revision identifiers, used by Alembic.
revision = '20e76fbc8f6'
down_revision = '4afdfb8648'

from alembic import op
from flask_sqlalchemy import _SessionSignalEvents
import sqlalchemy as sa
from sqlalchemy import event, exc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

try:
    event.remove(Session, 'before_commit', _SessionSignalEvents.session_signal_before_commit)
    event.remove(Session, 'after_commit', _SessionSignalEvents.session_signal_after_commit)
    event.remove(Session, 'after_rollback', _SessionSignalEvents.session_signal_after_rollback)
except exc.InvalidRequestError:
    pass

Base = declarative_base()


class Salad(Base):
    __tablename__ = 'salad'

    id = sa.Column(sa.Integer, primary_key=True)
    position = sa.Column(sa.Integer)


def upgrade():
    session = Session(bind=op.get_bind())

    for i, item in enumerate(session.query(Salad).order_by(Salad.position)):
        item.position = i

    session.commit()


def downgrade():
    pass
