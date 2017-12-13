"""record user

Revision ID: 4afdfb8648
Revises: 1377a5a0097
Create Date: 2014-07-20 20:50:41.570783
"""

# revision identifiers, used by Alembic.
revision = '4afdfb8648'
down_revision = '1377a5a0097'

import sqlalchemy as sa
from alembic import op
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

Base = declarative_base()


class CanonItem(Base):
    __tablename__ = 'canon_item'

    id = sa.Column(sa.Integer, primary_key=True)
    updated_by_id = sa.Column(sa.Integer)


class Salad(Base):
    __tablename__ = 'salad'

    id = sa.Column(sa.Integer, primary_key=True)
    updated_by_id = sa.Column(sa.Integer)


class WikiPage(Base):
    __tablename__ = 'wiki_page'

    id = sa.Column(sa.Integer, primary_key=True)
    author_id = sa.Column(sa.Integer)


def upgrade():
    session = Session(bind=op.get_bind())

    op.add_column('canon_item', sa.Column('updated_by_id', sa.Integer, sa.ForeignKey('user.id')))
    op.add_column('salad', sa.Column('updated_by_id', sa.Integer, sa.ForeignKey('user.id')))
    op.add_column('wiki_page', sa.Column('author_id', sa.Integer, sa.ForeignKey('user.id')))

    session.query(CanonItem).update({'updated_by_id': -1})
    session.query(Salad).update({'updated_by_id': -1})
    session.query(WikiPage).update({'author_id': -1})
    session.commit()

    op.alter_column('canon_item', 'updated_by_id', nullable=False)
    op.alter_column('salad', 'updated_by_id', nullable=False)
    op.alter_column('wiki_page', 'author_id', nullable=False)


def downgrade():
    op.drop_column('wiki_page', 'author_id')
    op.drop_column('salad', 'updated_by_id')
    op.drop_column('canon_item', 'updated_by_id')
