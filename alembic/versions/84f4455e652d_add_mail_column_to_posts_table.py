"""add mail column to posts table

Revision ID: 84f4455e652d
Revises: f5a54d92877c
Create Date: 2024-10-22 10:52:38.017255

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '84f4455e652d'
down_revision: Union[str, None] = 'f5a54d92877c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts', sa.Column('mail', sa.String(), nullable=False))
    pass


def downgrade() :
    op.drop_column('posts', 'mail')
    pass
