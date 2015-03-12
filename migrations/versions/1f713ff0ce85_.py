"""empty message

Revision ID: 1f713ff0ce85
Revises: 24e7910e3b7
Create Date: 2015-03-12 18:53:00.468935

"""

# revision identifiers, used by Alembic.
revision = '1f713ff0ce85'
down_revision = '24e7910e3b7'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('losses', sa.Integer(), nullable=True))
    op.add_column('user', sa.Column('ties', sa.Integer(), nullable=True))
    op.add_column('user', sa.Column('total_played', sa.Integer(), nullable=True))
    op.add_column('user', sa.Column('wins', sa.Integer(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'wins')
    op.drop_column('user', 'total_played')
    op.drop_column('user', 'ties')
    op.drop_column('user', 'losses')
    ### end Alembic commands ###