from typing import Literal, Optional

from pydantic import BaseModel


class Proxy(BaseModel):
    type: Literal["SOCKS5", "HTTP"]
    server: str
    port: int
    username: Optional[str] = None
    password: Optional[str] = None

    @property
    def as_url(self) -> str:
        """Возвращает строку вида socks5://user:pass@host:port"""
        return f"{self.type.lower()}://{self.auth}{self.server}:{self.port}"

    @property
    def auth(self) -> str:
        """Возвращает строку авторизации."""
        auth = ""
        if self.username:
            if self.password:
                auth = f"{self.username}:{self.password}@"
            else:
                auth = f"{self.username}@"
        return auth
