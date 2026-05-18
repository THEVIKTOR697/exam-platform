"""questions and options

Revision ID: 7bdb7cb3b73a
Revises: 2a58f18b07e7
Create Date: 2026-05-08 23:23:49.539570

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '7bdb7cb3b73a'
down_revision: Union[str, Sequence[str], None] = '2a58f18b07e7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        "questions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("exam_id", sa.Integer(), nullable=False),
        sa.Column("text", sa.String(), nullable=False),

        sa.ForeignKeyConstraint(["exam_id"], ["exams.id"], ondelete="CASCADE"),
    )

    op.create_index("ix_questions_exam_id", "questions", ["exam_id"])


    op.create_table(
        "options",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("question_id", sa.Integer(), nullable=False),
        sa.Column("text", sa.String(), nullable=False),
        sa.Column("is_correct", sa.Boolean(), nullable=False, server_default="false"),

        sa.ForeignKeyConstraint(["question_id"], ["questions.id"], ondelete="CASCADE"),
    )

    op.create_index("ix_options_question_id", "options", ["question_id"])


def downgrade():
    op.drop_index("ix_options_question_id", table_name="options")
    op.drop_table("options")

    op.drop_index("ix_questions_exam_id", table_name="questions")
    op.drop_table("questions")