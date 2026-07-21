"""create_schedules_enrollments_tables

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
    # =========================
    # SCHEDULES
    op.create_table(
        "schedules",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("offering_id", sa.Integer(), nullable=False),
        sa.Column("institution_id", sa.Integer(), nullable=False),
        sa.Column("day_of_week", sa.Integer(), nullable=False),
        sa.Column("start_time", sa.String(), nullable=False),
        sa.Column("end_time", sa.String(), nullable=False),
        sa.Column("classroom", sa.String(), nullable=True),

        sa.ForeignKeyConstraint(
            ["offering_id", "institution_id"],
            ["course_offerings.id", "course_offerings.institution_id"],
            name="fk_schedule_offering_same_institution"
        ),

        sa.ForeignKeyConstraint(
            ["institution_id"],
            ["institutions.id"],
            ondelete="CASCADE"
        ),
    )

    # =========================
    # ENROLLMENTS
    op.create_table(
        "enrollments",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("student_id", sa.Integer(), nullable=False),
        sa.Column("offering_id", sa.Integer(), nullable=False),
        sa.Column("institution_id", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(), nullable=True, server_default="active"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("dropped_at", sa.DateTime(), nullable=True),

        sa.ForeignKeyConstraint(
            ["student_id", "institution_id"],
            [
                "students.id",
                "students.institution_id"
            ],
            name="fk_enrollment_student_same_institution"
        ),

        sa.ForeignKeyConstraint(
            ["offering_id", "institution_id"],
            ["course_offerings.id", "course_offerings.institution_id"],
            name="fk_enrollment_offering_same_institution"
        ),

        sa.ForeignKeyConstraint(
            ["institution_id"],
            ["institutions.id"],
            ondelete="CASCADE"
        ),

        sa.UniqueConstraint(
            "student_id",
            "offering_id",
            "institution_id",
            name="uq_student_offering"
        ),
    )


def downgrade():
    op.drop_table("enrollments")
    op.drop_table("schedules")
