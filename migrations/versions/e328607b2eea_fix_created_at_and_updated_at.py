"""fix: created_at and updated_at

Revision ID: e328607b2eea
Revises: d8b327992664
Create Date: 2025-01-21 19:02:21.970920

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e328607b2eea'
down_revision: Union[str, None] = 'd8b327992664'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('donation', sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False))
    op.add_column('donation', sa.Column('updated_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('donation', 'updated_at')
    op.drop_column('donation', 'created_at')
    # ### end Alembic commands ###
