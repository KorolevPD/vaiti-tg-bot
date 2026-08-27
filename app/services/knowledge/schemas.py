from typing import Dict, List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, HttpUrl
from pydantic.alias_generators import to_camel


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        validate_by_name=True,
        alias_generator=to_camel,
    )


class Grade(BaseSchema):
    id: int
    name: str
    slug: str


class SkillMetadata(BaseSchema):
    application_areas: List[str]


class SkillRow(BaseSchema):
    id: int
    name: str
    slug: str
    criteria: Dict[str, str] = Field(default_factory=dict)
    type: Literal["COMPETENCY", "TOOL", "BOTH"]
    classification: Literal["HARD", "SOFT", "BOTH"]
    image_url: Optional[HttpUrl] = None
    complexity: Optional[str] = None
    metadata: Optional[SkillMetadata] = None


class SkillCategory(BaseSchema):
    category_name: str
    skills: List[SkillRow]


class DomainMatrixResponse(BaseSchema):
    id: int
    name: str
    slug: str
    description: Optional[str] = None
    image_url: Optional[HttpUrl] = None
    grades: List[Grade]
    skill_categories: List[SkillCategory]


class Skill(BaseSchema):
    id: int
    name: str
    slug: str
    category: str
    description: str
    image_url: Optional[HttpUrl] = None
    documentation_url: Optional[HttpUrl] = None
    metadata: Optional[SkillMetadata] = None


class DomainSummary(BaseSchema):
    id: int
    name: str
    slug: str
    isHidden: bool = False
    image_url: Optional[HttpUrl] = None


class Specialization(BaseSchema):
    id: int
    name: str
    slug: str
    image_url: Optional[HttpUrl] = None
    isHidden: bool = False
    domains: List[DomainSummary]


class TypicalQuestion(BaseSchema):
    question: str
    answer: str
    explanation: str
