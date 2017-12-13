"""community user

Revision ID: 1377a5a0097
Revises: 370524b8221
Create Date: 2014-07-20 20:36:17.716616
"""

# revision identifiers, used by Alembic.
revision = '1377a5a0097'
down_revision = '370524b8221'

from alembic import op
from flask_sqlalchemy import _SessionSignalEvents
import sqlalchemy as sa
from sqlalchemy import event, exc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

Base = declarative_base()


class Group(Base):
    __tablename__ = 'group'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String)


class SEUser(Base):
    __tablename__ = 'se_user'

    id = sa.Column(sa.Integer, primary_key=True)
    display_name = sa.Column(sa.String)


class User(SEUser):
    __tablename__ = 'user'

    id = sa.Column(sa.Integer, sa.ForeignKey(SEUser.id), primary_key=True)
    superuser = sa.Column(sa.Boolean, default=False)


def upgrade():
    session = Session(bind=op.get_bind())

    if session.query(User).get(-1) is None:
        session.add(User(id=-1, display_name='Community'))

    if session.query(Group).filter_by(name='approved').first() is None:
        session.add(Group(name='approved'))

    session.commit()


def downgrade():
    pass
