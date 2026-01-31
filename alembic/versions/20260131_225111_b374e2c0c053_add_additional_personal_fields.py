"""add additional personal fields

Revision ID: b374e2c0c053
Revises: 001_initial
Create Date: 2026-01-31 22:51:11.142127

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b374e2c0c053'
down_revision: Union[str, None] = '001_initial'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'personal_info',
        sa.Column('title', sa.String(length=255), nullable=True)
    )
    op.add_column(
        'personal_info',
        sa.Column('github_url', sa.String(length=500), nullable=True)
    )
    op.add_column(
        'personal_info',
        sa.Column('linkedin_url', sa.String(length=500), nullable=True)
    )
    op.add_column(
        'personal_info',
        sa.Column('twitter_url', sa.String(length=500), nullable=True)
    )
    op.add_column(
        'personal_info',
        sa.Column('website_url', sa.String(length=500), nullable=True)
    )


def downgrade() -> None:
    op.drop_column('personal_info', 'website_url')
    op.drop_column('personal_info', 'twitter_url')
    op.drop_column('personal_info', 'linkedin_url')
    op.drop_column('personal_info', 'github_url')
    op.drop_column('personal_info', 'title')
