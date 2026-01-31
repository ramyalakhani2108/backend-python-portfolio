"""
Projects Service - Business logic layer.
"""

from typing import List, Optional
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Project
from app.schemas import ProjectCreate, ProjectUpdate


class ProjectService:
    """Service class for project operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_projects(self) -> List[Project]:
        """Get all projects."""
        result = await self.db.execute(select(Project).order_by(Project.created_at.desc()))
        return list(result.scalars().all())

    async def get_project_by_id(self, project_id: UUID) -> Optional[Project]:
        """Get a project by ID."""
        result = await self.db.execute(
            select(Project).where(Project.id == project_id)
        )
        return result.scalar_one_or_none()

    async def get_projects_by_type(self, project_type: str) -> List[Project]:
        """Get projects by type."""
        result = await self.db.execute(
            select(Project).where(Project.project_type == project_type)
        )
        return list(result.scalars().all())

    async def create_project(self, data: ProjectCreate) -> Project:
        """Create a new project."""
        project = Project(**data.model_dump())
        self.db.add(project)
        await self.db.flush()
        await self.db.refresh(project)
        return project

    async def update_project(
        self, project_id: UUID, data: ProjectUpdate
    ) -> Optional[Project]:
        """Update a project."""
        result = await self.db.execute(
            select(Project).where(Project.id == project_id)
        )
        project = result.scalar_one_or_none()

        if project:
            update_data = data.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(project, field, value)
            await self.db.flush()
            await self.db.refresh(project)

        return project

    async def delete_project(self, project_id: UUID) -> bool:
        """Delete a project."""
        result = await self.db.execute(
            select(Project).where(Project.id == project_id)
        )
        project = result.scalar_one_or_none()

        if project:
            await self.db.delete(project)
            return True
        return False
