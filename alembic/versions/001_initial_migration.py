"""Initial migration - Create all portfolio tables

Revision ID: 001_initial
Revises: 
Create Date: 2026-01-31

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '001_initial'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create personal_info table
    op.create_table(
        'personal_info',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('place', sa.String(length=255), nullable=True),
        sa.Column('country', sa.String(length=100), nullable=True),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('phone', sa.String(length=50), nullable=True),
        sa.Column('bio', sa.Text(), nullable=True),
        sa.Column('profile_image_url', sa.String(length=500), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )

    # Create tags table
    op.create_table(
        'tags',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('label', sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('label')
    )

    # Create skills table
    op.create_table(
        'skills',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('category', sa.String(length=50), nullable=False),
        sa.Column('proficiency_level', sa.Integer(), nullable=True),
        sa.Column('is_hobby', sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # Create certifications table
    op.create_table(
        'certifications',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('issuer', sa.String(length=255), nullable=False),
        sa.Column('issue_date', sa.DateTime(), nullable=True),
        sa.Column('credential_url', sa.String(length=500), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # Create projects table
    op.create_table(
        'projects',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('tech_stack', postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column('github_url', sa.String(length=500), nullable=True),
        sa.Column('live_url', sa.String(length=500), nullable=True),
        sa.Column('project_type', sa.String(length=50), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # Create experience table
    op.create_table(
        'experience',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('company_name', sa.String(length=255), nullable=False),
        sa.Column('role', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('start_date', sa.DateTime(), nullable=True),
        sa.Column('end_date', sa.DateTime(), nullable=True),
        sa.Column('learnings', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # Create contact_requests table
    op.create_table(
        'contact_requests',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # Create ai_context_logs table
    op.create_table(
        'ai_context_logs',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_question', sa.Text(), nullable=False),
        sa.Column('ai_response', sa.Text(), nullable=False),
        sa.Column('used_context', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # Create indexes for better query performance
    op.create_index('ix_skills_category', 'skills', ['category'])
    op.create_index('ix_projects_project_type', 'projects', ['project_type'])
    op.create_index('ix_experience_start_date', 'experience', ['start_date'])
    op.create_index('ix_contact_requests_created_at', 'contact_requests', ['created_at'])
    op.create_index('ix_ai_context_logs_created_at', 'ai_context_logs', ['created_at'])


def downgrade() -> None:
    # Drop indexes
    op.drop_index('ix_ai_context_logs_created_at', table_name='ai_context_logs')
    op.drop_index('ix_contact_requests_created_at', table_name='contact_requests')
    op.drop_index('ix_experience_start_date', table_name='experience')
    op.drop_index('ix_projects_project_type', table_name='projects')
    op.drop_index('ix_skills_category', table_name='skills')

    # Drop tables
    op.drop_table('ai_context_logs')
    op.drop_table('contact_requests')
    op.drop_table('experience')
    op.drop_table('projects')
    op.drop_table('certifications')
    op.drop_table('skills')
    op.drop_table('tags')
    op.drop_table('personal_info')
