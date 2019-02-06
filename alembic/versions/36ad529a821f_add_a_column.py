"""Add a column

Revision ID: 36ad529a821f
Revises: 
Create Date: 2019-01-03 11:40:59.005550

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '36ad529a821f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('user', sa.Column('rank', sa.Integer))

def downgrade():
    op.drop_column('user', 'rank')
    