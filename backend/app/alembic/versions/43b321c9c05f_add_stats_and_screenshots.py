"""add stats and screenshots

Revision ID: 43b321c9c05f
Revises: 03c6544d3bad
Create Date: 2021-03-02 00:29:56.043010

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '43b321c9c05f'
down_revision = '03c6544d3bad'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('run', sa.Column('stats', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('run', 'stats')
    # ### end Alembic commands ###
