"""salad position

Revision ID: 3171252a864
Revises: 5044846b1bc
Create Date: 2014-07-14 22:56:18.118214

"""

# revision identifiers, used by Alembic.
revision = '3171252a864'
down_revision = '5044846b1bc'

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
    term = sa.Column(sa.String)
    position = sa.Column(sa.Integer)


def upgrade():
    op.add_column('salad', sa.Column('position', sa.Integer))

    session = Session(bind=op.get_bind())

    for i, item in enumerate(session.query(Salad).order_by(Salad.term)):
        item.position = i

    session.commit()

    op.alter_column('salad', 'position', nullable=False)


def downgrade():
    op.drop_column('salad', 'position')
