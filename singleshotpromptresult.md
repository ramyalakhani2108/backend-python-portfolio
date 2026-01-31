User: Follow instructions in [single-shot.prompt.md](file:///d%3A/portfolio-application/portfolio/.github/prompts/single-shot.prompt.md).

GitHub Copilot: I'll create a production-ready FastAPI backend for your portfolio application following the master prompt instructions. Let me set up the complete project structure. 

Created 8 todos

Created [](file:///d%3A/portfolio-application/backend/app/main.py)

Created [](file:///d%3A/portfolio-application/backend/app/core/config.py)

Created [](file:///d%3A/portfolio-application/backend/app/core/database.py)

Created [](file:///d%3A/portfolio-application/backend/app/core/security.py)

Created [](file:///d%3A/portfolio-application/backend/app/core/ai_client.py)

Created [](file:///d%3A/portfolio-application/backend/app/core/__init__.py)

Starting: *Create database models* (2/8)

Created [](file:///d%3A/portfolio-application/backend/app/models/models.py)

Created [](file:///d%3A/portfolio-application/backend/app/models/__init__.py)

Starting: *Create Pydantic schemas* (3/8)

Created [](file:///d%3A/portfolio-application/backend/app/schemas/personal.py)

Created [](file:///d%3A/portfolio-application/backend/app/schemas/skills.py)

Created [](file:///d%3A/portfolio-application/backend/app/schemas/certifications.py)

Created [](file:///d%3A/portfolio-application/backend/app/schemas/projects.py)

Created [](file:///d%3A/portfolio-application/backend/app/schemas/experience.py)

Created [](file:///d%3A/portfolio-application/backend/app/schemas/contact.py)

Created [](file:///d%3A/portfolio-application/backend/app/schemas/rya_ai.py)

Created [](file:///d%3A/portfolio-application/backend/app/schemas/tags.py)

Created [](file:///d%3A/portfolio-application/backend/app/schemas/__init__.py)

Starting: *Create API routers* (4/8)

Created [](file:///d%3A/portfolio-application/backend/app/services/personal_service.py)

Created [](file:///d%3A/portfolio-application/backend/app/services/skills_service.py)

Created [](file:///d%3A/portfolio-application/backend/app/services/certifications_service.py)

Created [](file:///d%3A/portfolio-application/backend/app/services/projects_service.py)

Continue to iterate?
[object Object]

Made changes.

User: @agent Continue: "Continue to iterate?"

GitHub Copilot: Created [](file:///d%3A/portfolio-application/backend/app/services/experience_service.py)

Created [](file:///d%3A/portfolio-application/backend/app/services/contact_service.py)

Created [](file:///d%3A/portfolio-application/backend/app/services/rya_ai_service.py)

Created [](file:///d%3A/portfolio-application/backend/app/services/__init__.py)

Created [](file:///d%3A/portfolio-application/backend/app/prompts/rya_system_prompt.py)

Created [](file:///d%3A/portfolio-application/backend/app/prompts/__init__.py)

Now let me create the API routers: 

Created [](file:///d%3A/portfolio-application/backend/app/versions/v1/routers/personal.py)

Created [](file:///d%3A/portfolio-application/backend/app/versions/v1/routers/skills.py)

Created [](file:///d%3A/portfolio-application/backend/app/versions/v1/routers/certifications.py)

Created [](file:///d%3A/portfolio-application/backend/app/versions/v1/routers/projects.py)

Created [](file:///d%3A/portfolio-application/backend/app/versions/v1/routers/experience.py)

Created [](file:///d%3A/portfolio-application/backend/app/versions/v1/routers/contact.py)

Created [](file:///d%3A/portfolio-application/backend/app/versions/v1/routers/rya_ai.py)

Created [](file:///d%3A/portfolio-application/backend/app/versions/v1/routers/__init__.py)

Created [](file:///d%3A/portfolio-application/backend/app/versions/v1/__init__.py)

Created [](file:///d%3A/portfolio-application/backend/app/versions/__init__.py)

Created [](file:///d%3A/portfolio-application/backend/app/utils/__init__.py)

Created [](file:///d%3A/portfolio-application/backend/app/__init__.py)

Starting: *Create Alembic migrations* (7/8)

Now let me create the Alembic configuration and migrations: 

Created [](file:///d%3A/portfolio-application/backend/alembic.ini)

Created [](file:///d%3A/portfolio-application/backend/alembic/env.py)

Created [](file:///d%3A/portfolio-application/backend/alembic/script.py.mako)

Created [](file:///d%3A/portfolio-application/backend/alembic/versions/001_initial_migration.py)

Starting: *Create SQL schema and README* (8/8)

Created [](file:///d%3A/portfolio-application/backend/schema.sql)

Created [](file:///d%3A/portfolio-application/backend/.env.example)

Created [](file:///d%3A/portfolio-application/backend/.gitignore)

Created [](file:///d%3A/portfolio-application/backend/requirements.txt)

Created [](file:///d%3A/portfolio-application/backend/README.md)

Completed: *Create SQL schema and README* (8/8)

I've created a complete **production-ready FastAPI backend** for your portfolio application. Here's a summary of what was created:

## 📦 Backend Structure

**Location:** backend

### Core Files Created:

| Component | Files |
|-----------|-------|
| **Main App** | app/main.py - FastAPI app with CORS & routers |
| **Config** | app/core/config.py, database.py, security.py, ai_client.py |
| **Models** | app/models/models.py - All 8 database tables |
| **Schemas** | 7 Pydantic schema files for validation |
| **Services** | 7 service files with business logic |
| **Routers** | 7 versioned API routers under `/api/v1/` |
| **AI Prompts** | app/prompts/rya_system_prompt.py |
| **Migrations** | alembic/ with initial migration |

### API Endpoints:

- `GET/POST/PUT /api/v1/personal` - Personal info
- `GET/POST/PUT/DELETE /api/v1/skills` - Skills
- `GET/POST/PUT/DELETE /api/v1/certifications` - Certifications
- `GET/POST/PUT/DELETE /api/v1/projects` - Projects
- `GET/POST/PUT/DELETE /api/v1/experience` - Experience
- `POST /api/v1/contact` - Contact requests
- `POST /api/v1/rya/ask` - **Rya AI Assistant**

### Quick Start:

```bash
cd d:\portfolio-application\backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
# Edit .env with your GEMINI_API_KEY and DATABASE_URL
uvicorn app.main:app --reload
```

Then visit **http://localhost:8000/docs** for Swagger documentation!

Made changes.