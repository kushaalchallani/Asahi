"""add feedback timestamp to user missions

Revision ID: 2bbf859faed2
Revises: e948c194faa7
Create Date: 2026-10-30 20:12:35.185591

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2bbf859faed2'
down_revision: Union[str, Sequence[str], None] = 'e948c194faa7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


"""add feedback timestamp to user missions

Revision ID: 2bbf859faed2
Revises: e948c194faa7
Create Date: 2026-10-30 20:12:35.185591

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2bbf859faed2'
down_revision: Union[str, Sequence[str], None] = 'e948c194faa7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "user_missions",
        sa.Column("feedback_at", sa.DateTime(), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("user_missions", "feedback_at")
