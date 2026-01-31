"""
Contact Service - Business logic layer.
"""

from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import ContactRequest
from app.schemas import ContactRequestCreate


class ContactService:
    """Service class for contact request operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_contact_requests(self) -> List[ContactRequest]:
        """Get all contact requests."""
        result = await self.db.execute(
            select(ContactRequest).order_by(ContactRequest.created_at.desc())
        )
        return list(result.scalars().all())

    async def create_contact_request(self, data: ContactRequestCreate) -> ContactRequest:
        """Create a new contact request."""
        contact_request = ContactRequest(**data.model_dump())
        self.db.add(contact_request)
        await self.db.flush()
        await self.db.refresh(contact_request)
        return contact_request
