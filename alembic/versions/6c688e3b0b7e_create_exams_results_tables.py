"""create exams/results tables

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
    """Upgrade schema."""
    # EXAMS TABLE
    op.create_table(
        'exams',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('price', sa.Numeric(10, 2), nullable=False),
        sa.Column('is_active', sa.Boolean(), server_default=sa.true(), nullable=False),
        sa.Column(
            'created_at',
            sa.DateTime(timezone=True),
            server_default=sa.text('now()'),
            nullable=False
        ),
    )
    op.create_index('ix_exams_id', 'exams', ['id'])
    op.create_index('ix_exams_title', 'exams', ['title'])

    # RESULTS TABLE
    op.create_table(
        'results',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('exam_id', sa.Integer(), nullable=False),
        sa.Column('score', sa.Numeric(5, 2), nullable=False),
        sa.Column('passed', sa.Boolean(), nullable=False),
        sa.Column(
            'created_at',
            sa.DateTime(timezone=True),
            server_default=sa.text('now()'),
            nullable=False
        ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['exam_id'], ['exams.id'], ondelete='CASCADE'),
    )

    op.create_index('ix_results_id', 'results', ['id'])
    op.create_index('ix_results_user_id', 'results', ['user_id'])
    op.create_index('ix_results_exam_id', 'results', ['exam_id'])


def downgrade() -> None:
    """Downgrade schema."""

    # Drop indexes first for best practice
    op.drop_index('ix_results_exam_id', table_name='results')
    op.drop_index('ix_results_user_id', table_name='results')
    op.drop_index('ix_results_id', table_name='results')

    op.drop_table('results')

    op.drop_index('ix_exams_id', table_name='exams')
    op.drop_table('exams')