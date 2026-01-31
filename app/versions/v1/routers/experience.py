"""
Experience API Router - Version 1
"""

from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas import ExperienceResponse, ExperienceCreate, ExperienceUpdate
from app.services import ExperienceService

router = APIRouter()


@router.get(
    "",
    response_model=List[ExperienceResponse],
    summary="Get All Experience",
    description="Retrieve all work experience entries.",
    responses={
        200: {"description": "Experience entries retrieved successfully"},
    },
)
async def get_experiences(db: AsyncSession = Depends(get_db)):
    """Get all work experience entries, ordered by start date (newest first)."""
    service = ExperienceService(db)
    return await service.get_all_experiences()


@router.get(
    "/{exp_id}",
    response_model=ExperienceResponse,
    summary="Get Experience by ID",
    description="Retrieve a specific experience entry by its ID.",
    responses={
        200: {"description": "Experience entry retrieved successfully"},
        404: {"description": "Experience entry not found"},
    },
)
async def get_experience(exp_id: UUID, db: AsyncSession = Depends(get_db)):
    """Get a specific experience entry by ID."""
    service = ExperienceService(db)
    experience = await service.get_experience_by_id(exp_id)
    
    if not experience:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Experience entry not found",
        )
    
    return experience


@router.post(
    "",
    response_model=ExperienceResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Experience",
    description="Add a new work experience entry.",
    responses={
        201: {"description": "Experience entry created successfully"},
    },
)
async def create_experience(data: ExperienceCreate, db: AsyncSession = Depends(get_db)):
    """
    Create a new work experience entry.
    
    - **company_name**: Name of the company
    - **role**: Job title/role
    - **description**: Description of responsibilities
    - **start_date**: Start date of employment
    - **end_date**: End date (null for current position)
    - **learnings**: Key learnings from this role
    """
    service = ExperienceService(db)
    return await service.create_experience(data)


@router.put(
    "/{exp_id}",
    response_model=ExperienceResponse,
    summary="Update Experience",
    description="Update an existing experience entry.",
    responses={
        200: {"description": "Experience entry updated successfully"},
        404: {"description": "Experience entry not found"},
    },
)
async def update_experience(
    exp_id: UUID,
    data: ExperienceUpdate,
    db: AsyncSession = Depends(get_db),
):
    """Update an existing experience entry."""
    service = ExperienceService(db)
    experience = await service.update_experience(exp_id, data)
    
    if not experience:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Experience entry not found",
        )
    
    return experience


@router.delete(
    "/{exp_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Experience",
    description="Remove an experience entry from the portfolio.",
    responses={
        204: {"description": "Experience entry deleted successfully"},
        404: {"description": "Experience entry not found"},
    },
)
async def delete_experience(exp_id: UUID, db: AsyncSession = Depends(get_db)):
    """Delete an experience entry."""
    service = ExperienceService(db)
    deleted = await service.delete_experience(exp_id)
    
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Experience entry not found",
        )
