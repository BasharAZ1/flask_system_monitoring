"""init db

Revision ID: e9a415bca996
Revises: 
Create Date: 2024-02-08 15:43:09.742938

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e9a415bca996'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('active_processes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('measurement_time', sa.String(length=50), nullable=False),
    sa.Column('pid', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('status', sa.String(length=50), nullable=False),
    sa.Column('start_date', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('measurement_time'),
    sa.UniqueConstraint('name'),
    sa.UniqueConstraint('pid')
    )
    op.create_table('cpu',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('measurement_time', sa.String(length=50), nullable=False),
    sa.Column('times_user', sa.Float(), nullable=False),
    sa.Column('times_system', sa.Float(), nullable=False),
    sa.Column('times_idle', sa.Float(), nullable=False),
    sa.Column('usage_percent', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('measurement_time')
    )
    op.create_table('disk',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('measurement_time', sa.String(length=50), nullable=False),
    sa.Column('used', sa.Integer(), nullable=False),
    sa.Column('free', sa.Integer(), nullable=False),
    sa.Column('usage_percent', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('measurement_time')
    )
    op.create_table('memory',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('measurement_time', sa.String(length=50), nullable=False),
    sa.Column('used', sa.Integer(), nullable=False),
    sa.Column('active', sa.Integer(), nullable=False),
    sa.Column('inactive', sa.Integer(), nullable=False),
    sa.Column('usage_percent', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('measurement_time')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('memory')
    op.drop_table('disk')
    op.drop_table('cpu')
    op.drop_table('active_processes')
    # ### end Alembic commands ###
