"""add to UsersOrm unique email

Revision ID: 030d3ba24900
Revises: fa6ea896cf36
Create Date: 2026-01-23 21:16:58.238818

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "030d3ba24900"
down_revision: Union[str, None] = "fa6ea896cf36"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(None, "users", ["email"])


def downgrade() -> None:
    op.drop_constraint(None, "users", type_="unique")
