"""rename approved

Revision ID: 316b5c044f3
Revises: 415ea570c2c
Create Date: 2014-09-05 19:36:39.123795
"""

# revision identifiers, used by Alembic.
revision = '316b5c044f3'
down_revision = '415ea570c2c'

from alembic import op
from flask_sqlalchemy import _SessionSignalEvents
import sqlalchemy as sa
from sqlalchemy import event, exc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, relationship

try:
    event.remove(Session, 'before_commit', _SessionSignalEvents.session_signal_before_commit)
    event.remove(Session, 'after_commit', _SessionSignalEvents.session_signal_after_commit)
    event.remove(Session, 'after_rollback', _SessionSignalEvents.session_signal_after_rollback)
except exc.InvalidRequestError:
    pass

Base = declarative_base()


class Group(Base):
    __tablename__ = 'group'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String)


def upgrade():
    op.execute("""update "group" set "name" = 'Dark Council' where "name" = 'approved'""")


def downgrade():
    op.execute("""update "group" set "name" = 'approved' where "name" = 'Dark Council'""")
