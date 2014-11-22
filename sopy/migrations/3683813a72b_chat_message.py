"""chat message

Revision ID: 3683813a72b
Revises: 3d0b280fd95
Create Date: 2014-11-23 09:20:21.790170
"""

# revision identifiers, used by Alembic.
revision = '3683813a72b'
down_revision = '3d0b280fd95'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'chat_message',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=False),
        sa.Column('room_id', sa.Integer, nullable=False),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('se_user.id'), nullable=False),
        sa.Column('ts', sa.DateTime, nullable=False),
        sa.Column('content', sa.String, nullable=False),
        sa.Column('rendered', sa.Boolean, nullable=False),
        sa.Column('stars', sa.Integer, nullable=False)
    )


def downgrade():
    op.drop_table('chat_message')
