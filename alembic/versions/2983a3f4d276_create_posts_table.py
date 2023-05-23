"""create posts table

Revision ID: 2983a3f4d276
Revises: 
Create Date: 2023-05-19 14:53:03.060308

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2983a3f4d276'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
     op.create_table('emails', sa.Column('id', sa.Integer(),  primary_key=True, index= True), sa.Column('email',sa.String(), nullable=False, unique=True))
     pass

def downgrade() -> None:
    op.drop_table('emails')
    pass
