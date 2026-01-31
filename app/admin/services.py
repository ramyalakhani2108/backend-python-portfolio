"""
Admin Services Layer
Calls the existing API endpoints using httpx.
"""

import httpx
from typing import Optional, List, Dict, Any
import os

# API Base URL - defaults to localhost
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
API_V1_PREFIX = "/api/v1"


class AdminAPIService:
    """Service class for making API calls from the admin panel."""
    
    def __init__(self, base_url: str = None):
        self.base_url = base_url or API_BASE_URL
        self.api_url = f"{self.base_url}{API_V1_PREFIX}"
    
    async def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Make an HTTP request to the API."""
        url = f"{self.api_url}{endpoint}"
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                if method == "GET":
                    response = await client.get(url, params=params)
                elif method == "POST":
                    response = await client.post(url, json=data)
                elif method == "PUT":
                    response = await client.put(url, json=data)
                elif method == "DELETE":
                    response = await client.delete(url)
                else:
                    raise ValueError(f"Unsupported HTTP method: {method}")
                
                # Return response data
                if response.status_code == 204:
                    return {"success": True}

                if response.status_code >= 400:
                    # Avoid raising on non-JSON (HTML) error pages from the API
                    try:
                        detail = response.json().get("detail", response.text)
                    except Exception:
                        detail = response.text or "Unknown error"

                    # Log to server log for easier debugging
                    try:
                        logger = __import__('logging').getLogger('app.admin.services')
                        logger.warning('API request error', extra={
                            'url': url,
                            'status_code': response.status_code,
                            'detail': (detail[:500] if isinstance(detail, str) else str(detail)),
                        })
                    except Exception:
                        pass

                    return {
                        "error": True,
                        "status_code": response.status_code,
                        "detail": detail,
                        "raw_text": response.text if response.headers.get("content-type", "").startswith("text/") else None,
                        "url": url,
                    }

                # Normal successful JSON response — but guard against invalid JSON
                try:
                    return response.json()
                except Exception:
                    return {"error": True, "detail": "Invalid JSON response from API", "raw_text": response.text}

            except httpx.RequestError as e:
                return {
                    "error": True,
                    "detail": f"Request failed: {str(e)}",
                }
    
    # ==================== Personal Info ====================
    
    async def get_personal_info(self) -> Dict[str, Any]:
        """Get personal information."""
        return await self._request("GET", "/personal")
    
    async def create_personal_info(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create personal information."""
        return await self._request("POST", "/personal", data=data)
    
    async def update_personal_info(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update personal information."""
        return await self._request("PUT", "/personal", data=data)
    
    # ==================== Skills ====================
    
    async def get_skills(self, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get all skills, optionally filtered by category."""
        params = {"category": category} if category else None
        result = await self._request("GET", "/skills", params=params)
        return result if isinstance(result, list) else []
    
    async def get_skill(self, skill_id: str) -> Dict[str, Any]:
        """Get a specific skill by ID."""
        return await self._request("GET", f"/skills/{skill_id}")
    
    async def create_skill(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new skill."""
        return await self._request("POST", "/skills", data=data)
    
    async def update_skill(self, skill_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a skill."""
        return await self._request("PUT", f"/skills/{skill_id}", data=data)
    
    async def delete_skill(self, skill_id: str) -> Dict[str, Any]:
        """Delete a skill."""
        return await self._request("DELETE", f"/skills/{skill_id}")
    
    # ==================== Certifications ====================
    
    async def get_certifications(self) -> List[Dict[str, Any]]:
        """Get all certifications."""
        result = await self._request("GET", "/certifications")
        return result if isinstance(result, list) else []
    
    async def get_certification(self, cert_id: str) -> Dict[str, Any]:
        """Get a specific certification by ID."""
        return await self._request("GET", f"/certifications/{cert_id}")
    
    async def create_certification(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new certification."""
        return await self._request("POST", "/certifications", data=data)
    
    async def update_certification(self, cert_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a certification."""
        return await self._request("PUT", f"/certifications/{cert_id}", data=data)
    
    async def delete_certification(self, cert_id: str) -> Dict[str, Any]:
        """Delete a certification."""
        return await self._request("DELETE", f"/certifications/{cert_id}")
    
    # ==================== Projects ====================
    
    async def get_projects(self, project_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get all projects, optionally filtered by type."""
        params = {"project_type": project_type} if project_type else None
        result = await self._request("GET", "/projects", params=params)
        return result if isinstance(result, list) else []
    
    async def get_project(self, project_id: str) -> Dict[str, Any]:
        """Get a specific project by ID."""
        return await self._request("GET", f"/projects/{project_id}")
    
    async def create_project(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new project."""
        return await self._request("POST", "/projects", data=data)
    
    async def update_project(self, project_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a project."""
        return await self._request("PUT", f"/projects/{project_id}", data=data)
    
    async def delete_project(self, project_id: str) -> Dict[str, Any]:
        """Delete a project."""
        return await self._request("DELETE", f"/projects/{project_id}")
    
    # ==================== Experience ====================
    
    async def get_experiences(self) -> List[Dict[str, Any]]:
        """Get all experience entries."""
        result = await self._request("GET", "/experience")
        return result if isinstance(result, list) else []
    
    async def get_experience(self, exp_id: str) -> Dict[str, Any]:
        """Get a specific experience by ID."""
        return await self._request("GET", f"/experience/{exp_id}")
    
    async def create_experience(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new experience entry."""
        return await self._request("POST", "/experience", data=data)
    
    async def update_experience(self, exp_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an experience entry."""
        return await self._request("PUT", f"/experience/{exp_id}", data=data)
    
    async def delete_experience(self, exp_id: str) -> Dict[str, Any]:
        """Delete an experience entry."""
        return await self._request("DELETE", f"/experience/{exp_id}")
    
    # ==================== Contact Requests ====================
    
    async def get_contact_requests(self) -> List[Dict[str, Any]]:
        """Get all contact requests (read-only for admin)."""
        # Note: The current API only has POST for contacts
        # This would need a GET endpoint added to the API
        # For now, we'll return an empty list or handle it differently
        result = await self._request("GET", "/contact")
        return result if isinstance(result, list) else []


# Singleton instance
admin_api_service = AdminAPIService()
