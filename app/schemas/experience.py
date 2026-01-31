"""
Pydantic schemas for Experience.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field


class ExperienceBase(BaseModel):
    """Base schema for experience."""

    company_name: str = Field(..., min_length=1, max_length=255, example="Tech Corp")
    role: str = Field(..., min_length=1, max_length=255, example="Senior Software Engineer")
    description: Optional[str] = Field(
        None,
        example="Led development of microservices architecture and mentored junior developers.",
    )
    start_date: Optional[datetime] = Field(None, example="2022-01-01T00:00:00")
    end_date: Optional[datetime] = Field(
        None, example="2024-12-31T00:00:00", description="Null for current position"
    )
    learnings: Optional[str] = Field(
        None,
        example="Gained expertise in distributed systems, cloud architecture, and team leadership.",
    )


class ExperienceCreate(ExperienceBase):
    """Schema for creating experience."""

    pass


class ExperienceUpdate(BaseModel):
    """Schema for updating experience."""

    company_name: Optional[str] = Field(None, min_length=1, max_length=255)
    role: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    learnings: Optional[str] = None


class ExperienceResponse(ExperienceBase):
    """Schema for experience response."""

    id: UUID

    class Config:
        from_attributes = True
