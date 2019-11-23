"""empty message

Revision ID: d1fc4b26d584
Revises: baa287b60a89
Create Date: 2019-11-23 21:53:25.879375

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd1fc4b26d584'
down_revision = 'baa287b60a89'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('chat',
    sa.Column('id', sa.Integer(), autoincrement=False, nullable=False),
    sa.Column('update_time', sa.DateTime(), nullable=False),
    sa.Column('mess_num', sa.Integer(), nullable=True),
    sa.Column('users_num', sa.Integer(), nullable=True),
    sa.Column('days_exist', sa.Integer(), nullable=True),
    sa.Column('mean_mess_chars', sa.Float(), nullable=True),
    sa.Column('mean_mess_words', sa.Float(), nullable=True),
    sa.Column('act_users_num', sa.Integer(), nullable=True),
    sa.Column('afk_users_num', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('chat_member',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(length=200), nullable=True),
    sa.Column('mean_char', sa.Float(), nullable=True),
    sa.Column('mean_word', sa.Float(), nullable=True),
    sa.Column('num_mess', sa.Integer(), nullable=True),
    sa.Column('num_words', sa.Integer(), nullable=True),
    sa.Column('num_chars', sa.Integer(), nullable=True),
    sa.Column('percent', sa.Float(), nullable=True),
    sa.Column('days_in', sa.Integer(), nullable=True),
    sa.Column('entity_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['entity_id'], ['chat.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('chat_word',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('word', sa.String(length=200), nullable=True),
    sa.Column('count', sa.Integer(), nullable=False),
    sa.Column('entity_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['entity_id'], ['chat.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('chat_word')
    op.drop_table('chat_member')
    op.drop_table('chat')
    # ### end Alembic commands ###