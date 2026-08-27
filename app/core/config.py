from enum import StrEnum
from functools import cached_property
import logging
from random import shuffle
from typing import Any, List, Literal, Optional

from aiogram.fsm.storage.base import KeyBuilder, StorageKey
from pydantic import Field, ValidationError
from pydantic_settings import BaseSettings
import yaml

from app.clients.proxy.models import Proxy


class UpdateMethod(StrEnum):
    POLLING = "polling"
    WEBHOOK = "webhook"


class CustomKeyBuilder(KeyBuilder):
    def build(
        self,
        key: StorageKey,
        part: Optional[Literal["data", "state", "lock"]] = None,
    ) -> str:
        if part in ("data", "state"):
            prefix = "fsm"
        else:
            prefix = "custom"
        return (
            f"{settings.REDIS_KEY_PREFIX}:{prefix}:"
            f"{key.user_id}:{part or 'data'}"
        )


class Settings(BaseSettings):
    """Глобальные настройки."""

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)
        try:
            self.PROXIES = self.load_proxies()
        except Exception as e:
            self.logger.warning(f"Failed to load proxies:\n{e}")
        if self.PROXIES:
            self.logger.info(f"Loaded {len(self.PROXIES)} proxies.")

    # Общее
    SERVICES_URL: str = Field("http://caddy")
    PROXIES: Optional[List[Proxy]] = None

    # Telegram Bot
    BOT_TOKEN: str = Field(...)
    BOT_SUPPORT_USERNAME: str = Field("vaiti_support")
    BOT_UPDATE_METHOD: UpdateMethod = Field(UpdateMethod.POLLING)
    WEBHOOK_DOMAIN: Optional[str] = Field(None)
    WEBHOOK_PATH: Optional[str] = Field(None)
    WEBHOOK_SECRET: Optional[str] = Field(None)

    # Redis
    REDIS_HOST: Optional[str] = Field(None)
    REDIS_PORT: Optional[int] = Field(None)
    REDIS_PASSWORD: Optional[str] = Field(None)
    REDIS_KEY_BUILDER: Optional[KeyBuilder] = Field(
        default_factory=CustomKeyBuilder
    )
    REDIS_KEY_PREFIX: str = Field("tg-bot")

    @cached_property
    def WEBHOOK_URL(self) -> str:
        return f"https://{self.WEBHOOK_DOMAIN}/{self.WEBHOOK_PATH}"

    @cached_property
    def logger(self) -> logging.Logger:
        return logging.getLogger("app")

    @classmethod
    def load_proxies(cls) -> Optional[List[Proxy]]:
        """Загружает прокси из расшифрованного файла."""
        proxies = []
        with open("../config/proxies.yaml", "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            for proxy in data.get("telegram", {}).get("proxies"):
                proxies.append(Proxy.model_validate(proxy))
        shuffle(proxies)
        return proxies or None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


try:
    settings = Settings()
except ValidationError as e:
    raise SystemExit(f"Ошибка конфигурации:\n{e}")
