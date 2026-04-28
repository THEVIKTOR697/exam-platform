"""Create users table

Revision ID: bdc1f4d06361
Revises: 
Create Date: 2026-04-20 07:10:52.205496

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bdc1f4d06361'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password_hash", sa.String(), default="pass"),
        sa.Column("is_admin", sa.Boolean, default=False)
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("users")
