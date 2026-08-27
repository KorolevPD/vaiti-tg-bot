from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        validate_by_name=True,
        alias_generator=to_camel,
    )


class FeedbackType(str, Enum):
    BUG = "BUG"
    REQUEST = "REQUEST"
    QUESTION = "QUESTION"
    OTHER = "OTHER"


class FeedbackRequest(BaseSchema):
    type: FeedbackType
    source: str = "TELEGRAM_BOT"
    contact: str
    message: str
    current_url: Optional[str] = None
    user_agent: Optional[str] = None
    app_version: Optional[str] = None
    locale: Optional[str] = None
    errors: Optional[List[str]] = None
