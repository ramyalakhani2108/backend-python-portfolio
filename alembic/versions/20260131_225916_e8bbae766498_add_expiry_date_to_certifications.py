"""add expiry_date to certifications

Revision ID: e8bbae766498
Revises: b374e2c0c053
Create Date: 2026-01-31 22:59:16.193261

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e8bbae766498'
down_revision: Union[str, None] = 'b374e2c0c053'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'certifications',
        sa.Column('expiry_date', sa.DateTime(), nullable=True)
    )


def downgrade() -> None:
    op.drop_column('certifications', 'expiry_date')
