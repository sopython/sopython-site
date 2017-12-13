"""squash

Revision ID: 1051
Revises:
Create Date: 2017-12-13 13:17:31.742850
"""

from alembic import op
import sqlalchemy as sa


revision = '1051'
down_revision = None
branch_labels = ('default',)
depends_on = None


def upgrade():
    op.create_table('group',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_group')),
    sa.UniqueConstraint('name', name=op.f('uq_group_name'))
    )
    op.create_table('se_question',
    sa.Column('id', sa.Integer(), autoincrement=False, nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('body', sa.String(), nullable=False),
    sa.Column('link', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_se_question'))
    )
    op.create_table('se_user',
    sa.Column('id', sa.Integer(), autoincrement=False, nullable=False),
    sa.Column('display_name', sa.String(), nullable=False),
    sa.Column('profile_image', sa.String(), nullable=False),
    sa.Column('profile_link', sa.String(), nullable=False),
    sa.Column('reputation', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_se_user'))
    )
    op.create_table('tag',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_tag')),
    sa.UniqueConstraint('name', name=op.f('uq_tag_name'))
    )
    op.create_table('transcript',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('ts', sa.DateTime(), nullable=False),
    sa.Column('body', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_transcript'))
    )
    op.create_table('chat_message',
    sa.Column('id', sa.Integer(), autoincrement=False, nullable=False),
    sa.Column('room_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('ts', sa.DateTime(), nullable=False),
    sa.Column('content', sa.String(), nullable=False),
    sa.Column('rendered', sa.Boolean(), nullable=False),
    sa.Column('stars', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['se_user.id'], name=op.f('fk_chat_message_user_id_se_user')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_chat_message'))
    )
    op.create_table('group_group',
    sa.Column('member_id', sa.Integer(), nullable=False),
    sa.Column('group_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['group_id'], ['group.id'], name=op.f('fk_group_group_group_id_group')),
    sa.ForeignKeyConstraint(['member_id'], ['group.id'], name=op.f('fk_group_group_member_id_group')),
    sa.PrimaryKeyConstraint('member_id', 'group_id', name=op.f('pk_group_group'))
    )
    op.create_table('se_question_tag',
    sa.Column('se_question_id', sa.Integer(), nullable=False),
    sa.Column('tag_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['se_question_id'], ['se_question.id'], name=op.f('fk_se_question_tag_se_question_id_se_question')),
    sa.ForeignKeyConstraint(['tag_id'], ['tag.id'], name=op.f('fk_se_question_tag_tag_id_tag')),
    sa.PrimaryKeyConstraint('se_question_id', 'tag_id', name=op.f('pk_se_question_tag'))
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('superuser', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['id'], ['se_user.id'], name=op.f('fk_user_id_se_user')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_user'))
    )
    op.create_table('canon_item',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('excerpt', sa.String(), nullable=False),
    sa.Column('body', sa.String(), nullable=False),
    sa.Column('draft', sa.Boolean(), nullable=False),
    sa.Column('community', sa.Boolean(), nullable=False),
    sa.Column('updated_by_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['updated_by_id'], ['user.id'], name=op.f('fk_canon_item_updated_by_id_user')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_canon_item'))
    )
    op.create_table('salad',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('term', sa.String(), nullable=False),
    sa.Column('definition', sa.String(), nullable=False),
    sa.Column('position', sa.Integer(), nullable=False),
    sa.Column('updated_by_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['updated_by_id'], ['user.id'], name=op.f('fk_salad_updated_by_id_user')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_salad')),
    sa.UniqueConstraint('term', name=op.f('uq_salad_term'))
    )
    op.create_table('transcript_message',
    sa.Column('transcript_id', sa.Integer(), nullable=False),
    sa.Column('message_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['message_id'], ['chat_message.id'], name=op.f('fk_transcript_message_message_id_chat_message')),
    sa.ForeignKeyConstraint(['transcript_id'], ['transcript.id'], name=op.f('fk_transcript_message_transcript_id_transcript')),
    sa.PrimaryKeyConstraint('transcript_id', 'message_id', name=op.f('pk_transcript_message'))
    )
    op.create_table('user_group',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('group_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['group_id'], ['group.id'], name=op.f('fk_user_group_group_id_group')),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name=op.f('fk_user_group_user_id_user')),
    sa.PrimaryKeyConstraint('user_id', 'group_id', name=op.f('pk_user_group'))
    )
    op.create_table('wiki_page',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('body', sa.String(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.Column('draft', sa.Boolean(), nullable=False),
    sa.Column('community', sa.Boolean(), nullable=False),
    sa.Column('author_id', sa.Integer(), nullable=False),
    sa.Column('redirect_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['user.id'], name=op.f('fk_wiki_page_author_id_user')),
    sa.ForeignKeyConstraint(['redirect_id'], ['wiki_page.id'], name=op.f('fk_wiki_page_redirect_id_wiki_page')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_wiki_page')),
    sa.UniqueConstraint('title', name=op.f('uq_wiki_page_title'))
    )
    op.create_table('canon_item_se_question',
    sa.Column('canon_item_id', sa.Integer(), nullable=False),
    sa.Column('se_question_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['canon_item_id'], ['canon_item.id'], name=op.f('fk_canon_item_se_question_canon_item_id_canon_item')),
    sa.ForeignKeyConstraint(['se_question_id'], ['se_question.id'], name=op.f('fk_canon_item_se_question_se_question_id_se_question')),
    sa.PrimaryKeyConstraint('canon_item_id', 'se_question_id', name=op.f('pk_canon_item_se_question'))
    )
    op.create_table('canon_item_tag',
    sa.Column('canon_item_id', sa.Integer(), nullable=False),
    sa.Column('tag_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['canon_item_id'], ['canon_item.id'], name=op.f('fk_canon_item_tag_canon_item_id_canon_item')),
    sa.ForeignKeyConstraint(['tag_id'], ['tag.id'], name=op.f('fk_canon_item_tag_tag_id_tag')),
    sa.PrimaryKeyConstraint('canon_item_id', 'tag_id', name=op.f('pk_canon_item_tag'))
    )


def downgrade():
    op.drop_table('canon_item_tag')
    op.drop_table('canon_item_se_question')
    op.drop_table('wiki_page')
    op.drop_table('user_group')
    op.drop_table('transcript_message')
    op.drop_table('salad')
    op.drop_table('canon_item')
    op.drop_table('user')
    op.drop_table('se_question_tag')
    op.drop_table('group_group')
    op.drop_table('chat_message')
    op.drop_table('transcript')
    op.drop_table('tag')
    op.drop_table('se_user')
    op.drop_table('se_question')
    op.drop_table('group')
