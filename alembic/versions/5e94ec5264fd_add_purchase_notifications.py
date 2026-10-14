"""add purchase notifications

Revision ID: 5e94ec5264fd
Revises: f971eba7d774
Create Date: 2026-10-14 16:47:07.713305

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5e94ec5264fd'
down_revision: Union[str, Sequence[str], None] = 'f971eba7d774'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "purchase_notifications",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("purchase_id", sa.Integer(), nullable=False),
        sa.Column(
            "notification_type",
            sa.String(length=50),
            nullable=False,
            server_default="purchase_confirmation",
        ),
        sa.Column(
            "status",
            sa.String(length=20),
            nullable=False,
            server_default="pending",
        ),
        sa.Column(
            "attempt_count",
            sa.Integer(),
            nullable=False,
            server_default="0",
        ),
        sa.Column("provider_id", sa.String(length=255), nullable=True),
        sa.Column("last_error", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "sent_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["purchase_id"],
            ["purchases.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "purchase_id",
            "notification_type",
            name="uq_purchase_notification_type",
        ),
    )

    op.create_index(
        op.f("ix_purchase_notifications_purchase_id"),
        "purchase_notifications",
        ["purchase_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        op.f("ix_purchase_notifications_purchase_id"),
        table_name="purchase_notifications",
    )
    op.drop_table("purchase_notifications")
