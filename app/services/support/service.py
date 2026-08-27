from app.clients import APIClient

from .protocol import SupportServiceProtocol
from .schemas import FeedbackRequest


class SupportService(APIClient, SupportServiceProtocol):
    async def send_feedback(self, data: FeedbackRequest) -> bool:
        r = await self._client.post(
            "/api/v1/support/feedback",
            json=data.model_dump(),
        )
        r.raise_for_status()
        return r.status_code == 202
