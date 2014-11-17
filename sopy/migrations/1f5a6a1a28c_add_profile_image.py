"""add profile_image

Revision ID: 1f5a6a1a28c
Revises: 20e76fbc8f6
Create Date: 2014-08-22 11:15:57.345984
"""

# revision identifiers, used by Alembic.
revision = '1f5a6a1a28c'
down_revision = '20e76fbc8f6'

import click
from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import Session


def upgrade():
    from sopy.se_data.models import SEUser

    session = Session(bind=op.get_bind())
    op.add_column('se_user', sa.Column('profile_image', sa.String))

    with click.progressbar(
        session.query(SEUser).all(),
        label='Updating user data'
    ) as bar:
        for user in bar:
            user.se_update()

    session.query(SEUser).filter_by(profile_image=None).update({'profile_image': ''})
    session.commit()
    op.alter_column('se_user', 'profile_image', nullable=False)


def downgrade():
    op.drop_column('se_user', 'profile_image')
