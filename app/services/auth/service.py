from aiogram.types import User
import httpx

from .protocol import AuthServiceProtocol
from .schemas import AuthResponse, TelegramAuthRequest


class AuthService(AuthServiceProtocol):
    def __init__(self, base_url: str):
        self._client = httpx.AsyncClient(
            base_url=base_url.rstrip("/"),
        )

    async def aclose(self) -> None:
        await self._client.aclose()

    async def get_auth_header(self, user: User) -> str:
        request = TelegramAuthRequest(id=user.id, first_name=user.first_name)
        r = await self._client.post(
            "/api/v1/auth/telegram", json=request.model_dump()
        )
        r.raise_for_status()
        auth_response = AuthResponse.model_validate(r.json())
        return auth_response.auth_header
