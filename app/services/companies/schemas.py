from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        validate_by_name=True,
        alias_generator=to_camel,
    )


class InterviewStageType(str, Enum):
    HR_SCREENING = "HR_SCREENING"
    TECHNICAL = "TECHNICAL"
    TEST_TASK = "TEST_TASK"
    LIVE_CODING = "LIVE_CODING"
    MANAGEMENT = "MANAGEMENT"


class InterviewFormat(str, Enum):
    ONLINE = "ONLINE"
    OFFICE = "OFFICE"
    HOME = "HOME"
    ON_CALL = "ON_CALL"
    ON_PLATFORM = "ON_PLATFORM"


class OfferStatus(str, Enum):
    OFFER_ACCEPTED = "OFFER_ACCEPTED"
    OFFER_DECLINED = "OFFER_DECLINED"
    REJECTION = "REJECTION"
    SELF_DECLINED = "SELF_DECLINED"
    IN_PROGRESS = "IN_PROGRESS"


class ReviewModerationStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class CompanyLocation(str, Enum):
    DOMESTIC = "DOMESTIC"
    INTERNATIONAL = "INTERNATIONAL"
    GLOBAL = "GLOBAL"


class CompanySize(str, Enum):
    SMALL = "SMALL"
    MEDIUM = "MEDIUM"
    LARGE = "LARGE"
    ENTERPRISE = "ENTERPRISE"


class InterviewStage(BaseSchema):
    type: Optional[InterviewStageType] = None
    count: Optional[int] = None
    format: Optional[InterviewFormat] = None
    duration: Optional[str] = None
    is_paid: Optional[bool] = None
    deadline: Optional[str] = None
    internet_access: Optional[bool] = None
    interviewer_roles: Optional[List[str]] = None
    topics: Optional[List[str]] = None


class Questions(BaseSchema):
    topics: Optional[List[str]] = None
    examples: Optional[str] = None


class IndustrySnapshot(BaseSchema):
    id: Optional[str] = None
    name: Optional[str] = None
    slug: Optional[str] = None


class PageMetadata(BaseSchema):
    size: Optional[int] = None
    number: Optional[int] = None
    total_elements: Optional[int] = None
    total_pages: Optional[int] = None


class ReviewRequest(BaseSchema):
    rating: int = Field(..., ge=1, le=10)
    comment: Optional[str] = None
    is_anonymous: Optional[bool] = None
    position_title: Optional[str] = None
    grade_id: Optional[int] = None
    offer_status: Optional[OfferStatus] = None
    interview_ratings: Optional[Dict[str, int]] = None
    interview_stages: Optional[List[InterviewStage]] = None
    questions_data: Optional[Questions] = None


class ReviewResponse(BaseSchema):
    id: Optional[str] = None
    user_id: Optional[str] = None
    rating: Optional[int] = Field(None, ge=1, le=10)
    comment: Optional[str] = None
    is_anonymous: Optional[bool] = None
    position_title: Optional[str] = None
    grade_id: Optional[int] = None
    offer_status: Optional[OfferStatus] = None
    interview_ratings: Optional[Dict[str, int]] = None
    interview_stages: Optional[List[InterviewStage]] = None
    questions_data: Optional[Questions] = None
    status: Optional[ReviewModerationStatus] = None
    created_at: Optional[datetime] = None


class CompanyResponse(BaseSchema):
    id: Optional[str] = None
    name: str = "—"
    slug: Optional[str] = None
    description: Optional[str] = None
    website_url: Optional[str] = None
    logo_url: Optional[str] = None
    industries: Optional[List[IndustrySnapshot]] = None
    location: Optional[CompanyLocation] = None
    size: Optional[CompanySize] = None
    rating: float = Field(0.0, ge=0.0, le=10.0)
    complexity_rating: float = Field(0.0, ge=0.0, le=10.0)
    review_count: Optional[int] = None
    stack_ids: Optional[List[int]] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class PagedModelCompanyResponse(BaseSchema):
    content: Optional[List[CompanyResponse]] = None
    page: Optional[PageMetadata] = None


class RecruiterResponse(BaseSchema):
    id: Optional[str] = None
    company_id: Optional[str] = None
    name: Optional[str] = None
    surname: Optional[str] = None
    position: Optional[str] = None
    contacts: Optional[Dict[str, str]] = None


class ProblemDetail(BaseSchema):
    type: Optional[str] = None
    title: Optional[str] = None
    status: Optional[int] = None
    detail: Optional[str] = None
    instance: Optional[str] = None
    properties: Optional[Dict[str, Any]] = None
