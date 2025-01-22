"""feat: create table request

Revision ID: 48177af17256
Revises: e328607b2eea
Create Date: 2025-01-21 20:59:56.142867

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '48177af17256'
down_revision: Union[str, None] = 'e328607b2eea'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('request',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_donation', sa.Integer(), nullable=False),
    sa.Column('id_giver', sa.Integer(), nullable=False),
    sa.Column('id_receiver', sa.Integer(), nullable=False),
    sa.Column('item', sa.String(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('order_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.ForeignKeyConstraint(['id_donation'], ['donation.id'], ),
    sa.ForeignKeyConstraint(['id_giver'], ['donation.id_user'], ),
    sa.ForeignKeyConstraint(['id_receiver'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('request')
    # ### end Alembic commands ###
