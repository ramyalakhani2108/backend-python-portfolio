"""
Personal Info Service - Business logic layer.
"""

from typing import Optional
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import PersonalInfo
from app.schemas import PersonalInfoCreate, PersonalInfoUpdate


class PersonalInfoService:
    """Service class for personal info operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_personal_info(self) -> Optional[PersonalInfo]:
        """Get the personal info (single record)."""
        result = await self.db.execute(select(PersonalInfo).limit(1))
        return result.scalar_one_or_none()

    async def create_personal_info(self, data: PersonalInfoCreate) -> PersonalInfo:
        """Create personal info."""
        personal_info = PersonalInfo(**data.model_dump())
        self.db.add(personal_info)
        await self.db.flush()
        await self.db.refresh(personal_info)
        return personal_info

    async def update_personal_info(
        self, id: UUID, data: PersonalInfoUpdate
    ) -> Optional[PersonalInfo]:
        """Update personal info."""
        result = await self.db.execute(
            select(PersonalInfo).where(PersonalInfo.id == id)
        )
        personal_info = result.scalar_one_or_none()

        if personal_info:
            update_data = data.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(personal_info, field, value)
            await self.db.flush()
            await self.db.refresh(personal_info)

        return personal_info
