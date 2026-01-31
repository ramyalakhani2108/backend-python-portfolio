"""
Pydantic schemas for Rya AI Assistant.
"""

from datetime import datetime
from typing import Optional, Dict, Any
from uuid import UUID
from pydantic import BaseModel, Field


class RyaQuestionRequest(BaseModel):
    """Schema for asking Rya a question."""

    question: str = Field(
        ...,
        min_length=1,
        example="What technologies does Ramya use?",
        description="The question to ask Rya about the portfolio owner.",
    )


class RyaAnswerResponse(BaseModel):
    """Schema for Rya's answer response."""

    answer: str = Field(
        ...,
        example="Ramya specializes in NestJS, PostgreSQL, Flutter, and has experience with cloud technologies like AWS.",
    )


class AIContextLogResponse(BaseModel):
    """Schema for AI context log response."""

    id: UUID
    user_question: str
    ai_response: str
    used_context: Optional[Dict[str, Any]]
    created_at: datetime

    class Config:
        from_attributes = True
