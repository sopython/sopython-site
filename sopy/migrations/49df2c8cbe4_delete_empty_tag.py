"""delete empty tag

Revision ID: 49df2c8cbe4
Revises: 2eb4ce026c3
Create Date: 2014-11-16 17:16:54.536438
"""

# revision identifiers, used by Alembic.
revision = '49df2c8cbe4'
down_revision = '2eb4ce026c3'

from alembic import op
from sqlalchemy.orm import Session


def upgrade():
    from sopy.canon.models import CanonItem
    from sopy.tags.models import Tag

    session = Session(bind=op.get_bind())

    for item in session.query(CanonItem).join(CanonItem._tags).filter(Tag.name == ''):
        item.tags.discard('')

    empty_tag = session.query(Tag).filter_by(name='').one()
    session.delete(empty_tag)
    session.commit()

def downgrade():
    pass
