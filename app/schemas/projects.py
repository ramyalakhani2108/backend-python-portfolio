"""
Pydantic schemas for Projects.
"""

from datetime import datetime
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, Field
from enum import Enum


class ProjectType(str, Enum):
    """Project type enum."""

    PERSONAL = "personal"
    PROFESSIONAL = "professional"


class ProjectBase(BaseModel):
    """Base schema for projects."""

    title: str = Field(..., min_length=1, max_length=255, example="Portfolio App")
    description: Optional[str] = Field(
        None, example="A personal portfolio application built with Flutter and FastAPI."
    )
    tech_stack: Optional[List[str]] = Field(
        None, example=["Flutter", "FastAPI", "PostgreSQL", "Gemini AI"]
    )
    github_url: Optional[str] = Field(
        None, max_length=500, example="https://github.com/username/portfolio"
    )
    live_url: Optional[str] = Field(
        None, max_length=500, example="https://portfolio.example.com"
    )
    project_type: ProjectType = Field(ProjectType.PERSONAL, example=ProjectType.PERSONAL)


class ProjectCreate(ProjectBase):
    """Schema for creating a project."""

    pass


class ProjectUpdate(BaseModel):
    """Schema for updating a project."""

    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    tech_stack: Optional[List[str]] = None
    github_url: Optional[str] = Field(None, max_length=500)
    live_url: Optional[str] = Field(None, max_length=500)
    project_type: Optional[ProjectType] = None


class ProjectResponse(ProjectBase):
    """Schema for project response."""

    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True
