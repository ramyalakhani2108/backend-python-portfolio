"""
Pydantic schemas for Tags.
"""

from uuid import UUID
from pydantic import BaseModel, Field


class TagBase(BaseModel):
    """Base schema for tags."""

    label: str = Field(..., min_length=1, max_length=100, example="Machine Learning")


class TagCreate(TagBase):
    """Schema for creating a tag."""

    pass


class TagResponse(TagBase):
    """Schema for tag response."""

    id: UUID

    class Config:
        from_attributes = True
