"""
Rya AI Service - AI Assistant business logic layer.
"""

from typing import Dict, Any, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import (
    PersonalInfo,
    Skill,
    Certification,
    Project,
    Experience,
    AIContextLog,
)
from app.core.ai_client import get_gemini_client
from app.prompts.rya_system_prompt import RYA_SYSTEM_PROMPT


class RyaAIService:
    """Service class for Rya AI assistant operations."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.gemini_client = get_gemini_client()

    async def _fetch_portfolio_context(self) -> Dict[str, Any]:
        """Fetch all relevant portfolio data for AI context."""
        context = {}

        # Fetch personal info
        personal_result = await self.db.execute(select(PersonalInfo).limit(1))
        personal_info = personal_result.scalar_one_or_none()
        if personal_info:
            context["personal_info"] = {
                "name": personal_info.name,
                "place": personal_info.place,
                "country": personal_info.country,
                "email": personal_info.email,
                "bio": personal_info.bio,
            }

        # Fetch skills
        skills_result = await self.db.execute(select(Skill))
        skills = skills_result.scalars().all()
        context["skills"] = [
            {
                "name": s.name,
                "category": s.category,
                "proficiency_level": s.proficiency_level,
                "is_hobby": s.is_hobby,
            }
            for s in skills
        ]

        # Fetch certifications
        certs_result = await self.db.execute(select(Certification))
        certifications = certs_result.scalars().all()
        context["certifications"] = [
            {
                "title": c.title,
                "issuer": c.issuer,
                "issue_date": str(c.issue_date) if c.issue_date else None,
            }
            for c in certifications
        ]

        # Fetch projects
        projects_result = await self.db.execute(select(Project))
        projects = projects_result.scalars().all()
        context["projects"] = [
            {
                "title": p.title,
                "description": p.description,
                "tech_stack": p.tech_stack,
                "project_type": p.project_type,
                "github_url": p.github_url,
                "live_url": p.live_url,
            }
            for p in projects
        ]

        # Fetch experience
        exp_result = await self.db.execute(select(Experience))
        experiences = exp_result.scalars().all()
        context["experience"] = [
            {
                "company_name": e.company_name,
                "role": e.role,
                "description": e.description,
                "start_date": str(e.start_date) if e.start_date else None,
                "end_date": str(e.end_date) if e.end_date else None,
                "learnings": e.learnings,
            }
            for e in experiences
        ]

        return context

    def _format_context_for_prompt(self, context: Dict[str, Any]) -> str:
        """Format the context dictionary into a readable string for the AI prompt."""
        formatted_parts = []

        if "personal_info" in context and context["personal_info"]:
            info = context["personal_info"]
            formatted_parts.append(f"""
PERSONAL INFORMATION:
- Name: {info.get('name', 'N/A')}
- Location: {info.get('place', 'N/A')}, {info.get('country', 'N/A')}
- Email: {info.get('email', 'N/A')}
- Bio: {info.get('bio', 'N/A')}
""")

        if "skills" in context and context["skills"]:
            skills_text = "\nSKILLS:\n"
            for skill in context["skills"]:
                skills_text += f"- {skill['name']} ({skill['category']}) - Proficiency: {skill.get('proficiency_level', 'N/A')}%"
                if skill.get('is_hobby'):
                    skills_text += " [Hobby]"
                skills_text += "\n"
            formatted_parts.append(skills_text)

        if "certifications" in context and context["certifications"]:
            certs_text = "\nCERTIFICATIONS:\n"
            for cert in context["certifications"]:
                certs_text += f"- {cert['title']} by {cert['issuer']}"
                if cert.get('issue_date'):
                    certs_text += f" (Issued: {cert['issue_date']})"
                certs_text += "\n"
            formatted_parts.append(certs_text)

        if "projects" in context and context["projects"]:
            projects_text = "\nPROJECTS:\n"
            for project in context["projects"]:
                projects_text += f"- {project['title']} ({project['project_type']})\n"
                projects_text += f"  Description: {project.get('description', 'N/A')}\n"
                if project.get('tech_stack'):
                    projects_text += f"  Technologies: {', '.join(project['tech_stack'])}\n"
            formatted_parts.append(projects_text)

        if "experience" in context and context["experience"]:
            exp_text = "\nWORK EXPERIENCE:\n"
            for exp in context["experience"]:
                exp_text += f"- {exp['role']} at {exp['company_name']}\n"
                if exp.get('start_date'):
                    end = exp.get('end_date', 'Present')
                    exp_text += f"  Duration: {exp['start_date']} - {end}\n"
                if exp.get('description'):
                    exp_text += f"  Description: {exp['description']}\n"
                if exp.get('learnings'):
                    exp_text += f"  Key Learnings: {exp['learnings']}\n"
            formatted_parts.append(exp_text)

        return "\n".join(formatted_parts) if formatted_parts else "No portfolio data available."

    async def ask_rya(self, question: str) -> str:
        """
        Ask Rya a question about the portfolio.
        
        Args:
            question: The user's question
            
        Returns:
            AI-generated response
        """
        # Fetch portfolio context
        context = await self._fetch_portfolio_context()
        formatted_context = self._format_context_for_prompt(context)

        # Generate AI response
        response = await self.gemini_client.generate_response(
            user_question=question,
            context=formatted_context,
            system_prompt=RYA_SYSTEM_PROMPT,
        )

        # Log the interaction
        await self._log_interaction(question, response, context)

        return response

    async def _log_interaction(
        self, question: str, response: str, context: Dict[str, Any]
    ) -> AIContextLog:
        """Log the AI interaction to the database."""
        log = AIContextLog(
            user_question=question,
            ai_response=response,
            used_context=context,
        )
        self.db.add(log)
        await self.db.flush()
        return log
