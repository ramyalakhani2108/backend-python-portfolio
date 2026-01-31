"""
Pydantic schemas for Contact Requests.
"""

from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field


class ContactRequestBase(BaseModel):
    """Base schema for contact request."""

    name: str = Field(..., min_length=1, max_length=255, example="John Doe")
    email: EmailStr = Field(..., example="john.doe@example.com")
    message: str = Field(
        ...,
        min_length=10,
        example="Hi! I'd like to discuss a potential collaboration opportunity.",
    )


class ContactRequestCreate(ContactRequestBase):
    """Schema for creating a contact request."""

    pass


class ContactRequestResponse(ContactRequestBase):
    """Schema for contact request response."""

    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True
