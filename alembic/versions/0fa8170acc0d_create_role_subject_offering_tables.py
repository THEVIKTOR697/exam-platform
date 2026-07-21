"""create_institution_role_subject_and_offerings tables

Revision ID: 0fa8170acc0d
Revises: 7bdb7cb3b73a
Create Date: 2026-07-11 01:44:11.849464

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '0fa8170acc0d'
down_revision: Union[str, Sequence[str], None] = '7bdb7cb3b73a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    # =========================
    # ROLES
    op.create_table(
        "roles",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=False),
        sa.UniqueConstraint("name", name="uq_roles_name"),
    )

    # =========================
    # MEMBERSHIPS
    op.create_table(
        "memberships",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("institution_id", sa.Integer(), nullable=False),
        sa.Column("role_id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),

        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["institution_id"], ["institutions.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["role_id"], ["roles.id"], ondelete="RESTRICT"),
        sa.UniqueConstraint(
            "user_id",
            "institution_id",
            "role_id",
            name="uq_membership_unique"
        ),
        sa.UniqueConstraint(
            "id",
            "institution_id",
            name="uq_membership_id_institution"
        ),
    )

    op.create_index("ix_membership_user", "memberships", ["user_id"])
    op.create_index("ix_membership_institution", "memberships", ["institution_id"])


    # =========================
    # GRADES
    op.create_table(
        "grades",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("level", sa.Integer(), nullable=False),
        sa.Column("institution_id", sa.Integer(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),

        sa.ForeignKeyConstraint(
            ["institution_id"],
            ["institutions.id"],
            ondelete="CASCADE"
        ),

        sa.UniqueConstraint(
            "name",
            "institution_id",
            name="uq_grade_name_per_institution"
        ),
    )

    op.create_index("ix_grades_institution", "grades", ["institution_id"])

    # =========================
    # STUDENTS
    op.create_table(
        "students",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("membership_id", sa.Integer(), nullable=False),
        sa.Column("institution_id", sa.Integer(), nullable=False),
        sa.Column("student_number", sa.String(), nullable=False),
        sa.Column("current_grade_id", sa.Integer(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True),server_default=sa.func.now()),
        sa.ForeignKeyConstraint(
            ["membership_id", "institution_id"],
            [
                "memberships.id",
                "memberships.institution_id"
            ],
            name="fk_student_membership_same_institution",
            ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["institution_id"],
            ["institutions.id"],
            ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["current_grade_id"],
            ["grades.id"],
            ondelete="RESTRICT"
        ),
        sa.UniqueConstraint(
            "student_number",
            name="uq_students_number"
        ),
        sa.UniqueConstraint(
            "membership_id",
            name="uq_student_membership"
        ),
        sa.UniqueConstraint(
            "id",
            "institution_id",
            name="uq_student_id_institution"
        ),
    )
    op.create_index("ix_students_institution","students",["institution_id"])
    op.create_index("ix_students_grade","students",["current_grade_id"])

    # =========================
    # SUBJECTS
    op.create_table(
        "subjects",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=False),
        sa.Column("code", sa.String(), nullable=False),
        sa.Column("credits", sa.Integer(), nullable=True),
        sa.Column("grade_id", sa.Integer(), nullable=False),
        sa.Column("institution_id", sa.Integer(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),

        sa.ForeignKeyConstraint(
            ["grade_id"],
            ["grades.id"],
            ondelete="CASCADE"
        ),

        sa.ForeignKeyConstraint(
            ["institution_id"],
            ["institutions.id"],
            ondelete="CASCADE"
        ),

        sa.UniqueConstraint(
            "code",
            "institution_id",
            name="uq_subject_code_per_institution"
        ),
    )

    op.create_index("ix_subjects_grade", "subjects", ["grade_id"])
    op.create_index("ix_subjects_institution", "subjects", ["institution_id"])


    # =========================
    # COURSE OFFERINGS
    op.create_table(
        "course_offerings",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("institution_id", sa.Integer(), nullable=False),
        sa.Column("subject_id", sa.Integer(), nullable=False),
        sa.Column("teacher_id", sa.Integer(), nullable=True),
        sa.Column("group_name", sa.String(), nullable=True),
        sa.Column("capacity", sa.Integer(), nullable=True),
        sa.Column("start_time", sa.Time(), nullable=False),
        sa.Column("end_time", sa.Time(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),

        sa.ForeignKeyConstraint(
            ["institution_id"],
            ["institutions.id"],
            ondelete="CASCADE"
        ),

        sa.ForeignKeyConstraint(
            ["subject_id"],
            ["subjects.id"],
            ondelete="CASCADE"
        ),

        sa.ForeignKeyConstraint(
            ["teacher_id"],
            ["memberships.id"],
            ondelete="SET NULL"
        ),
        sa.UniqueConstraint(
            "id",
            "institution_id",
            name="uq_course_offering_id_institution"
        ),
        sa.UniqueConstraint(
            "subject_id",
            "group_name",
            "institution_id",
            name="uq_course_offering_group"
        ),
    )

    op.create_index("ix_offerings_subject", "course_offerings", ["subject_id"])
    op.create_index("ix_offerings_institution", "course_offerings", ["institution_id"])


def downgrade():
    op.drop_table("course_offerings")
    op.drop_table("subjects")
    op.drop_index("ix_students_grade", table_name="students")
    op.drop_index("ix_students_institution", table_name="students")
    op.drop_table("students")
    # op.execute(
    #     "DROP INDEX IF EXISTS ix_students_grade"
    # )
    # op.execute(
    #     "DROP INDEX IF EXISTS ix_students_institution"
    # )
    # op.execute("""   DROP TABLE IF EXISTS students CASCADE    """)
    op.drop_table("grades")
    op.drop_index("ix_membership_institution", table_name="memberships")
    op.drop_index("ix_membership_user", table_name="memberships")
    op.drop_table("memberships")
    op.drop_table("roles")
