"""group hierarchy

Revision ID: 1914e1c7a03
Revises: 1f5a6a1a28c
Create Date: 2014-09-05 09:39:23.213989
"""

# revision identifiers, used by Alembic.
revision = '1914e1c7a03'
down_revision = '1f5a6a1a28c'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('group_group',
        sa.Column('member_id', sa.Integer, sa.ForeignKey('group.id'), primary_key=True),
        sa.Column('group_id', sa.Integer, sa.ForeignKey('group.id'), primary_key=True)
    )


def downgrade():
    op.drop_table('group_group')
