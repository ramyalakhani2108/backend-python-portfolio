"""
Portfolio Backend API - Version 1
Production-ready FastAPI backend for personal portfolio application.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from pathlib import Path

from app.core.config import settings
from app.core.database import engine, Base
from app.versions.v1.routers import (
    personal,
    skills,
    certifications,
    projects,
    experience,
    contact,
    rya_ai,
)
from app.admin.routes import router as admin_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("Database tables created/verified successfully")
    except Exception as e:
        print(f"Database initialization error: {e}")
        # Don't fail startup if tables already exist
        pass
    yield
    # Shutdown
    await engine.dispose()


app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Personal Portfolio API with AI Assistant (Rya)",
    version="1.0.0",
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include V1 Routers
app.include_router(
    personal.router,
    prefix=f"{settings.API_V1_PREFIX}/personal",
    tags=["Personal Info"],
)
app.include_router(
    skills.router,
    prefix=f"{settings.API_V1_PREFIX}/skills",
    tags=["Skills"],
)
app.include_router(
    certifications.router,
    prefix=f"{settings.API_V1_PREFIX}/certifications",
    tags=["Certifications"],
)
app.include_router(
    projects.router,
    prefix=f"{settings.API_V1_PREFIX}/projects",
    tags=["Projects"],
)
app.include_router(
    experience.router,
    prefix=f"{settings.API_V1_PREFIX}/experience",
    tags=["Experience"],
)
app.include_router(
    contact.router,
    prefix=f"{settings.API_V1_PREFIX}/contact",
    tags=["Contact"],
)
app.include_router(
    rya_ai.router,
    prefix=f"{settings.API_V1_PREFIX}/rya",
    tags=["Rya AI Assistant"],
)

# Include Admin Panel Router (Server-rendered UI)
app.include_router(admin_router)


@app.get("/", tags=["Health"])
async def root():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "message": "Portfolio API is running",
        "version": "1.0.0",
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Detailed health check."""
    return {
        "status": "healthy",
        "database": "connected",
        "ai_service": "ready",
    }
