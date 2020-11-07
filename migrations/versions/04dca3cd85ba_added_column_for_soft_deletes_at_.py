"""Added column for soft-deletes at ArcticSun model

Revision ID: 04dca3cd85ba
Revises: 37e3a9361efb
Create Date: 2020-11-07 15:14:45.318931

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '04dca3cd85ba'
down_revision = '37e3a9361efb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('arctic_sun', sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('arctic_sun', 'deleted_at')
    # ### end Alembic commands ###