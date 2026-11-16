"""add user preferences columns

Revision ID: f1a2b3c4d5e6
Revises: c7b6233703dd
Create Date: 2026-11-09 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f1a2b3c4d5e6'
down_revision = 'c7b6233703dd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Theme preference (light/dark/system)
    op.add_column(
        'users',
        sa.Column(
            'theme',
            sa.String(length=10),
            nullable=False,
            server_default='system',
        )
    )

    # Reminders enabled flag
    op.add_column(
        'users',
        sa.Column(
            'reminders_enabled',
            sa.Boolean(),
            nullable=False,
            server_default=sa.text('true'),
        )
    )

    # Reminder time (HH:MM format)
    op.add_column(
        'users',
        sa.Column(
            'reminder_time',
            sa.String(length=5),
            nullable=False,
            server_default='20:00',
        )
    )

    # Email digest flag
    op.add_column(
        'users',
        sa.Column(
            'email_digest',
            sa.Boolean(),
            nullable=False,
            server_default=sa.text('true'),
        )
    )

    # Text size preference
    op.add_column(
        'users',
        sa.Column(
            'text_size',
            sa.String(length=10),
            nullable=False,
            server_default='normal',
        )
    )

    # Reduced motion flag
    op.add_column(
        'users',
        sa.Column(
            'reduced_motion',
            sa.Boolean(),
            nullable=False,
            server_default=sa.text('false'),
        )
    )

    # High contrast mode flag
    op.add_column(
        'users',
        sa.Column(
            'high_contrast',
            sa.Boolean(),
            nullable=False,
            server_default=sa.text('false'),
        )
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('users', 'high_contrast')
    op.drop_column('users', 'reduced_motion')
    op.drop_column('users', 'text_size')
    op.drop_column('users', 'email_digest')
    op.drop_column('users', 'reminder_time')
    op.drop_column('users', 'reminders_enabled')
    op.drop_column('users', 'theme')