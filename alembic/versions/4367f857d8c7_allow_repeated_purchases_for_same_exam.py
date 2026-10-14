"""allow repeated purchases for same exam

Revision ID: 4367f857d8c7
Revises: 8deecd0c2d93
Create Date: 2026-10-11 23:05:21.928290

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4367f857d8c7'
down_revision: Union[str, Sequence[str], None] = '8deecd0c2d93'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.drop_constraint(
        "uq_user_exam_purchase",
        "purchases",
        type_="unique",
    )


def downgrade():
    op.create_unique_constraint(
        "uq_user_exam_purchase",
        "purchases",
        ["user_id", "exam_id"],
    )