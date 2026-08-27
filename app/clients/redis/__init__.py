from typing import Optional

from redis.asyncio import Redis

from app.core.config import settings


async def create_redis_client() -> Optional[Redis]:
    """Создает подключение к Redis."""
    if not (settings.REDIS_HOST and settings.REDIS_PORT):
        return None

    try:
        redis_client = Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            password=settings.REDIS_PASSWORD,
            decode_responses=True,
            socket_connect_timeout=5,
            socket_timeout=5,
            health_check_interval=30,
        )
        await redis_client.ping()  # type: ignore
        return redis_client
    except Exception:
        settings.logger.warning("Unable to connect to Redis.")
        return None
