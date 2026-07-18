"""create_courses_exams_results_tables

Revision ID: 6c688e3b0b7e
Revises: bdc1f4d06361
Create Date: 2026-05-08 22:42:29.697034

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6c688e3b0b7e'
down_revision: Union[str, Sequence[str], None] = 'bdc1f4d06361'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Institutions
    op.create_table(
        "institutions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("slug", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("email", sa.String(), nullable=True),
        sa.Column("phone", sa.String(), nullable=True),
        sa.Column("website", sa.String(), nullable=True),
        sa.Column("country", sa.String(), nullable=True),
        sa.Column("state", sa.String(), nullable=True),
        sa.Column("city", sa.String(), nullable=True),
        sa.Column("address", sa.String(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.UniqueConstraint("slug", name="uq_institutions_slug"),
    )

    # Certification courses
    op.create_table(
        "certification_courses",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("institution_id", sa.Integer(), nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default=sa.true(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["institution_id"], ["institutions.id"]),
    )

    # Certification exams
    op.create_table(
        "certification_exams",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(), nullable=False, unique=True),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("price", sa.Numeric(10, 2), nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default=sa.true(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("institution_id", sa.Integer(), nullable=False),
        sa.Column("course_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["institution_id"], ["institutions.id"]),
        sa.ForeignKeyConstraint(["course_id"], ["certification_courses.id"]),
    )

    op.create_index('ix_certification_exams_title', 'certification_exams', ['title'])

    # Certification results
    op.create_table(
        "certification_results",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("exam_id", sa.Integer(), nullable=False),
        sa.Column("score", sa.Numeric(5, 2), nullable=False),
        sa.Column("passed", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["exam_id"], ["certification_exams.id"], ondelete="CASCADE"),
    )

    op.create_index('ix_certification_results_user_id', 'certification_results', ['user_id'])
    op.create_index('ix_certification_results_exam_id', 'certification_results', ['exam_id'])
    op.create_index(
        'ix_results_user_exam',
        'certification_results',
        ['user_id', 'exam_id']
    )

def downgrade() -> None:
    op.drop_index('ix_results_user_exam', table_name='certification_results')
    op.drop_index('ix_certification_results_exam_id', table_name='certification_results')
    op.drop_index('ix_certification_results_user_id', table_name='certification_results')

    op.drop_table('certification_results')

    op.drop_index('ix_certification_exams_title', table_name='certification_exams')

    op.drop_table('certification_exams')
    op.drop_table('certification_courses')
    op.drop_table('institutions')