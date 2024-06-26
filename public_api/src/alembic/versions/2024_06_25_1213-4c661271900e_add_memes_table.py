"""Add memes table

Revision ID: 4c661271900e
Revises: 
Create Date: 2024-06-25 12:13:35.659591

"""
import uuid
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4c661271900e'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'memes',
        sa.Column('id', sa.Uuid(), primary_key=True, default=uuid.uuid4),
        sa.Column('text', sa.Text(), nullable=False),
        sa.Column('img', sa.String(255), nullable=False),
        sa.Column('bucket', sa.String(10), nullable=False)
    )


def downgrade() -> None:
    op.drop_table('memes')

