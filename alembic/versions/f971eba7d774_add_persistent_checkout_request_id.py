"""add persistent checkout request id

Revision ID: f971eba7d774
Revises: 4367f857d8c7
Create Date: 2026-10-11 23:28:05.452688

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f971eba7d774'
down_revision: Union[str, Sequence[str], None] = '4367f857d8c7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column(
        "purchases",
        sa.Column(
            "checkout_request_id",
            sa.String(length=36),
            nullable=True,
        ),
    )

    op.alter_column(
        "purchases",
        "stripe_session_id",
        existing_type=sa.String(),
        nullable=True,
    )

    op.create_unique_constraint(
        "uq_purchase_user_checkout_request",
        "purchases",
        ["user_id", "checkout_request_id"],
    )



def downgrade():
    op.drop_constraint(
        "uq_purchase_user_checkout_request",
        "purchases",
        type_="unique",
    )

    op.drop_column("purchases", "checkout_request_id")

    op.alter_column(
        "purchases",
        "stripe_session_id",
        existing_type=sa.String(),
        nullable=False,
    )
