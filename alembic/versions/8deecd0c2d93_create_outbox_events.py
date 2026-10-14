"""create outbox events

Revision ID: 8deecd0c2d93
Revises: ce938e146e74
Create Date: 2026-10-11 00:19:18.011013

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '8deecd0c2d93'
down_revision: Union[str, Sequence[str], None] = 'ce938e146e74'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "outbox_events",
        sa.Column(
            "id",
            sa.BigInteger(),
            primary_key=True,
        ),
        sa.Column(
            "aggregate_type",
            sa.String(100),
            nullable=False,
        ),
        sa.Column(
            "aggregate_id",
            sa.String(100),
            nullable=False,
        ),
        sa.Column(
            "event_type",
            sa.String(150),
            nullable=False,
        ),
        sa.Column(
            "payload",
            postgresql.JSONB(),
            nullable=False,
        ),
        sa.Column(
            "status",
            sa.String(20),
            nullable=False,
            server_default="pending",
        ),
        sa.Column(
            "retry_count",
            sa.Integer(),
            nullable=False,
            server_default="0",
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column(
            "published_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
        sa.Column(
            "last_error",
            sa.Text(),
            nullable=True,
        ),
    )

    op.create_index(
        "ix_outbox_events_status_created_at",
        "outbox_events",
        ["status", "created_at"],
    )


def downgrade() -> None:
    op.drop_index(
        "ix_outbox_events_status_created_at",
        table_name="outbox_events",
    )
    op.drop_table("outbox_events")
