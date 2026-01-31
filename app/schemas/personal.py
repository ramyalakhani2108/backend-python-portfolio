"""
Pydantic schemas for Personal Info.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field


class PersonalInfoBase(BaseModel):
    """Base schema for personal info."""

    name: str = Field(..., min_length=1, max_length=255, example="Ramya")
    title: Optional[str] = Field(None, max_length=255, example="Full Stack Developer")
    place: Optional[str] = Field(None, max_length=255, example="Bangalore")
    country: Optional[str] = Field(None, max_length=100, example="India")
    email: EmailStr = Field(..., example="ramya@example.com")
    phone: Optional[str] = Field(None, max_length=50, example="+91-9876543210")
    bio: Optional[str] = Field(
        None,
        example="Full-stack developer passionate about building scalable applications.",
    )
    profile_image_url: Optional[str] = Field(
        None, max_length=500, example="https://example.com/profile.jpg"
    )
    github_url: Optional[str] = Field(None, max_length=500, example="https://github.com/username")
    linkedin_url: Optional[str] = Field(None, max_length=500, example="https://linkedin.com/in/username")
    twitter_url: Optional[str] = Field(None, max_length=500, example="https://twitter.com/username")
    website_url: Optional[str] = Field(None, max_length=500, example="https://website.com")


class PersonalInfoCreate(PersonalInfoBase):
    """Schema for creating personal info."""

    pass


class PersonalInfoUpdate(BaseModel):
    """Schema for updating personal info."""

    name: Optional[str] = Field(None, min_length=1, max_length=255)
    title: Optional[str] = Field(None, max_length=255)
    place: Optional[str] = Field(None, max_length=255)
    country: Optional[str] = Field(None, max_length=100)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=50)
    bio: Optional[str] = None
    profile_image_url: Optional[str] = Field(None, max_length=500)
    github_url: Optional[str] = Field(None, max_length=500)
    linkedin_url: Optional[str] = Field(None, max_length=500)
    twitter_url: Optional[str] = Field(None, max_length=500)
    website_url: Optional[str] = Field(None, max_length=500)


class PersonalInfoResponse(PersonalInfoBase):
    """Schema for personal info response."""

    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
