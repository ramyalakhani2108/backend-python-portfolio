"""
Admin Authentication Module
Session-based authentication for the admin panel.
"""

from typing import Optional
from fastapi import Request, HTTPException, status
from fastapi.responses import RedirectResponse
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from functools import wraps

from app.core.config import settings

# Load admin credentials from environment
ADMIN_USERNAME = settings.ADMIN_USERNAME
ADMIN_PASSWORD = settings.ADMIN_PASSWORD
SECRET_KEY = settings.ADMIN_SECRET_KEY
SESSION_EXPIRY = 60 * 60 * 24  # 24 hours in seconds

# Session serializer
serializer = URLSafeTimedSerializer(SECRET_KEY)


def create_session_token(username: str) -> str:
    """Create a session token for the admin user."""
    return serializer.dumps({"username": username})


def verify_session_token(token: str) -> Optional[dict]:
    """Verify a session token and return the payload."""
    try:
        data = serializer.loads(token, max_age=SESSION_EXPIRY)
        return data
    except (BadSignature, SignatureExpired):
        return None


def verify_credentials(username: str, password: str) -> bool:
    """Verify admin credentials."""
    return username == ADMIN_USERNAME and password == ADMIN_PASSWORD


def get_current_admin(request: Request) -> Optional[str]:
    """Get the current admin user from session cookie."""
    token = request.cookies.get("admin_session")
    if not token:
        return None
    
    data = verify_session_token(token)
    if not data:
        return None
    
    return data.get("username")


def login_required(func):
    """Decorator to require admin login for a route."""
    @wraps(func)
    async def wrapper(request: Request, *args, **kwargs):
        admin = get_current_admin(request)
        if not admin:
            return RedirectResponse(url="/admin/login", status_code=status.HTTP_302_FOUND)
        return await func(request, *args, **kwargs)
    return wrapper


class AdminAuth:
    """Admin authentication helper class."""
    
    @staticmethod
    def login(username: str, password: str) -> Optional[str]:
        """
        Attempt to log in with the provided credentials.
        Returns a session token if successful, None otherwise.
        """
        if verify_credentials(username, password):
            return create_session_token(username)
        return None
    
    @staticmethod
    def logout_response(redirect_url: str = "/admin/login") -> RedirectResponse:
        """Create a response that logs out the user."""
        response = RedirectResponse(url=redirect_url, status_code=status.HTTP_302_FOUND)
        response.delete_cookie("admin_session")
        return response
    
    @staticmethod
    def login_response(token: str, redirect_url: str = "/admin/dashboard") -> RedirectResponse:
        """Create a response that logs in the user."""
        response = RedirectResponse(url=redirect_url, status_code=status.HTTP_302_FOUND)
        response.set_cookie(
            key="admin_session",
            value=token,
            httponly=True,
            max_age=SESSION_EXPIRY,
            samesite="lax",
        )
        return response
