"""transcript

Revision ID: 54a3343a03b
Revises: 3683813a72b
Create Date: 2014-11-24 23:42:50.112415
"""

# revision identifiers, used by Alembic.
revision = '54a3343a03b'
down_revision = '3683813a72b'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'transcript',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('title', sa.String, nullable=False),
        sa.Column('ts', sa.DateTime, nullable=False),
        sa.Column('body', sa.String, nullable=False)
    )
    op.create_table(
        'transcript_message',
        sa.Column('transcript_id', sa.Integer, sa.ForeignKey('transcript.id'), primary_key=True),
        sa.Column('message_id', sa.Integer, sa.ForeignKey('chat_message.id'), primary_key=True)
    )


def downgrade():
    op.drop_table('transcript_message')
    op.drop_table('transcript')
