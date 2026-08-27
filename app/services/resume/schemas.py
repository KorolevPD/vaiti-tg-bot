from datetime import date, datetime
from typing import List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        validate_by_name=True,
        alias_generator=to_camel,
    )


class ProfileSkill(BaseSchema):
    skill_id: int
    level: str


class Language(BaseSchema):
    name: str
    level: str


class Course(BaseSchema):
    id: str
    name: str
    platform: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    current: Optional[bool] = None


class Education(BaseSchema):
    id: str
    institution: str
    specialization: Optional[str] = None
    degree: Optional[str] = None
    location: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    current: Optional[bool] = None


class WorkExperience(BaseSchema):
    id: str
    company_id: Optional[str] = None
    company_name: str
    position_title: str
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    current: Optional[bool] = None


class ProfileResponse(BaseSchema):
    user_id: str
    first_name: str
    last_name: str
    middle_name: Optional[str] = None
    gender: Optional[Literal["MALE", "FEMALE", "UNKNOWN"]] = None
    email: Optional[str] = None
    telegram: Optional[str] = None
    image_path: Optional[str] = None
    position_title: Optional[str] = None
    level: Optional[str] = None
    status: Optional[
        Literal["ACTIVE", "OPEN_TO_OFFERS", "NOT_LOOKING", "HIDDEN", "BLOCKED"]
    ] = None
    target_salary: Optional[int] = None
    employment_type: Optional[str] = None
    work_format: Optional[Literal["REMOTE", "OFFICE", "HYBRID"]] = None
    location: Optional[str] = None
    ready_for_relocation: bool = False
    bio: Optional[str] = None
    citizenship: Optional[str] = None
    work_permits: List[str] = Field(default_factory=list)
    links: List[str] = Field(default_factory=list)
    experience: List[WorkExperience] = Field(default_factory=list)
    education: List[Education] = Field(default_factory=list)
    courses: List[Course] = Field(default_factory=list)
    languages: List[Language] = Field(default_factory=list)
    skills: List[ProfileSkill] = Field(default_factory=list)


class ResumeData(BaseSchema):
    position_title: Optional[str] = None
    bio: Optional[str] = None
    experience: List[WorkExperience] = Field(default_factory=list)
    education: List[Education] = Field(default_factory=list)
    courses: List[Course] = Field(default_factory=list)
    languages: List[Language] = Field(default_factory=list)
    skills: List[ProfileSkill] = Field(default_factory=list)


class ResumeSummary(BaseSchema):
    id: str
    title: str
    source_type: str
    created_at: datetime
    updated_at: datetime
    is_primary: bool


class ResumeCreate(BaseSchema):
    title: Optional[str] = Field(None, max_length=255)
    parsed_data: ResumeData


class ResumeDetail(BaseSchema):
    id: str
    title: str
    source_type: str
    created_at: datetime
    updated_at: datetime
    is_primary: bool
    parsed_data: ResumeData


class ResumeUpdate(BaseSchema):
    title: Optional[str] = Field(None, max_length=255)
    parsed_data: ResumeData


class ResumeUploadResponse(BaseSchema):
    id: str
    file_name: str
    status: str
