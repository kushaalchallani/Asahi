"""add users and data ownership

Revision ID: e948c194faa7
Revises: 95d57041f44b
Create Date: 2026-10-20 00:11:36.437976
"""

from datetime import datetime
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "e948c194faa7"
down_revision: Union[str, Sequence[str], None] = "95d57041f44b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if "users" not in inspector.get_table_names():
        op.create_table(
            "users",
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("email", sa.String(320), nullable=False),
            sa.Column("password_hash", sa.String(), nullable=True),
            sa.Column(
                "is_active",
                sa.Boolean(),
                nullable=False,
                server_default=sa.true(),
            ),
            sa.Column(
                "created_at",
                sa.DateTime(),
                nullable=False,
                server_default=sa.func.now(),
            ),
            sa.UniqueConstraint("email", name="uq_users_email"),
        )

    inspector = sa.inspect(bind)
    indexes = {
        index["name"]
        for index in inspector.get_indexes("users")
    }

    if "ix_users_id" not in indexes:
        op.create_index("ix_users_id", "users", ["id"])

    if "ix_users_email" not in indexes:
        op.create_index(
            "ix_users_email",
            "users",
            ["email"],
            unique=True,
        )

    users = sa.table(
        "users",
        sa.column("id", sa.Integer()),
        sa.column("email", sa.String()),
        sa.column("password_hash", sa.String()),
        sa.column("is_active", sa.Boolean()),
        sa.column("created_at", sa.DateTime()),
    )

    existing_user = bind.execute(
        sa.text("SELECT id FROM users WHERE email = :email"),
        {"email": "kushaal147@gmail.com"},
    ).scalar_one_or_none()

    if existing_user is None:
        bind.execute(
            users.insert().values(
                email="kushaal147@gmail.com",
                password_hash=None,
                is_active=True,
                created_at=datetime.now(),
            )
        )

    user_id = bind.execute(
        sa.text("SELECT id FROM users WHERE email = :email"),
        {"email": "kushaal147@gmail.com"},
    ).scalar_one()

    bind.execute(
        sa.text(
            "SELECT setval("
            "pg_get_serial_sequence('users', 'id'), "
            "COALESCE((SELECT MAX(id) FROM users), 1), "
            "EXISTS (SELECT 1 FROM users)"
            ")"
        )
    )

    for table_name in ("check_ins", "user_missions"):
        inspector = sa.inspect(bind)
        columns = {
            column["name"]
            for column in inspector.get_columns(table_name)
        }

        if "user_id" not in columns:
            op.add_column(
                table_name,
                sa.Column("user_id", sa.Integer(), nullable=True),
            )

        bind.execute(
            sa.text(
                f"UPDATE {table_name} "
                "SET user_id = :user_id WHERE user_id IS NULL"
            ),
            {"user_id": user_id},
        )

        op.alter_column(
            table_name,
            "user_id",
            existing_type=sa.Integer(),
            nullable=False,
        )

        inspector = sa.inspect(bind)
        indexes = {
            index["name"]
            for index in inspector.get_indexes(table_name)
        }
        index_name = f"ix_{table_name}_user_id"

        if index_name not in indexes:
            op.create_index(index_name, table_name, ["user_id"])

        foreign_keys = {
            fk["name"]
            for fk in inspector.get_foreign_keys(table_name)
        }
        fk_name = f"fk_{table_name}_user_id_users"

        if fk_name not in foreign_keys:
            op.create_foreign_key(
                fk_name,
                table_name,
                "users",
                ["user_id"],
                ["id"],
                ondelete="CASCADE",
            )


def downgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    for table_name in ("check_ins", "user_missions"):
        inspector = sa.inspect(bind)

        for fk in inspector.get_foreign_keys(table_name):
            if fk["constrained_columns"] == ["user_id"]:
                op.drop_constraint(
                    fk["name"],
                    table_name,
                    type_="foreignkey",
                )

        inspector = sa.inspect(bind)

        for index in inspector.get_indexes(table_name):
            if index["column_names"] == ["user_id"]:
                op.drop_index(index["name"], table_name=table_name)

        columns = {
            column["name"]
            for column in inspector.get_columns(table_name)
        }
        if "user_id" in columns:
            op.drop_column(table_name, "user_id")

    inspector = sa.inspect(bind)
    if "users" in inspector.get_table_names():
        op.drop_table("users")