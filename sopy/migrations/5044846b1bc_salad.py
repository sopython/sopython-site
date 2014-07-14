"""salad

Revision ID: 5044846b1bc
Revises: 2fe56c1c437
Create Date: 2014-07-14 11:38:07.161362

"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '5044846b1bc'
down_revision = '2fe56c1c437'


def upgrade():
    op.create_table('salad',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('term', sa.String, nullable=False, unique=True),
        sa.Column('definition', sa.String, nullable=False)
    )


def downgrade():
    op.drop_table('salad')
