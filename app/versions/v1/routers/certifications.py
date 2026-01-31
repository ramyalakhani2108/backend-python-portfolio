"""
Certifications API Router - Version 1
"""

from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas import CertificationResponse, CertificationCreate, CertificationUpdate
from app.services import CertificationService

router = APIRouter()


@router.get(
    "",
    response_model=List[CertificationResponse],
    summary="Get All Certifications",
    description="Retrieve all certifications.",
    responses={
        200: {"description": "Certifications retrieved successfully"},
    },
)
async def get_certifications(db: AsyncSession = Depends(get_db)):
    """Get all certifications."""
    service = CertificationService(db)
    return await service.get_all_certifications()


@router.get(
    "/{cert_id}",
    response_model=CertificationResponse,
    summary="Get Certification by ID",
    description="Retrieve a specific certification by its ID.",
    responses={
        200: {"description": "Certification retrieved successfully"},
        404: {"description": "Certification not found"},
    },
)
async def get_certification(cert_id: UUID, db: AsyncSession = Depends(get_db)):
    """Get a specific certification by ID."""
    service = CertificationService(db)
    certification = await service.get_certification_by_id(cert_id)
    
    if not certification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Certification not found",
        )
    
    return certification


@router.post(
    "",
    response_model=CertificationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Certification",
    description="Add a new certification to the portfolio.",
    responses={
        201: {"description": "Certification created successfully"},
    },
)
async def create_certification(
    data: CertificationCreate,
    db: AsyncSession = Depends(get_db),
):
    """
    Create a new certification.
    
    - **title**: Certification title
    - **issuer**: Organization that issued the certification
    - **issue_date**: Date the certification was issued
    - **credential_url**: URL to verify the credential
    """
    service = CertificationService(db)
    return await service.create_certification(data)


@router.put(
    "/{cert_id}",
    response_model=CertificationResponse,
    summary="Update Certification",
    description="Update an existing certification.",
    responses={
        200: {"description": "Certification updated successfully"},
        404: {"description": "Certification not found"},
    },
)
async def update_certification(
    cert_id: UUID,
    data: CertificationUpdate,
    db: AsyncSession = Depends(get_db),
):
    """Update an existing certification."""
    service = CertificationService(db)
    certification = await service.update_certification(cert_id, data)
    
    if not certification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Certification not found",
        )
    
    return certification


@router.delete(
    "/{cert_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Certification",
    description="Remove a certification from the portfolio.",
    responses={
        204: {"description": "Certification deleted successfully"},
        404: {"description": "Certification not found"},
    },
)
async def delete_certification(cert_id: UUID, db: AsyncSession = Depends(get_db)):
    """Delete a certification."""
    service = CertificationService(db)
    deleted = await service.delete_certification(cert_id)
    
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Certification not found",
        )
