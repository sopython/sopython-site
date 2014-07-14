"""basic

Revision ID: 2fe56c1c437
Revises: None
Create Date: 2014-07-06 14:14:04.306753

"""

# revision identifiers, used by Alembic.
revision = '2fe56c1c437'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'tag',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String, nullable=False, unique=True)
    )
    op.create_table(
        'so_question',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=False),
        sa.Column('title', sa.String, nullable=False),
        sa.Column('body', sa.String, nullable=False)
    )
    op.create_table(
        'so_question_tag',
        sa.Column('so_question_id', sa.Integer, sa.ForeignKey('so_question.id'), primary_key=True),
        sa.Column('tag_id', sa.Integer, sa.ForeignKey('tag.id'), primary_key=True)
    )
    op.create_table(
        'canon_item',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('title', sa.String, nullable=False),
        sa.Column('excerpt', sa.String, nullable=False),
        sa.Column('body', sa.String, nullable=False)
    )
    op.create_table(
        'canon_item_tag',
        sa.Column('canon_item_id', sa.Integer, sa.ForeignKey('canon_item.id'), primary_key=True),
        sa.Column('tag_id', sa.Integer, sa.ForeignKey('tag.id'), primary_key=True)
    )
    op.create_table(
        'canon_item_so_question',
        sa.Column('canon_item_id', sa.Integer, sa.ForeignKey('canon_item.id'), primary_key=True),
        sa.Column('so_question_id', sa.Integer, sa.ForeignKey('so_question.id'), primary_key=True)
    )


def downgrade():
    op.drop_table('canon_item_so_question')
    op.drop_table('canon_item_tag')
    op.drop_table('canon_item')
    op.drop_table('so_question_tag')
    op.drop_table('so_question')
    op.drop_table('tag')
