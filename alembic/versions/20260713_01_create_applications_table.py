"""Create applications table.

Revision ID: 20260713_01
Revises:
Create Date: 2026-07-13

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "20260713_01"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create the applications table and primary-key index."""
    op.create_table(
        "applications",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("company", sa.String(), nullable=False),
        sa.Column("position", sa.String(), nullable=False),
        sa.Column("status", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_applications_id"),
        "applications",
        ["id"],
        unique=False,
    )


def downgrade() -> None:
    """Remove the applications table."""
    op.drop_index(op.f("ix_applications_id"), table_name="applications")
    op.drop_table("applications")
