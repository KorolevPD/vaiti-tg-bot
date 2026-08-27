from typing import Optional

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        validate_by_name=True,
        alias_generator=to_camel,
    )


class GenerateRequest(BaseModel):
    vacancy_id: Optional[str] = None
    vacancy_url: Optional[str] = None
    raw_vacancy_text: Optional[str] = None
    resume_id: Optional[str] = None
    tone: str = "formal"


class DraftResponse(BaseModel):
    id: str
    vacancy_id: Optional[str] = None
    vacancy_url: Optional[str] = None
    resume_id: Optional[str] = None
    tone: Optional[str] = None
    status: str
    content: Optional[str] = None
    error_message: Optional[str] = None
