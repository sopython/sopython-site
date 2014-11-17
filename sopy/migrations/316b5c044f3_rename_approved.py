"""rename approved

Revision ID: 316b5c044f3
Revises: 415ea570c2c
Create Date: 2014-09-05 19:36:39.123795
"""

# revision identifiers, used by Alembic.
revision = '316b5c044f3'
down_revision = '415ea570c2c'

from alembic import op

def upgrade():
    op.execute("""update "group" set "name" = 'Dark Council' where "name" = 'approved'""")


def downgrade():
    op.execute("""update "group" set "name" = 'approved' where "name" = 'Dark Council'""")
