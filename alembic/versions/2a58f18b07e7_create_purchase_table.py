"""create_purchase_table

Revision ID: 2a58f18b07e7
Revises: 6c688e3b0b7e
Create Date: 2026-05-08 22:57:46.469137

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '2a58f18b07e7'
down_revision: Union[str, Sequence[str], None] = '6c688e3b0b7e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_table(
        'purchases',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),

        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('exam_id', sa.Integer(), nullable=False),

        sa.Column('stripe_session_id', sa.String(), nullable=False),
        sa.Column('payment_intent_id', sa.String(), nullable=True, unique=True),

        sa.Column('amount', sa.Numeric(10, 2), nullable=False),

        sa.Column(
            'currency',
            sa.String(length=10),
            nullable=False,
            server_default='usd'
        ),

        sa.Column(
            'status',
            sa.String(length=20),
            nullable=False,
            server_default='pending'
        ),

        sa.Column(
            'created_at',
            sa.DateTime(timezone=True),
            server_default=sa.text('now()'),
            nullable=False
        ),

        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['exam_id'], ['certification_exams.id'], ondelete='CASCADE'),

        sa.UniqueConstraint('user_id', 'exam_id', name='uq_user_exam_purchase'),
    )

    op.create_index('ix_purchases_user_id', 'purchases', ['user_id'])
    op.create_index('ix_purchases_exam_id', 'purchases', ['exam_id'])
    op.create_index('ix_purchases_stripe_session_id', 'purchases', ['stripe_session_id'], unique=True)


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_index('ix_purchases_stripe_session_id', table_name='purchases')
    op.drop_index('ix_purchases_exam_id', table_name='purchases')
    op.drop_index('ix_purchases_user_id', table_name='purchases')

    op.drop_table('purchases')