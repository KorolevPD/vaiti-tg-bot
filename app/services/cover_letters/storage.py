from typing import Awaitable, cast

from redis.asyncio import Redis

from app.core.config import settings
from app.services.cover_letters.schemas import DraftResponse


class CoverLettersStorage:
    def __init__(self, redis: Redis) -> None:
        self._redis = redis

    def _ids_key(self, user_id: int) -> str:
        return f"{settings.REDIS_KEY_PREFIX}:cover_letters:{user_id}:ids"

    def _drafts_key(self, user_id: int) -> str:
        return f"{settings.REDIS_KEY_PREFIX}:cover_letters:{user_id}:drafts"

    async def add_id(self, user_id: int, draft_id: str) -> None:
        await cast(
            Awaitable[int],
            self._redis.lpush(self._ids_key(user_id), draft_id),
        )

    async def get_page_ids(
        self,
        user_id: int,
        page: int,
        size: int,
    ) -> list[str]:
        start = page * size
        end = start + size - 1

        ids = await cast(
            Awaitable[list[str]],
            self._redis.lrange(self._ids_key(user_id), start, end),
        )

        return ids

    async def count(self, user_id: int) -> int:
        return await cast(
            Awaitable[int],
            self._redis.llen(self._ids_key(user_id)),
        )

    async def save_draft(
        self,
        user_id: int,
        draft: DraftResponse,
    ) -> None:
        await cast(
            Awaitable[int],
            self._redis.hset(
                self._drafts_key(user_id),
                str(draft.id),
                draft.model_dump_json(),
            ),
        )

    async def get_cached_draft(
        self,
        user_id: int,
        draft_id: str,
    ) -> DraftResponse | None:
        raw = await cast(
            Awaitable[str | None],
            self._redis.hget(
                self._drafts_key(user_id),
                str(draft_id),
            ),
        )

        if not raw:
            return None

        return DraftResponse.model_validate_json(raw)

    async def delete_draft(
        self,
        user_id: int,
        draft_id: str,
    ) -> None:
        await cast(
            Awaitable[int],
            self._redis.hdel(
                self._drafts_key(user_id),
                str(draft_id),
            ),
        )
