"""
Rya AI API Router - Version 1
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas import RyaQuestionRequest, RyaAnswerResponse
from app.services import RyaAIService

router = APIRouter()


@router.post(
    "/ask",
    response_model=RyaAnswerResponse,
    status_code=status.HTTP_200_OK,
    summary="Ask Rya AI",
    description="Ask Rya, the AI assistant, a question about the portfolio owner.",
    responses={
        200: {
            "description": "AI response generated successfully",
            "content": {
                "application/json": {
                    "example": {
                        "answer": "Based on the portfolio, they specialize in Python, FastAPI, Flutter, and have extensive experience with PostgreSQL and cloud technologies."
                    }
                }
            },
        },
    },
)
async def ask_rya(
    request: RyaQuestionRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Ask Rya a question about the portfolio owner.
    
    Rya will answer based on the portfolio data including:
    - Personal information
    - Skills and technologies
    - Work experience
    - Projects
    - Certifications
    
    **Important**: Rya only answers using information available in the portfolio.
    If information is not available, Rya will politely indicate this.
    
    Example questions:
    - "What technologies does the portfolio owner use?"
    - "Tell me about their work experience"
    - "What projects have they worked on?"
    - "What certifications do they have?"
    """
    service = RyaAIService(db)
    answer = await service.ask_rya(request.question)
    return RyaAnswerResponse(answer=answer)
