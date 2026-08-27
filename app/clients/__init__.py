from typing import Optional

import httpx


class APIClient:
    def __init__(self, base_url: str, auth_header: Optional[str] = None):
        self.auth_header = auth_header
        self._client = httpx.AsyncClient(
            base_url=base_url.rstrip("/"),
            headers=self.headers,
        )

    @property
    def headers(self) -> dict[str, str]:
        if not self.auth_header:
            return {}
        return {"Authorization": self.auth_header}

    async def aclose(self) -> None:
        await self._client.aclose()
