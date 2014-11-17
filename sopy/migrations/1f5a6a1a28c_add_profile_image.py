"""add profile_image

Revision ID: 1f5a6a1a28c
Revises: 20e76fbc8f6
Create Date: 2014-08-22 11:15:57.345984
"""

# revision identifiers, used by Alembic.
revision = '1f5a6a1a28c'
down_revision = '20e76fbc8f6'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('se_user', sa.Column('profile_image', sa.String))
    op.execute("update se_user set profile_image = ''")
    op.alter_column('se_user', 'profile_image', nullable=False)


def downgrade():
    op.drop_column('se_user', 'profile_image')
