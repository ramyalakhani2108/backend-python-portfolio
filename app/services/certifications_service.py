"""
Certifications Service - Business logic layer.
"""

from typing import List, Optional
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Certification
from app.schemas import CertificationCreate, CertificationUpdate


class CertificationService:
    """Service class for certification operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_certifications(self) -> List[Certification]:
        """Get all certifications."""
        result = await self.db.execute(select(Certification))
        return list(result.scalars().all())

    async def get_certification_by_id(self, cert_id: UUID) -> Optional[Certification]:
        """Get a certification by ID."""
        result = await self.db.execute(
            select(Certification).where(Certification.id == cert_id)
        )
        return result.scalar_one_or_none()

    async def create_certification(self, data: CertificationCreate) -> Certification:
        """Create a new certification."""
        certification = Certification(**data.model_dump())
        self.db.add(certification)
        await self.db.flush()
        await self.db.refresh(certification)
        return certification

    async def update_certification(
        self, cert_id: UUID, data: CertificationUpdate
    ) -> Optional[Certification]:
        """Update a certification."""
        result = await self.db.execute(
            select(Certification).where(Certification.id == cert_id)
        )
        certification = result.scalar_one_or_none()

        if certification:
            update_data = data.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(certification, field, value)
            await self.db.flush()
            await self.db.refresh(certification)

        return certification

    async def delete_certification(self, cert_id: UUID) -> bool:
        """Delete a certification."""
        result = await self.db.execute(
            select(Certification).where(Certification.id == cert_id)
        )
        certification = result.scalar_one_or_none()

        if certification:
            await self.db.delete(certification)
            return True
        return False
