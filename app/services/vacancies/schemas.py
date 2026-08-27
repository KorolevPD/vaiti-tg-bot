from datetime import datetime
from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class InteractionType(StrEnum):
    LIKE = "LIKE"
    DISLIKE = "DISLIKE"
    APPLIED = "APPLIED"
    FAVORITE = "FAVORITE"


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        validate_by_name=True,
        alias_generator=to_camel,
        use_enum_values=True,
    )


class VacancySearchRequest(BaseSchema):
    grade_id: int | None = None
    specialization_id: int | None = None
    city: str | None = None
    salary_min: int | None = None
    sort_by: (
        Literal["RELEVANCE", "DATE", "SALARY_DESC", "SALARY_FIRST"] | None
    ) = None
    vector: list[float] | None = None
    excluded_ids: list[str] | None = None
    incognito_mode: bool | None = None
    min_match_score: int | None = None
    supports_auto_apply: bool | None = None


class PageMetadata(BaseSchema):
    size: int
    number: int
    total_elements: int
    total_pages: int


class VacancyResponse(BaseSchema):
    id: str
    source: str
    company_id: str | None = None
    company_name: str | None = None
    company_logo_url: str | None = None
    position_title: str
    raw_text: str | None = None
    location: str | None = None
    city: str | None = None
    source_url: str | None = None
    salary_min: int | None = None
    salary_max: int | None = None
    salary_currency: str | None = None
    salary_gross: bool | None = None
    work_format: str | None = None
    employment_type: str | None = None
    published_at: datetime | None = None
    grade_id: int | None = None
    specialization_id: int | None = None
    skill_ids: list[int] | None = None
    tool_ids: list[int] | None = None
    attributes: dict[str, str] | None = None
    match_score: int | None = None
    auto_apply_type: Literal["API", "EXTENSION", "NONE"] | None = None

    @property
    def salary_text(self) -> str | None:
        if self.salary_max is None:
            return None

        cur = self.salary_currency or ""

        if self.salary_min is not None:
            return f"{self.salary_min} - {self.salary_max} {cur}"
        return f"{self.salary_max} {cur}"


class PagedVacancyResponse(BaseSchema):
    content: list[VacancyResponse]
    page: PageMetadata


class InteractionRequest(BaseSchema):
    vacancy_id: str
    type: InteractionType
