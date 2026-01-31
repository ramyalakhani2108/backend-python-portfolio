"""Schemas module initialization."""

from app.schemas.personal import (
    PersonalInfoBase,
    PersonalInfoCreate,
    PersonalInfoUpdate,
    PersonalInfoResponse,
)
from app.schemas.skills import (
    SkillBase,
    SkillCreate,
    SkillUpdate,
    SkillResponse,
    SkillCategory,
)
from app.schemas.certifications import (
    CertificationBase,
    CertificationCreate,
    CertificationUpdate,
    CertificationResponse,
)
from app.schemas.projects import (
    ProjectBase,
    ProjectCreate,
    ProjectUpdate,
    ProjectResponse,
    ProjectType,
)
from app.schemas.experience import (
    ExperienceBase,
    ExperienceCreate,
    ExperienceUpdate,
    ExperienceResponse,
)
from app.schemas.contact import (
    ContactRequestBase,
    ContactRequestCreate,
    ContactRequestResponse,
)
from app.schemas.rya_ai import (
    RyaQuestionRequest,
    RyaAnswerResponse,
    AIContextLogResponse,
)
from app.schemas.tags import TagBase, TagCreate, TagResponse

__all__ = [
    # Personal
    "PersonalInfoBase",
    "PersonalInfoCreate",
    "PersonalInfoUpdate",
    "PersonalInfoResponse",
    # Skills
    "SkillBase",
    "SkillCreate",
    "SkillUpdate",
    "SkillResponse",
    "SkillCategory",
    # Certifications
    "CertificationBase",
    "CertificationCreate",
    "CertificationUpdate",
    "CertificationResponse",
    # Projects
    "ProjectBase",
    "ProjectCreate",
    "ProjectUpdate",
    "ProjectResponse",
    "ProjectType",
    # Experience
    "ExperienceBase",
    "ExperienceCreate",
    "ExperienceUpdate",
    "ExperienceResponse",
    # Contact
    "ContactRequestBase",
    "ContactRequestCreate",
    "ContactRequestResponse",
    # Rya AI
    "RyaQuestionRequest",
    "RyaAnswerResponse",
    "AIContextLogResponse",
    # Tags
    "TagBase",
    "TagCreate",
    "TagResponse",
]
