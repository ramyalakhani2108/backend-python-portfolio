"""
Contact API Router - Version 1
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas import ContactRequestResponse, ContactRequestCreate
from app.services import ContactService

router = APIRouter()


@router.post(
    "",
    response_model=ContactRequestResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Submit Contact Request",
    description="Submit a contact request to the portfolio owner.",
    responses={
        201: {"description": "Contact request submitted successfully"},
    },
)
async def submit_contact_request(
    data: ContactRequestCreate,
    db: AsyncSession = Depends(get_db),
):
    """
    Submit a contact request.
    
    - **name**: Your name
    - **email**: Your email address
    - **message**: Your message (minimum 10 characters)
    
    The portfolio owner will receive your message and may respond via email.
    """
    service = ContactService(db)
    return await service.create_contact_request(data)
