"""refactor exams to certification_exams

Revision ID: 063b9881e88b
Revises: 0fa8170acc0d
Create Date: 2026-07-11 01:48:26.512835

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '063b9881e88b'
down_revision: Union[str, Sequence[str], None] = '0fa8170acc0d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.rename_table("exams", "certification_exams")
    op.rename_table("results", "certification_results")

    op.create_table(
        "certification_courses",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("institution_id", sa.Integer(), nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),

        sa.ForeignKeyConstraint(
            ["institution_id"],
            ["institutions.id"]
        )
    )

    op.add_column(
        "certification_exams",
        sa.Column("institution_id", sa.Integer(), nullable=True)
    )

    op.add_column(
        "certification_exams",
        sa.Column("course_id", sa.Integer(), nullable=True)
    )

    op.create_foreign_key(
        "fk_exam_institution",
        "certification_exams",
        "institutions",
        ["institution_id"],
        ["id"],
    )

    op.create_foreign_key(
        "fk_exam_course",
        "certification_exams",
        "certification_courses",
        ["course_id"],
        ["id"],
    )


def downgrade() -> None:
    op.drop_constraint("fk_exam_course", "certification_exams", type_="foreignkey")
    op.drop_constraint("fk_exam_institution", "certification_exams", type_="foreignkey")

    op.drop_column("certification_exams", "course_id")
    op.drop_column("certification_exams", "institution_id")

    op.drop_table("certification_courses")

    op.rename_table("certification_results", "results")
    op.rename_table("certification_exams", "exams")
