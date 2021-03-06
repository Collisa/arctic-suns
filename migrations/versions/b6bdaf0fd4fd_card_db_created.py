"""Card db created

Revision ID: b6bdaf0fd4fd
Revises: d39db9f16f81
Create Date: 2020-08-24 19:49:08.248024

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b6bdaf0fd4fd'
down_revision = 'd39db9f16f81'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('card',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('card', sa.String(length=25), nullable=True),
    sa.Column('date_out', sa.Date(), nullable=True),
    sa.Column('date_retour', sa.Date(), nullable=True),
    sa.Column('chauffeur', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('card')
    # ### end Alembic commands ###
