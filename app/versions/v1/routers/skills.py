"""
Skills API Router - Version 1
"""

from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas import SkillResponse, SkillCreate, SkillUpdate, SkillCategory
from app.services import SkillService

router = APIRouter()


@router.get(
    "",
    response_model=List[SkillResponse],
    summary="Get All Skills",
    description="Retrieve all skills with optional category filtering.",
    responses={
        200: {"description": "Skills retrieved successfully"},
    },
)
async def get_skills(
    category: Optional[SkillCategory] = Query(
        None, description="Filter by skill category"
    ),
    db: AsyncSession = Depends(get_db),
):
    """
    Get all skills.
    
    Optionally filter by category (backend, frontend, devops, other).
    """
    service = SkillService(db)
    
    if category:
        return await service.get_skills_by_category(category.value)
    
    return await service.get_all_skills()


@router.get(
    "/{skill_id}",
    response_model=SkillResponse,
    summary="Get Skill by ID",
    description="Retrieve a specific skill by its ID.",
    responses={
        200: {"description": "Skill retrieved successfully"},
        404: {"description": "Skill not found"},
    },
)
async def get_skill(skill_id: UUID, db: AsyncSession = Depends(get_db)):
    """Get a specific skill by ID."""
    service = SkillService(db)
    skill = await service.get_skill_by_id(skill_id)
    
    if not skill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Skill not found",
        )
    
    return skill


@router.post(
    "",
    response_model=SkillResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Skill",
    description="Add a new skill to the portfolio.",
    responses={
        201: {"description": "Skill created successfully"},
    },
)
async def create_skill(data: SkillCreate, db: AsyncSession = Depends(get_db)):
    """
    Create a new skill.
    
    - **name**: Name of the skill (e.g., "Python", "React")
    - **category**: Category (backend, frontend, devops, other)
    - **proficiency_level**: Level from 1-100
    - **is_hobby**: Whether this is a hobby skill
    """
    service = SkillService(db)
    return await service.create_skill(data)


@router.put(
    "/{skill_id}",
    response_model=SkillResponse,
    summary="Update Skill",
    description="Update an existing skill.",
    responses={
        200: {"description": "Skill updated successfully"},
        404: {"description": "Skill not found"},
    },
)
async def update_skill(
    skill_id: UUID,
    data: SkillUpdate,
    db: AsyncSession = Depends(get_db),
):
    """Update an existing skill."""
    service = SkillService(db)
    skill = await service.update_skill(skill_id, data)
    
    if not skill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Skill not found",
        )
    
    return skill


@router.delete(
    "/{skill_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Skill",
    description="Remove a skill from the portfolio.",
    responses={
        204: {"description": "Skill deleted successfully"},
        404: {"description": "Skill not found"},
    },
)
async def delete_skill(skill_id: UUID, db: AsyncSession = Depends(get_db)):
    """Delete a skill."""
    service = SkillService(db)
    deleted = await service.delete_skill(skill_id)
    
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Skill not found",
        )
