"""so to se

Revision ID: 370524b8221
Revises: 14aa0a5af3a
Create Date: 2014-07-20 18:02:42.992827
"""

# revision identifiers, used by Alembic.
revision = '370524b8221'
down_revision = '14aa0a5af3a'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.rename_table('so_user', 'se_user')
    op.rename_table('so_question', 'se_question')
    op.rename_table('so_question_tag', 'se_question_tag')
    op.rename_table('canon_item_so_question', 'canon_item_se_question')

    op.alter_column('se_question_tag', 'so_question_id', new_column_name='se_question_id')
    op.alter_column('canon_item_se_question', 'so_question_id', new_column_name='se_question_id')


def downgrade():
    op.rename_table('se_user', 'so_user')
    op.rename_table('se_question', 'so_question')
    op.rename_table('se_question_tag', 'so_question_tag')
    op.rename_table('canon_item_se_question', 'canon_item_so_question')

    op.alter_column('so_question_tag', 'se_question_id', new_column_name='so_question_id')
    op.alter_column('canon_item_so_question', 'se_question_id', new_column_name='so_question_id')
