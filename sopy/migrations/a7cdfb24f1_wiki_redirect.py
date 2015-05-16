"""wiki redirect

Revision ID: a7cdfb24f1
Revises: 54a3343a03b
Create Date: 2015-05-16 09:43:45.455535
"""

from alembic import op
import sqlalchemy as sa


revision = 'a7cdfb24f1'
down_revision = '54a3343a03b'
branch_labels = ()
depends_on = None


def upgrade():
    op.add_column('wiki_page', sa.Column('redirect_id', sa.Integer(), nullable=True))
    op.create_unique_constraint(op.f('uq_wiki_page_title'), 'wiki_page', ['title'])
    op.create_foreign_key(op.f('fk_wiki_page_redirect_id_wiki_page'), 'wiki_page', 'wiki_page', ['redirect_id'], ['id'])


def downgrade():
    op.drop_constraint(op.f('fk_wiki_page_redirect_id_wiki_page'), 'wiki_page', type_='foreignkey')
    op.drop_constraint(op.f('uq_wiki_page_title'), 'wiki_page', type_='unique')
    op.drop_column('wiki_page', 'redirect_id')
