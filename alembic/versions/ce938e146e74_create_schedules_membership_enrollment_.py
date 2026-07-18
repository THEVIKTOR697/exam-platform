"""create_schedules_membership_enrollment_tables

Revision ID: ce938e146e74
Revises: 0fa8170acc0d
Create Date: 2026-07-18 04:42:19.689140

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ce938e146e74'
down_revision: Union[str, Sequence[str], None] = '0fa8170acc0d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Schedules
    op.create_table(
        "schedules",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("offering_id", sa.Integer(), sa.ForeignKey("course_offerings.id"), nullable=False),
        sa.Column("day_of_week", sa.Integer(), nullable=False),
        sa.Column("start_time", sa.String(), nullable=False),
        sa.Column("end_time", sa.String(), nullable=False),
        sa.Column("classroom", sa.String(), nullable=True),
    )

    # Memberships
    op.create_table(
        "memberships",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("institution_id", sa.Integer(), sa.ForeignKey("institutions.id"), nullable=False),
        sa.Column("role_id", sa.Integer(), sa.ForeignKey("roles.id"), nullable=False),
        sa.UniqueConstraint("user_id", "institution_id", "role_id", name="uq_membership"),
    )

    op.create_index("ix_membership_user", "memberships", ["user_id"])
    op.create_index("ix_membership_institution", "memberships", ["institution_id"])

    # Enrollments
    op.create_table(
        "enrollments",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("offering_id", sa.Integer(), sa.ForeignKey("course_offerings.id"), nullable=False),
        sa.Column("status", sa.String(), nullable=True, server_default="active"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("dropped_at", sa.DateTime(), nullable=True),
        sa.UniqueConstraint("user_id", "offering_id", name="uq_user_offering"),
    )


def downgrade():
    """Downgrade schema."""
    op.drop_table("enrollments")
    op.drop_index("ix_membership_institution", table_name="memberships")
    op.drop_index("ix_membership_user", table_name="memberships")
    op.drop_table("memberships")
    op.drop_table("schedules")

