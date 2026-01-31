"""
Gemini AI Client for Rya AI Assistant.
"""

import google.generativeai as genai
from typing import Optional
from app.core.config import settings


class GeminiClient:
    """Client for interacting with Google Gemini AI."""

    def __init__(self):
        """Initialize the Gemini client."""
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(settings.GEMINI_MODEL)

    async def generate_response(
        self,
        user_question: str,
        context: str,
        system_prompt: str,
    ) -> str:
        """
        Generate AI response using Gemini.
        
        Args:
            user_question: The user's question
            context: Relevant data from the portfolio database
            system_prompt: System instructions for the AI
            
        Returns:
            AI-generated response string
        """
        try:
            full_prompt = f"""
{system_prompt}

PORTFOLIO DATA CONTEXT:
{context}

USER QUESTION:
{user_question}

INSTRUCTIONS:
- Answer ONLY using the portfolio data provided above
- If the information is not available in the context, politely say so
- Be helpful, professional, and concise
- Speak as if you know the portfolio owner personally
- Never make up information that isn't in the context

RESPONSE:
"""
            response = self.model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            return f"I apologize, but I'm having trouble processing your request right now. Error: {str(e)}"


# Singleton instance
gemini_client = GeminiClient()


def get_gemini_client() -> GeminiClient:
    """Get the Gemini client instance."""
    return gemini_client
