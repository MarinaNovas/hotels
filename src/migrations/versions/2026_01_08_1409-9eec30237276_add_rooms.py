"""add rooms

Revision ID: 9eec30237276
Revises: fc094b0e9fad
Create Date: 2026-01-08 14:09:13.731806

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "9eec30237276"
down_revision: Union[str, None] = "fc094b0e9fad"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "rooms",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("hotels_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("price", sa.Integer(), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["hotels_id"],
            ["hotels.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("rooms")
