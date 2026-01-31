"""
Pydantic schemas for Certifications.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field, HttpUrl


class CertificationBase(BaseModel):
    """Base schema for certifications."""

    title: str = Field(
        ..., min_length=1, max_length=255, example="AWS Solutions Architect"
    )
    issuer: str = Field(..., min_length=1, max_length=255, example="Amazon Web Services")
    issue_date: Optional[datetime] = Field(None, example="2024-01-15T00:00:00")
    expiry_date: Optional[datetime] = Field(None, example="2027-01-15T00:00:00")
    credential_url: Optional[str] = Field(
        None, max_length=500, example="https://aws.amazon.com/verification/12345"
    )


class CertificationCreate(CertificationBase):
    """Schema for creating a certification."""

    pass


class CertificationUpdate(BaseModel):
    """Schema for updating a certification."""

    title: Optional[str] = Field(None, min_length=1, max_length=255)
    issuer: Optional[str] = Field(None, min_length=1, max_length=255)
    issue_date: Optional[datetime] = None
    expiry_date: Optional[datetime] = None
    credential_url: Optional[str] = Field(None, max_length=500)


class CertificationResponse(CertificationBase):
    """Schema for certification response."""

    id: UUID

    class Config:
        from_attributes = True
