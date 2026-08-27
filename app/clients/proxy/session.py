from typing import Any, AsyncGenerator

from aiogram import Bot
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.session.base import BaseSession
from aiogram.exceptions import TelegramNetworkError
from aiogram.methods import TelegramMethod
from aiogram.methods.base import TelegramType
from aiohttp import ClientError
from aiohttp_socks import ProxyConnectionError

from app.core.config import settings

from .models import Proxy

logger = settings.logger


class ProxySession(BaseSession):
    def __init__(self, proxies: list[Proxy], request_timeout: int = 10):
        if not proxies:
            raise ValueError("No proxies provided")

        super().__init__()
        self.request_timeout = request_timeout
        self._proxies = proxies
        self._index = 0
        self._current_proxy = proxies[0]
        self._session: AiohttpSession = AiohttpSession(
            proxy=self._current_proxy.as_url
        )

    async def _set_next_proxy(self) -> None:
        self._index = (self._index + 1) % len(self._proxies)
        self._current_proxy = self._proxies[self._index]

        if self._session:
            try:
                await self._session.close()
            except Exception as e:
                logger.debug(f"Error closing old session: {e}")

        self._session = AiohttpSession(proxy=self._current_proxy.as_url)
        logger.info(f"Switched to proxy: {self._current_proxy.server}")

    async def make_request(
        self,
        bot: Bot,
        method: TelegramMethod[TelegramType],
        timeout: int | None = None,
    ) -> TelegramType:
        attempts = len(self._proxies)
        timeout = self.request_timeout or timeout
        for attempt in range(attempts):
            try:
                return await self._session.make_request(bot, method, timeout)

            except (
                ClientError,
                TelegramNetworkError,
                ProxyConnectionError,
            ) as e:
                logger.warning(
                    f"Proxy failed [{attempt+1}/{attempts}] "
                    f"{self._current_proxy.server} — {type(e).__name__}: {e}"
                )

                await self._set_next_proxy()

        raise RuntimeError("All proxies failed after multiple attempts")

    async def close(self) -> None:
        if self._session:
            try:
                await self._session.close()
            except Exception as e:
                logger.debug(f"Error while closing ProxySession: {e}")

    async def stream_content(
        self,
        url: str,
        headers: dict[str, Any] | None = None,
        timeout: int = 30,
        chunk_size: int = 65536,
        raise_for_status: bool = True,
    ) -> AsyncGenerator[bytes, None]:
        async for chunk in self._session.stream_content(
            url=url,
            headers=headers,
            timeout=timeout,
            chunk_size=chunk_size,
            raise_for_status=raise_for_status,
        ):
            yield chunk
