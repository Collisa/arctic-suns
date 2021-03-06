"""db for hours added

Revision ID: c652ec160e90
Revises: b6bdaf0fd4fd
Create Date: 2020-09-12 13:57:26.118789

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c652ec160e90'
down_revision = 'b6bdaf0fd4fd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('employee',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('person_id', sa.Integer, nullable=False),
    sa.Column('workday', sa.Date(), nullable=True),
    sa.Column('start_hour', sa.Time(), nullable=True),
    sa.Column('end_hour', sa.Time(), nullable=True),
    sa.Column('type_day', sa.String(length=20), nullable=True),
    sa.Column('total_leave_days', sa.Integer(), nullable=True),
    sa.Column('extra_hours', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('employee')
    # ### end Alembic commands ###
