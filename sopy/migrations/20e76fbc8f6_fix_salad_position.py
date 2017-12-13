"""fix salad position

Revision ID: 20e76fbc8f6
Revises: 4afdfb8648
Create Date: 2014-07-21 22:06:44.827834
"""

# revision identifiers, used by Alembic.
revision = '20e76fbc8f6'
down_revision = '4afdfb8648'

import sqlalchemy as sa
from alembic import op
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

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
