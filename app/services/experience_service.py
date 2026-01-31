"""
Experience Service - Business logic layer.
"""

from typing import List, Optional
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Experience
from app.schemas import ExperienceCreate, ExperienceUpdate


class ExperienceService:
    """Service class for experience operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_experiences(self) -> List[Experience]:
        """Get all experiences ordered by start date."""
        result = await self.db.execute(
            select(Experience).order_by(Experience.start_date.desc())
        )
        return list(result.scalars().all())

    async def get_experience_by_id(self, exp_id: UUID) -> Optional[Experience]:
        """Get an experience by ID."""
        result = await self.db.execute(
            select(Experience).where(Experience.id == exp_id)
        )
        return result.scalar_one_or_none()

    async def create_experience(self, data: ExperienceCreate) -> Experience:
        """Create a new experience."""
        experience = Experience(**data.model_dump())
        self.db.add(experience)
        await self.db.flush()
        await self.db.refresh(experience)
        return experience

    async def update_experience(
        self, exp_id: UUID, data: ExperienceUpdate
    ) -> Optional[Experience]:
        """Update an experience."""
        result = await self.db.execute(
            select(Experience).where(Experience.id == exp_id)
        )
        experience = result.scalar_one_or_none()

        if experience:
            update_data = data.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(experience, field, value)
            await self.db.flush()
            await self.db.refresh(experience)

        return experience

    async def delete_experience(self, exp_id: UUID) -> bool:
        """Delete an experience."""
        result = await self.db.execute(
            select(Experience).where(Experience.id == exp_id)
        )
        experience = result.scalar_one_or_none()

        if experience:
            await self.db.delete(experience)
            return True
        return False
