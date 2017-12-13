"""rename constraints

Revision ID: 1532
Revises: 1051
Create Date: 2017-12-13 13:25:32.236544
"""

from alembic import op
import sqlalchemy as sa


revision = '1532'
down_revision = '1051'
branch_labels = ()
depends_on = None


def upgrade():
    op.create_unique_constraint(op.f('uq_group_name'), 'group', ['name'])
    op.drop_constraint('group_name_key', 'group', type_='unique')
    op.create_unique_constraint(op.f('uq_salad_term'), 'salad', ['term'])
    op.drop_constraint('salad_term_key', 'salad', type_='unique')
    op.create_unique_constraint(op.f('uq_tag_name'), 'tag', ['name'])
    op.drop_constraint('tag_name_key', 'tag', type_='unique')


def downgrade():
    op.create_unique_constraint('tag_name_key', 'tag', ['name'])
    op.drop_constraint(op.f('uq_tag_name'), 'tag', type_='unique')
    op.create_unique_constraint('salad_term_key', 'salad', ['term'])
    op.drop_constraint(op.f('uq_salad_term'), 'salad', type_='unique')
    op.create_unique_constraint('group_name_key', 'group', ['name'])
    op.drop_constraint(op.f('uq_group_name'), 'group', type_='unique')
