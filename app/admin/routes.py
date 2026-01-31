"""
Admin Panel Routes
Server-rendered UI using FastAPI + Jinja2.
"""

from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from typing import Optional
import logging

from app.admin.auth import (
    AdminAuth,
    get_current_admin,
    login_required,
)
from app.admin.services import admin_api_service

# Setup templates
templates_path = Path(__file__).parent / "templates"
templates = Jinja2Templates(directory=str(templates_path))

router = APIRouter(prefix="/admin", tags=["Admin Panel"])

logger = logging.getLogger(__name__)


def _norm(value: Optional[str]) -> Optional[str]:
    """Normalize form inputs: strip strings and convert empty->None."""
    if value is None:
        return None
    if isinstance(value, str):
        v = value.strip()
        return v if v != "" else None
    return value


# ==================== Auth Routes ====================

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Render the login page."""
    admin = get_current_admin(request)
    if admin:
        return RedirectResponse(url="/admin/dashboard", status_code=302)
    
    return templates.TemplateResponse(
        "login.html",
        {"request": request, "error": None}
    )


@router.post("/login", response_class=HTMLResponse)
async def login_submit(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
):
    """Handle login form submission."""
    token = AdminAuth.login(username, password)
    
    if token:
        return AdminAuth.login_response(token)
    
    return templates.TemplateResponse(
        "login.html",
        {"request": request, "error": "Invalid username or password"}
    )


@router.get("/logout")
async def logout(request: Request):
    """Log out the admin user."""
    return AdminAuth.logout_response()


# ==================== Dashboard ====================

@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Render the admin dashboard."""
    admin = get_current_admin(request)
    if not admin:
        return RedirectResponse(url="/admin/login", status_code=302)
    
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "admin": admin}
    )


# ==================== Personal Info ====================

@router.get("/personal", response_class=HTMLResponse)
async def personal_page(request: Request):
    """Render the personal info management page."""
    admin = get_current_admin(request)
    if not admin:
        return RedirectResponse(url="/admin/login", status_code=302)
    
    personal_info = await admin_api_service.get_personal_info()
    is_new = personal_info.get("error", False)
    
    return templates.TemplateResponse(
        "personal.html",
        {
            "request": request,
            "admin": admin,
            "personal_info": personal_info if not is_new else {},
            "is_new": is_new,
            "message": None,
            "error": None,
        }
    )


@router.post("/personal")
async def personal_submit(
    request: Request,
    name: str = Form(...),
    title: str = Form(...),
    bio: str = Form(...),
    email: str = Form(...),
    phone: Optional[str] = Form(None),
    place: Optional[str] = Form(None),
    country: Optional[str] = Form(None),
    profile_image_url: Optional[str] = Form(None),
    github_url: Optional[str] = Form(None),
    linkedin_url: Optional[str] = Form(None),
    twitter_url: Optional[str] = Form(None),
    website_url: Optional[str] = Form(None),
    is_update: str = Form("false"),
):
    """Handle personal info form submission with normalization + validation."""
    admin = get_current_admin(request)
    if not admin:
        return RedirectResponse(url="/admin/login", status_code=302)

    # Normalize inputs
    name = _norm(name)
    title = _norm(title)
    bio = _norm(bio)
    email = _norm(email)
    phone = _norm(phone)
    place = _norm(place)
    country = _norm(country)
    profile_image_url = _norm(profile_image_url)
    github_url = _norm(github_url)
    linkedin_url = _norm(linkedin_url)
    twitter_url = _norm(twitter_url)
    website_url = _norm(website_url)

    # Server-side validation for required fields
    if not name or not title or not email or not bio:
        certifications = await admin_api_service.get_certifications()  # reuse a safe call to populate template
        return templates.TemplateResponse(
            "personal.html",
            {
                "request": request,
                "admin": admin,
                "personal_info": {
                    "name": name,
                    "title": title,
                    "email": email,
                    "bio": bio,
                },
                "is_new": True,
                "message": None,
                "error": "Please fill all required fields (name, title, email, bio).",
            },
        )

    data = {
        "name": name,
        "title": title,
        "bio": bio,
        "email": email,
        "phone": phone,
        "place": place,
        "country": country,
        "profile_image_url": profile_image_url,
        "github_url": github_url,
        "linkedin_url": linkedin_url,
        "twitter_url": twitter_url,
        "website_url": website_url,
    }

    try:
        if is_update == "true":
            result = await admin_api_service.update_personal_info(data)
        else:
            result = await admin_api_service.create_personal_info(data)
    except Exception as exc:
        logger.exception("admin -> create_personal_info failed")
        return templates.TemplateResponse(
            "personal.html",
            {
                "request": request,
                "admin": admin,
                "personal_info": data,
                "is_new": True,
                "message": None,
                "error": f"API error: {str(exc)}",
            },
        )

    error = result.get("error")
    message = None if error else "Personal information saved successfully!"

    return templates.TemplateResponse(
        "personal.html",
        {
            "request": request,
            "admin": admin,
            "personal_info": result if not error else data,
            "is_new": error,
            "message": message,
            "error": result.get("detail") if error else None,
        },
    )


# ==================== Skills ====================

@router.get("/skills", response_class=HTMLResponse)
async def skills_page(request: Request):
    """Render the skills management page."""
    admin = get_current_admin(request)
    if not admin:
        return RedirectResponse(url="/admin/login", status_code=302)
    
    skills = await admin_api_service.get_skills()
    
    return templates.TemplateResponse(
        "skills.html",
        {
            "request": request,
            "admin": admin,
            "skills": skills,
            "message": request.query_params.get("message"),
            "error": request.query_params.get("error"),
        }
    )


@router.post("/skills", response_class=HTMLResponse)
async def skills_submit(
    request: Request,
    name: str = Form(...),
    category: str = Form(...),
    proficiency_level: int = Form(...),
    is_hobby: bool = Form(False),
):
    """Handle skill creation form submission."""
    admin = get_current_admin(request)
    if not admin:
        return RedirectResponse(url="/admin/login", status_code=302)
    
    data = {
        "name": name,
        "category": category,
        "proficiency_level": proficiency_level,
        "is_hobby": is_hobby,
    }
    
    result = await admin_api_service.create_skill(data)
    error = result.get("error")
    
    if error:
        skills = await admin_api_service.get_skills()
        return templates.TemplateResponse(
            "skills.html",
            {
                "request": request,
                "admin": admin,
                "skills": skills,
                "message": None,
                "error": result.get("detail"),
            }
        )
    
    return RedirectResponse(
        url="/admin/skills?message=Skill+created+successfully",
        status_code=302
    )


@router.get("/skills/{skill_id}/delete")
async def skills_delete(request: Request, skill_id: str):
    """Delete a skill."""
    admin = get_current_admin(request)
    if not admin:
        return RedirectResponse(url="/admin/login", status_code=302)
    
    result = await admin_api_service.delete_skill(skill_id)
    error = result.get("error")
    
    if error:
        return RedirectResponse(
            url=f"/admin/skills?error={result.get('detail')}",
            status_code=302
        )
    
    return RedirectResponse(
        url="/admin/skills?message=Skill+deleted+successfully",
        status_code=302
    )


# ==================== Certifications ====================

@router.get("/certifications", response_class=HTMLResponse)
async def certifications_page(request: Request):
    """Render the certifications management page."""
    admin = get_current_admin(request)
    if not admin:
        return RedirectResponse(url="/admin/login", status_code=302)
    
    certifications = await admin_api_service.get_certifications()
    
    return templates.TemplateResponse(
        "certifications.html",
        {
            "request": request,
            "admin": admin,
            "certifications": certifications,
            "message": request.query_params.get("message"),
            "error": request.query_params.get("error"),
        }
    )


@router.post("/certifications")
async def certifications_submit(
    request: Request,
    title: str = Form(...),
    issuer: str = Form(...),
    issue_date: str = Form(...),
    expiry_date: Optional[str] = Form(None),
    credential_url: Optional[str] = Form(None),
):
    """Handle certification creation form submission."""
    admin = get_current_admin(request)
    if not admin:
        return RedirectResponse(url="/admin/login", status_code=302)
    
    # Convert date strings to ISO format that the API can parse
    issue_date_iso = f"{issue_date}T00:00:00" if issue_date else None
    expiry_date_iso = f"{expiry_date}T00:00:00" if expiry_date and expiry_date.strip() else None
    
    data = {
        "title": title,
        "issuer": issuer,
        "issue_date": issue_date_iso,
        "expiry_date": expiry_date_iso,
        "credential_url": credential_url or None,
    }
    
    try:
        result = await admin_api_service.create_certification(data)
    except Exception as exc:
        # Defensive: capture unexpected errors from the HTTP client or network
        certifications = await admin_api_service.get_certifications()
        return templates.TemplateResponse(
            "certifications.html",
            {
                "request": request,
                "admin": admin,
                "certifications": certifications,
                "message": None,
                "error": f"API call failed: {str(exc)}",
            }
        )

    error = result.get("error")

    if error:
        certifications = await admin_api_service.get_certifications()
        # Prefer API-provided detail, fall back to raw_text if present
        detail = result.get("detail") or result.get("raw_text") or "Unknown error from API"
        return templates.TemplateResponse(
            "certifications.html",
            {
                "request": request,
                "admin": admin,
                "certifications": certifications,
                "message": None,
                "error": detail,                "api_error_raw": (result.get("raw_text")[:200] + '...') if result.get("raw_text") else None,
                "api_error_url": result.get("url") if result.get("url") else None,            }
        )

    return RedirectResponse(
        url="/admin/certifications?message=Certification+created+successfully",
        status_code=302
    )


@router.get("/certifications/{cert_id}/delete")
async def certifications_delete(request: Request, cert_id: str):
    """Delete a certification."""
    admin = get_current_admin(request)
    if not admin:
        return RedirectResponse(url="/admin/login", status_code=302)
    
    result = await admin_api_service.delete_certification(cert_id)
    error = result.get("error")
    
    if error:
        return RedirectResponse(
            url=f"/admin/certifications?error={result.get('detail')}",
            status_code=302
        )
    
    return RedirectResponse(
        url="/admin/certifications?message=Certification+deleted+successfully",
        status_code=302
    )


# ==================== Projects ====================

@router.get("/projects", response_class=HTMLResponse)
async def projects_page(request: Request):
    """Render the projects management page."""
    admin = get_current_admin(request)
    if not admin:
        return RedirectResponse(url="/admin/login", status_code=302)
    
    projects = await admin_api_service.get_projects()
    
    return templates.TemplateResponse(
        "projects.html",
        {
            "request": request,
            "admin": admin,
            "projects": projects,
            "message": request.query_params.get("message"),
            "error": request.query_params.get("error"),
        }
    )


@router.post("/projects", response_class=HTMLResponse)
async def projects_submit(
    request: Request,
    title: str = Form(...),
    description: str = Form(...),
    tech_stack: str = Form(...),
    project_type: str = Form(...),
    github_url: Optional[str] = Form(None),
    live_url: Optional[str] = Form(None),
    image_url: Optional[str] = Form(None),
):
    """Handle project creation form submission."""
    admin = get_current_admin(request)
    if not admin:
        return RedirectResponse(url="/admin/login", status_code=302)
    
    # Parse tech stack from comma-separated string
    tech_stack_list = [t.strip() for t in tech_stack.split(",") if t.strip()]
    
    data = {
        "title": title,
        "description": description,
        "tech_stack": tech_stack_list,
        "project_type": project_type,
        "github_url": github_url or None,
        "live_url": live_url or None,
        "image_url": image_url or None,
    }
    
    result = await admin_api_service.create_project(data)
    error = result.get("error")
    
    if error:
        projects = await admin_api_service.get_projects()
        return templates.TemplateResponse(
            "projects.html",
            {
                "request": request,
                "admin": admin,
                "projects": projects,
                "message": None,
                "error": result.get("detail"),
            }
        )
    
    return RedirectResponse(
        url="/admin/projects?message=Project+created+successfully",
        status_code=302
    )


@router.get("/projects/{project_id}/delete")
async def projects_delete(request: Request, project_id: str):
    """Delete a project."""
    admin = get_current_admin(request)
    if not admin:
        return RedirectResponse(url="/admin/login", status_code=302)
    
    result = await admin_api_service.delete_project(project_id)
    error = result.get("error")
    
    if error:
        return RedirectResponse(
            url=f"/admin/projects?error={result.get('detail')}",
            status_code=302
        )
    
    return RedirectResponse(
        url="/admin/projects?message=Project+deleted+successfully",
        status_code=302
    )


# ==================== Experience ====================

@router.get("/experience", response_class=HTMLResponse)
async def experience_page(request: Request):
    """Render the experience management page."""
    admin = get_current_admin(request)
    if not admin:
        return RedirectResponse(url="/admin/login", status_code=302)
    
    experiences = await admin_api_service.get_experiences()
    
    return templates.TemplateResponse(
        "experience.html",
        {
            "request": request,
            "admin": admin,
            "experiences": experiences,
            "message": request.query_params.get("message"),
            "error": request.query_params.get("error"),
        }
    )


@router.post("/experience", response_class=HTMLResponse)
async def experience_submit(
    request: Request,
    company_name: str = Form(...),
    role: str = Form(...),
    description: str = Form(...),
    start_date: str = Form(...),
    end_date: Optional[str] = Form(None),
    learnings: Optional[str] = Form(None),
):
    """Handle experience creation form submission."""
    admin = get_current_admin(request)
    if not admin:
        return RedirectResponse(url="/admin/login", status_code=302)
    
    # Always send ISO-formatted datetimes so the API/storage layer receives consistent values.
    start_date_iso = f"{start_date.strip()}T00:00:00" if start_date and start_date.strip() else None
    end_date_iso = f"{end_date.strip()}T00:00:00" if end_date and end_date.strip() else None

    data = {
        "company_name": company_name,
        "role": role,
        "description": description,
        "start_date": start_date_iso,
        "end_date": end_date_iso,
        "learnings": learnings or None,
    }
    
    try:
        result = await admin_api_service.create_experience(data)
    except Exception as exc:
        experiences = await admin_api_service.get_experiences()
        logger.exception("admin -> create_experience failed")
        return templates.TemplateResponse(
            "experience.html",
            {
                "request": request,
                "admin": admin,
                "experiences": experiences,
                "message": None,
                "error": f"API call failed: {str(exc)}",
            }
        )
    error = result.get("error")
    
    if error:
        logger.error(f"admin -> create_experience API error: {result.get('detail')}", extra={"payload": data, "result": result})
        experiences = await admin_api_service.get_experiences()
        # Prefer API-provided detail, fall back to raw_text if present
        detail = result.get("detail") or result.get("raw_text") or "Unknown error from API"
        return templates.TemplateResponse(
            "experience.html",
            {
                "request": request,
                "admin": admin,
                "experiences": experiences,
                "message": None,
                "error": detail,
                "api_error_raw": (result.get("raw_text")[:500] + '...') if result.get("raw_text") else None,
                "api_error_url": result.get("url") if result.get("url") else None,
            }
        )
    
    return RedirectResponse(
        url="/admin/experience?message=Experience+created+successfully",
        status_code=302
    )


@router.get("/experience/{exp_id}/delete")
async def experience_delete(request: Request, exp_id: str):
    """Delete an experience entry."""
    admin = get_current_admin(request)
    if not admin:
        return RedirectResponse(url="/admin/login", status_code=302)
    
    result = await admin_api_service.delete_experience(exp_id)
    error = result.get("error")
    
    if error:
        return RedirectResponse(
            url=f"/admin/experience?error={result.get('detail')}",
            status_code=302
        )
    
    return RedirectResponse(
        url="/admin/experience?message=Experience+deleted+successfully",
        status_code=302
    )


# ==================== Contact Requests ====================

@router.get("/contacts", response_class=HTMLResponse)
async def contacts_page(request: Request):
    """Render the contact requests page (read-only)."""
    admin = get_current_admin(request)
    if not admin:
        return RedirectResponse(url="/admin/login", status_code=302)
    
    contacts = await admin_api_service.get_contact_requests()
    
    return templates.TemplateResponse(
        "contacts.html",
        {
            "request": request,
            "admin": admin,
            "contacts": contacts,
        }
    )
