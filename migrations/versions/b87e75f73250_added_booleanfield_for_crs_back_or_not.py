"""added booleanfield for CRS; back or not

Revision ID: b87e75f73250
Revises: 088060656eec
Create Date: 2021-01-28 17:57:44.854207

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "b87e75f73250"
down_revision = "088060656eec"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "arctic_sun", sa.Column("returned_from_crs", sa.Boolean(), nullable=True)
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("arctic_sun", "returned_from_crs")
    # ### end Alembic commands ###
