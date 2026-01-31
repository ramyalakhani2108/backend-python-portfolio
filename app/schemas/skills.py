"""
Pydantic schemas for Skills.
"""

from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field
from enum import Enum


class SkillCategory(str, Enum):
    """Skill category enum."""

    BACKEND = "backend"
    FRONTEND = "frontend"
    DEVOPS = "devops"
    OTHER = "other"


class SkillBase(BaseModel):
    """Base schema for skills."""

    name: str = Field(..., min_length=1, max_length=100, example="Python")
    category: SkillCategory = Field(..., example=SkillCategory.BACKEND)
    proficiency_level: Optional[int] = Field(
        None, ge=1, le=100, example=90, description="Proficiency level from 1-100"
    )
    is_hobby: bool = Field(False, example=False)


class SkillCreate(SkillBase):
    """Schema for creating a skill."""

    pass


class SkillUpdate(BaseModel):
    """Schema for updating a skill."""

    name: Optional[str] = Field(None, min_length=1, max_length=100)
    category: Optional[SkillCategory] = None
    proficiency_level: Optional[int] = Field(None, ge=1, le=100)
    is_hobby: Optional[bool] = None


class SkillResponse(SkillBase):
    """Schema for skill response."""

    id: UUID

    class Config:
        from_attributes = True
