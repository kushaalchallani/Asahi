
"""create initial database schema

Revision ID: 000000000001
Revises:
"""

from alembic import op
import sqlalchemy as sa


revision = "000000000001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Original check-ins table (before the note migration).
    op.create_table(
        "check_ins",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("feeling", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_check_ins_id", "check_ins", ["id"])

    # Original missions table (before personalization fields).
    op.create_table(
        "missions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=False),
        sa.Column("category", sa.String(), nullable=False),
        sa.Column("difficulty", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_missions_id", "missions", ["id"])

    # Original user missions table (before tracking and ownership).
    op.create_table(
        "user_missions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("mission_id", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("started_at", sa.DateTime(), nullable=True),
        sa.Column("completed_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_user_missions_id", "user_missions", ["id"])


def downgrade():
    op.drop_index("ix_user_missions_id", table_name="user_missions")
    op.drop_table("user_missions")

    op.drop_index("ix_missions_id", table_name="missions")
    op.drop_table("missions")

    op.drop_index("ix_check_ins_id", table_name="check_ins")
    op.drop_table("check_ins")
