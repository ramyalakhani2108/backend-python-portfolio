"""
Skills Service - Business logic layer.
"""

from typing import List, Optional
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Skill
from app.schemas import SkillCreate, SkillUpdate


class SkillService:
    """Service class for skill operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_skills(self) -> List[Skill]:
        """Get all skills."""
        result = await self.db.execute(select(Skill))
        return list(result.scalars().all())

    async def get_skill_by_id(self, skill_id: UUID) -> Optional[Skill]:
        """Get a skill by ID."""
        result = await self.db.execute(select(Skill).where(Skill.id == skill_id))
        return result.scalar_one_or_none()

    async def get_skills_by_category(self, category: str) -> List[Skill]:
        """Get skills by category."""
        result = await self.db.execute(
            select(Skill).where(Skill.category == category)
        )
        return list(result.scalars().all())

    async def create_skill(self, data: SkillCreate) -> Skill:
        """Create a new skill."""
        skill = Skill(**data.model_dump())
        self.db.add(skill)
        await self.db.flush()
        await self.db.refresh(skill)
        return skill

    async def update_skill(self, skill_id: UUID, data: SkillUpdate) -> Optional[Skill]:
        """Update a skill."""
        result = await self.db.execute(select(Skill).where(Skill.id == skill_id))
        skill = result.scalar_one_or_none()

        if skill:
            update_data = data.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(skill, field, value)
            await self.db.flush()
            await self.db.refresh(skill)

        return skill

    async def delete_skill(self, skill_id: UUID) -> bool:
        """Delete a skill."""
        result = await self.db.execute(select(Skill).where(Skill.id == skill_id))
        skill = result.scalar_one_or_none()

        if skill:
            await self.db.delete(skill)
            return True
        return False
