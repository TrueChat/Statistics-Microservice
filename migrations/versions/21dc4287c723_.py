"""empty message

Revision ID: 21dc4287c723
Revises: 
Create Date: 2019-11-22 01:18:00.412065

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '21dc4287c723'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), autoincrement=False, nullable=False),
    sa.Column('update_time', sa.DateTime(), nullable=False),
    sa.Column('chats_num', sa.Integer(), nullable=True),
    sa.Column('dialogs_num', sa.Integer(), nullable=True),
    sa.Column('groups_num', sa.Integer(), nullable=True),
    sa.Column('days_with', sa.Integer(), nullable=True),
    sa.Column('mess_num', sa.Integer(), nullable=True),
    sa.Column('words_num', sa.Integer(), nullable=True),
    sa.Column('chars_num', sa.Integer(), nullable=True),
    sa.Column('active_period', sa.String(length=100), nullable=True),
    sa.Column('act_mess_num', sa.Integer(), nullable=True),
    sa.Column('act_words_num', sa.Integer(), nullable=True),
    sa.Column('act_chars_num', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('word',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('word', sa.String(length=200), nullable=True),
    sa.Column('count', sa.Integer(), nullable=False),
    sa.Column('entity_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['entity_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('word')
    op.drop_table('user')
    # ### end Alembic commands ###
