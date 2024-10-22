"""add last few columns to posts table

Revision ID: 0838c245588d
Revises: 2781867152bb
Create Date: 2024-10-22 11:02:13.221812

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0838c245588d'
down_revision: Union[str, None] = '2781867152bb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() :
    op.add_column('posts', sa.Column(
        'published', sa.Boolean(), nullable=False, server_default='TRUE'),)
    op.add_column('posts', sa.Column(
        'created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')),)
    pass


def downgrade() :
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
