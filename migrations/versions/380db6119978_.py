"""empty message

Revision ID: 380db6119978
Revises: 33bed37283a5
Create Date: 2015-05-04 00:49:51.435828

"""

# revision identifiers, used by Alembic.
revision = '380db6119978'
down_revision = '33bed37283a5'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('event', sa.Column('winner', sa.String(length=64), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('event', 'winner')
    ### end Alembic commands ###
