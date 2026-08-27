from typing import Protocol

from aiogram.types import User


class AuthServiceProtocol(Protocol):
    async def get_auth_header(self, user: User) -> str: ...
