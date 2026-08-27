from typing import Any, Awaitable, Callable, Dict, Optional

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from redis.asyncio import Redis

from app.core.config import settings
from app.services.auth.service import AuthService


class AuthMiddleware(BaseMiddleware):
    def __init__(self, redis: Optional[Redis] = None) -> None:
        self.redis = redis
        self.auth_service = AuthService(settings.SERVICES_URL)

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        state = data.get("state")
        user = data.get("event_from_user")
        if user:
            auth_header: Optional[str] = None

            if self.redis:
                key = f"{settings.REDIS_KEY_PREFIX}:auth:{user.id}"
                auth_header = await self.redis.get(key)

            if not auth_header:
                auth_header = await self.auth_service.get_auth_header(user)
                if self.redis and auth_header:
                    await self.redis.set(key, auth_header, ex=900)

            if state:
                await state.update_data(auth_header=auth_header)
            data["auth_header"] = auth_header

        return await handler(event, data)
