"""auth

Revision ID: 14aa0a5af3a
Revises: 2345d75e84a
Create Date: 2014-07-20 17:17:46.054226
"""

# revision identifiers, used by Alembic.
revision = '14aa0a5af3a'
down_revision = '2345d75e84a'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('so_user',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=False),
        sa.Column('display_name', sa.String, nullable=False)
    )
    op.create_table('group',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String, nullable=False, unique=True)
    )
    op.create_table('user',
        sa.Column('id', sa.Integer, sa.ForeignKey('so_user.id'), primary_key=True),
        sa.Column('superuser', sa.Boolean, nullable=False)
    )
    op.create_table('user_group',
        sa.Column('user_id', sa.Integer, sa.ForeignKey('user.id'), primary_key=True),
        sa.Column('group_id', sa.Integer, sa.ForeignKey('group.id'), primary_key=True)
    )


def downgrade():
    op.drop_table('user_group')
    op.drop_table('user')
    op.drop_table('group')
    op.drop_table('so_user')
