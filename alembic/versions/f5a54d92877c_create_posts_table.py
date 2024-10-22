"""create posts table

Revision ID: f5a54d92877c
Revises: 
Create Date: 2024-10-22 10:19:39.371111

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f5a54d92877c'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() :
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False,
                    primary_key=True), sa.Column('name', sa.String(), nullable=False))
    pass


def downgrade() :
    op.drop_table('posts')
    pass
