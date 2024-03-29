"""empty message

Revision ID: a0b037f7a26f
Revises: 
Create Date: 2019-11-20 00:26:00.298574

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a0b037f7a26f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'response_time')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('response_time', sa.INTEGER(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
