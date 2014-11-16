"""add profile link

Revision ID: 2eb4ce026c3
Revises: 316b5c044f3
Create Date: 2014-11-16 11:49:38.302856
"""

# revision identifiers, used by Alembic.
revision = '2eb4ce026c3'
down_revision = '316b5c044f3'

import click
from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import Session


def upgrade():
    from sopy.se_data.models import SEUser

    session = Session(bind=op.get_bind())
    op.add_column('se_user', sa.Column('profile_link', sa.String))

    with click.progressbar(
        session.query(SEUser).all(),
        label='Updating user data'
    ) as bar:
        for user in bar:
            user.se_update()

    session.query(SEUser).filter_by(profile_link=None).update({'profile_link': ''})

    session.commit()

    op.alter_column('se_user', 'profile_link', nullable=False)


def downgrade():
    op.drop_column('se_user', 'profile_link')
