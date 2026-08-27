import hashlib
import hmac
from time import time

from pydantic import BaseModel, ConfigDict, Field, computed_field
from pydantic.alias_generators import to_camel

from app.core.config import settings


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        validate_by_name=True,
        alias_generator=to_camel,
    )


class AuthResponse(BaseSchema):
    access_token: str = Field(...)
    type: str = Field(...)

    @property
    def auth_header(self) -> str:
        return f"{self.type} {self.access_token}"


class TelegramAuthRequest(BaseSchema):
    id: int
    first_name: str
    auth_date: int = Field(default_factory=lambda: int(time()))

    @computed_field
    def hash(self) -> str:
        data = {
            "id": self.id,
            "first_name": self.first_name,
            "auth_date": self.auth_date,
        }

        data_check_string = "\n".join(
            f"{k}={v}" for k, v in sorted(data.items())
        )

        secret_key = hashlib.sha256(
            settings.BOT_TOKEN.encode("utf-8")
        ).digest()

        hash_bytes = hmac.new(
            secret_key, data_check_string.encode("utf-8"), hashlib.sha256
        ).digest()

        return hash_bytes.hex()
