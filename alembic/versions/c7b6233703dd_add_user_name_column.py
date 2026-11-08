"""add user name column

Revision ID: c7b6233703dd
Revises: ed3a4ab6a3f3
Create Date: 2026-11-09 03:08:11.935000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c7b6233703dd'
down_revision: Union[str, Sequence[str], None] = 'ed3a4ab6a3f3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        'users',
        sa.Column(
            'name',
            sa.String(length=100),
            nullable=True,
            default=None,
        )
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('users', 'name')