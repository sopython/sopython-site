"""add user rep

Revision ID: 3d0b280fd95
Revises: 49df2c8cbe4
Create Date: 2014-11-16 17:29:56.729439
"""

# revision identifiers, used by Alembic.
revision = '3d0b280fd95'
down_revision = '49df2c8cbe4'

import click
from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import Session


def upgrade():
    from sopy.se_data.models import SEUser

    session = Session(bind=op.get_bind())
    op.add_column('se_user', sa.Column('reputation', sa.Integer))

    with click.progressbar(
        session.query(SEUser).all(),
        label='Updating user data'
    ) as bar:
        for user in bar:
            user.se_update()

    session.query(SEUser).filter_by(reputation=None).update({'reputation': 1})
    session.commit()
    op.alter_column('se_user', 'reputation', nullable=False)


def downgrade():
    op.drop_column('se_user', 'profile_link')
