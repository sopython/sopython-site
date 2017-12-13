"""editor group

Revision ID: 415ea570c2c
Revises: 1914e1c7a03
Create Date: 2014-09-05 16:20:08.585269
"""

# revision identifiers, used by Alembic.
revision = '415ea570c2c'
down_revision = '1914e1c7a03'

import sqlalchemy as sa
from alembic import op
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, relationship

Base = declarative_base()


class Group(Base):
    __tablename__ = 'group'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String)

    groups = relationship(
        'Group', 'group_group',
        primaryjoin='Group.id == group_group.c.member_id',
        secondaryjoin='Group.id == group_group.c.group_id',
        backref='members'
    )


group_group = sa.Table(
    'group_group', Base.metadata,
    sa.Column('member_id', sa.Integer, sa.ForeignKey('group.id'), primary_key=True),
    sa.Column('group_id', sa.Integer, sa.ForeignKey('group.id'), primary_key=True)
)


class CanonItem(Base):
    __tablename__ = 'canon_item'

    id = sa.Column(sa.Integer, primary_key=True)
    draft = sa.Column(sa.Boolean)
    community = sa.Column(sa.Boolean)


class WikiPage(Base):
    __tablename__ = 'wiki_page'

    id = sa.Column(sa.Integer, primary_key=True)
    draft = sa.Column(sa.Boolean)
    community = sa.Column(sa.Boolean)


def upgrade():
    op.add_column('canon_item', sa.Column('draft', sa.Boolean))
    op.add_column('canon_item', sa.Column('community', sa.Boolean))
    op.add_column('wiki_page', sa.Column('draft', sa.Boolean))
    op.add_column('wiki_page', sa.Column('community', sa.Boolean))

    session = Session(bind=op.get_bind())
    session.query(CanonItem).update({'draft': False, 'community': False})
    session.query(WikiPage).update({'draft': False, 'community': False})
    session.commit()

    op.alter_column('canon_item', 'draft', nullable=False)
    op.alter_column('canon_item', 'community', nullable=False)
    op.alter_column('wiki_page', 'draft', nullable=False)
    op.alter_column('wiki_page', 'community', nullable=False)

    approved = session.query(Group).filter_by(name='approved').one()
    approved.groups.append(Group(name='editor'))
    session.commit()


def downgrade():
    session = Session(bind=op.get_bind())
    session.delete(session.query(Group).filter_by(name='editor').one())
    session.commit()

    op.drop_column('wiki_page', 'community')
    op.drop_column('wiki_page', 'draft')
    op.drop_column('canon_item', 'community')
    op.drop_column('canon_item', 'draft')
