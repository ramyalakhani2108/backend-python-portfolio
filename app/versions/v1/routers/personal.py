"""
Personal Info API Router - Version 1
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas import PersonalInfoResponse, PersonalInfoCreate, PersonalInfoUpdate
from app.services import PersonalInfoService

router = APIRouter()


@router.get(
    "",
    response_model=PersonalInfoResponse,
    summary="Get Personal Information",
    description="Retrieve the portfolio owner's personal information.",
    responses={
        200: {"description": "Personal information retrieved successfully"},
        404: {"description": "Personal information not found"},
    },
)
async def get_personal_info(db: AsyncSession = Depends(get_db)):
    """
    Get the personal information of the portfolio owner.
    
    Returns the single personal info record.
    """
    service = PersonalInfoService(db)
    personal_info = await service.get_personal_info()
    
    if not personal_info:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Personal information not found. Please create one first.",
        )
    
    return personal_info


@router.post(
    "",
    response_model=PersonalInfoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Personal Information",
    description="Create the portfolio owner's personal information.",
    responses={
        201: {"description": "Personal information created successfully"},
        400: {"description": "Personal information already exists"},
    },
)
async def create_personal_info(
    data: PersonalInfoCreate,
    db: AsyncSession = Depends(get_db),
):
    """
    Create personal information for the portfolio owner.
    
    Only one personal info record can exist.
    """
    service = PersonalInfoService(db)
    existing = await service.get_personal_info()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Personal information already exists. Use PUT to update.",
        )
    
    return await service.create_personal_info(data)


@router.put(
    "",
    response_model=PersonalInfoResponse,
    summary="Update Personal Information",
    description="Update the portfolio owner's personal information.",
    responses={
        200: {"description": "Personal information updated successfully"},
        404: {"description": "Personal information not found"},
    },
)
async def update_personal_info(
    data: PersonalInfoUpdate,
    db: AsyncSession = Depends(get_db),
):
    """
    Update the personal information of the portfolio owner.
    
    Partial updates are supported - only provided fields will be updated.
    """
    service = PersonalInfoService(db)
    existing = await service.get_personal_info()
    
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Personal information not found. Please create one first.",
        )
    
    updated = await service.update_personal_info(existing.id, data)
    return updated
