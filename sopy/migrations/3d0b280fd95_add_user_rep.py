"""add user rep

Revision ID: 3d0b280fd95
Revises: 49df2c8cbe4
Create Date: 2014-11-16 17:29:56.729439
"""

# revision identifiers, used by Alembic.
revision = '3d0b280fd95'
down_revision = '49df2c8cbe4'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('se_user', sa.Column('reputation', sa.Integer))
    op.execute('update se_user set reputation = 1')
    op.alter_column('se_user', 'reputation', nullable=False)


def downgrade():
    op.drop_column('se_user', 'profile_link')
