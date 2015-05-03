"""empty message

Revision ID: 2ec39838e907
Revises: 4b6628c4d118
Create Date: 2015-04-30 15:43:56.403229

"""

# revision identifiers, used by Alembic.
revision = '2ec39838e907'
down_revision = '4b6628c4d118'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('event', sa.Column('host', sa.String(length=64), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('event', 'host')
    ### end Alembic commands ###