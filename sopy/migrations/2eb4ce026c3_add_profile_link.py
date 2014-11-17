"""add profile link

Revision ID: 2eb4ce026c3
Revises: 316b5c044f3
Create Date: 2014-11-16 11:49:38.302856
"""

# revision identifiers, used by Alembic.
revision = '2eb4ce026c3'
down_revision = '316b5c044f3'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('se_user', sa.Column('profile_link', sa.String))
    op.execute("update se_user set profile_link = ''")
    op.alter_column('se_user', 'profile_link', nullable=False)


def downgrade():
    op.drop_column('se_user', 'profile_link')
