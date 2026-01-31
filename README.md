# Portfolio Backend API v1

Production-ready FastAPI backend for a personal portfolio application with AI assistant (Rya).

## 🚀 Features

- **RESTful API** with versioned endpoints (`/api/v1/`)
- **PostgreSQL** database with async SQLAlchemy ORM
- **Alembic** database migrations
- **Gemini AI Integration** (Rya) - AI assistant that answers questions using portfolio data
- **Swagger/OpenAPI** auto-generated documentation
- **CORS** enabled for Flutter and web clients
- **JWT scaffolding** ready for future authentication

## 📦 Tech Stack

- **Python 3.11+**
- **FastAPI** - Modern async web framework
- **PostgreSQL** - Relational database
- **SQLAlchemy** - Async ORM
- **Alembic** - Database migrations
- **Pydantic** - Data validation
- **Google Gemini** - AI integration (gemini-2.5-flash)

## 🗄️ Database Schema

| Table | Description |
|-------|-------------|
| `personal_info` | Portfolio owner's information |
| `skills` | Technical skills with categories |
| `certifications` | Professional certifications |
| `projects` | Portfolio projects |
| `experience` | Work experience |
| `contact_requests` | Contact form submissions |
| `tags` | Tags for categorization |
| `ai_context_logs` | AI interaction logs |

## 🛠️ Setup Instructions

### 1. Prerequisites

- Python 3.11+
- PostgreSQL 14+
- Google Gemini API key

### 2. Clone and Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
# Copy example env file
copy .env.example .env  # Windows
# cp .env.example .env  # macOS/Linux

# Edit .env with your values
```

Required environment variables:
```env
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/portfolio_db
GEMINI_API_KEY=your-gemini-api-key
```

### 4. Setup Database

```bash
# Create PostgreSQL database
psql -U postgres
CREATE DATABASE portfolio_db;
\q

# Run migrations
alembic upgrade head

# OR use the SQL schema directly
psql -U postgres -d portfolio_db -f schema.sql
```

### 5. Run the Server

```bash
# Development mode
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production mode
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## 📚 API Documentation

Once the server is running, access:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/api/v1/openapi.json

## 🌐 API Endpoints

### Personal Info
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/personal` | Get personal info |
| POST | `/api/v1/personal` | Create personal info |
| PUT | `/api/v1/personal` | Update personal info |

### Skills
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/skills` | Get all skills |
| GET | `/api/v1/skills?category=backend` | Filter by category |
| POST | `/api/v1/skills` | Create skill |
| PUT | `/api/v1/skills/{id}` | Update skill |
| DELETE | `/api/v1/skills/{id}` | Delete skill |

### Certifications
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/certifications` | Get all certifications |
| POST | `/api/v1/certifications` | Create certification |
| PUT | `/api/v1/certifications/{id}` | Update certification |
| DELETE | `/api/v1/certifications/{id}` | Delete certification |

### Projects
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/projects` | Get all projects |
| GET | `/api/v1/projects?project_type=personal` | Filter by type |
| POST | `/api/v1/projects` | Create project |
| PUT | `/api/v1/projects/{id}` | Update project |
| DELETE | `/api/v1/projects/{id}` | Delete project |

### Experience
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/experience` | Get all experience |
| POST | `/api/v1/experience` | Create experience |
| PUT | `/api/v1/experience/{id}` | Update experience |
| DELETE | `/api/v1/experience/{id}` | Delete experience |

### Contact
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/contact` | Submit contact request |

### Rya AI Assistant
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/rya/ask` | Ask Rya a question |

## 🤖 Rya AI Assistant

Rya is an AI assistant powered by Google Gemini that answers questions about the portfolio using data from the database.

### Example Request
```json
POST /api/v1/rya/ask
{
  "question": "What technologies does Ramya use?"
}
```

### Example Response
```json
{
  "answer": "Based on the portfolio, Ramya specializes in Python, FastAPI, Flutter, PostgreSQL, and has experience with cloud technologies like AWS."
}
```

### AI Guardrails
- ✅ Only answers using portfolio data
- ✅ Politely declines if information is not available
- ✅ Never hallucinations
- ✅ Logs all interactions

## 📁 Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI application
│   ├── core/
│   │   ├── config.py        # Settings management
│   │   ├── database.py      # Database setup
│   │   ├── security.py      # JWT utilities
│   │   └── ai_client.py     # Gemini AI client
│   ├── models/
│   │   └── models.py        # SQLAlchemy models
│   ├── schemas/
│   │   ├── personal.py
│   │   ├── skills.py
│   │   ├── certifications.py
│   │   ├── projects.py
│   │   ├── experience.py
│   │   ├── contact.py
│   │   └── rya_ai.py
│   ├── services/
│   │   ├── personal_service.py
│   │   ├── skills_service.py
│   │   ├── certifications_service.py
│   │   ├── projects_service.py
│   │   ├── experience_service.py
│   │   ├── contact_service.py
│   │   └── rya_ai_service.py
│   ├── prompts/
│   │   └── rya_system_prompt.py
│   ├── utils/
│   └── versions/
│       └── v1/
│           └── routers/
├── alembic/
│   ├── env.py
│   └── versions/
├── alembic.ini
├── requirements.txt
├── schema.sql
├── .env.example
└── README.md
```

## 🔐 Security Notes

- Change `SECRET_KEY` in production
- Update CORS origins for production
- Use environment variables for sensitive data
- Enable HTTPS in production

## 🚀 Future Enhancements (v2)

- [ ] JWT Authentication
- [ ] Admin panel
- [ ] Analytics dashboard
- [ ] Image upload (Cloudinary/S3)
- [ ] Email notifications
- [ ] Rate limiting

## 📄 License

MIT License

---

Built with ❤️ for the portfolio application
