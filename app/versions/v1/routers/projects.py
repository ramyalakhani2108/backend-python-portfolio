"""
Projects API Router - Version 1
"""

from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas import ProjectResponse, ProjectCreate, ProjectUpdate, ProjectType
from app.services import ProjectService

router = APIRouter()


@router.get(
    "",
    response_model=List[ProjectResponse],
    summary="Get All Projects",
    description="Retrieve all projects with optional type filtering.",
    responses={
        200: {"description": "Projects retrieved successfully"},
    },
)
async def get_projects(
    project_type: Optional[ProjectType] = Query(
        None, description="Filter by project type (personal/professional)"
    ),
    db: AsyncSession = Depends(get_db),
):
    """
    Get all projects.
    
    Optionally filter by project type (personal, professional).
    """
    service = ProjectService(db)
    
    if project_type:
        return await service.get_projects_by_type(project_type.value)
    
    return await service.get_all_projects()


@router.get(
    "/{project_id}",
    response_model=ProjectResponse,
    summary="Get Project by ID",
    description="Retrieve a specific project by its ID.",
    responses={
        200: {"description": "Project retrieved successfully"},
        404: {"description": "Project not found"},
    },
)
async def get_project(project_id: UUID, db: AsyncSession = Depends(get_db)):
    """Get a specific project by ID."""
    service = ProjectService(db)
    project = await service.get_project_by_id(project_id)
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
    
    return project


@router.post(
    "",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Project",
    description="Add a new project to the portfolio.",
    responses={
        201: {"description": "Project created successfully"},
    },
)
async def create_project(data: ProjectCreate, db: AsyncSession = Depends(get_db)):
    """
    Create a new project.
    
    - **title**: Project title
    - **description**: Detailed description
    - **tech_stack**: List of technologies used
    - **github_url**: GitHub repository URL
    - **live_url**: Live demo URL
    - **project_type**: personal or professional
    """
    service = ProjectService(db)
    return await service.create_project(data)


@router.put(
    "/{project_id}",
    response_model=ProjectResponse,
    summary="Update Project",
    description="Update an existing project.",
    responses={
        200: {"description": "Project updated successfully"},
        404: {"description": "Project not found"},
    },
)
async def update_project(
    project_id: UUID,
    data: ProjectUpdate,
    db: AsyncSession = Depends(get_db),
):
    """Update an existing project."""
    service = ProjectService(db)
    project = await service.update_project(project_id, data)
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
    
    return project


@router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Project",
    description="Remove a project from the portfolio.",
    responses={
        204: {"description": "Project deleted successfully"},
        404: {"description": "Project not found"},
    },
)
async def delete_project(project_id: UUID, db: AsyncSession = Depends(get_db)):
    """Delete a project."""
    service = ProjectService(db)
    deleted = await service.delete_project(project_id)
    
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
