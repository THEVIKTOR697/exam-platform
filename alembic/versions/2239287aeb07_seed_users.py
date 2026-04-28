"""seed users

Revision ID: 2239287aeb07
Revises: bdc1f4d06361
Create Date: 2026-04-20 07:15:29.423829

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2239287aeb07'
down_revision: Union[str, Sequence[str], None] = 'bdc1f4d06361'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""
        INSERT INTO users (name, email) VALUES
        ('Frodo', 'frodo@shire.com'),
        ('Sam', 'sam@shire.com'),
        ('Gandalf', 'gandalf@middleearth.com')
    """)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("""
        DELETE FROM users
        WHERE email IN (
            'frodo@shire.com',
            'sam@shire.com',
            'gandalf@middleearth.com'
        )
    """)
