"""wiki page

Revision ID: 2345d75e84a
Revises: 3171252a864
Create Date: 2014-07-17 08:48:29.503516
"""

# revision identifiers, used by Alembic.
revision = '2345d75e84a'
down_revision = '3171252a864'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'wiki_page',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('title', sa.String, nullable=False),
        sa.Column('body', sa.String, nullable=False),
        sa.Column('updated', sa.DateTime, nullable=False)
    )


def downgrade():
    op.drop_table('wiki_page')
