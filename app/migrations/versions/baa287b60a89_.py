"""empty message

Revision ID: baa287b60a89
Revises: a0b037f7a26f
Create Date: 2019-11-20 18:51:32.894932

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'baa287b60a89'
down_revision = 'a0b037f7a26f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('act_words_num', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'act_words_num')
    # ### end Alembic commands ###