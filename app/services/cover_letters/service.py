from app.clients import APIClient

from .protocol import CoverLetterServiceProtocol
from .schemas import DraftResponse, GenerateRequest


class CoverLetterService(APIClient, CoverLetterServiceProtocol):
    async def generate(
        self,
        request: GenerateRequest,
    ) -> DraftResponse:
        resp = await self._client.post(
            "/api/v1/application/cover-letters/generate",
            json=request.model_dump(exclude_none=True),
        )

        resp.raise_for_status()
        return DraftResponse.model_validate(resp.json())

    async def get_draft(
        self,
        draft_id: str,
    ) -> DraftResponse:
        resp = await self._client.get(
            f"/api/v1/application/cover-letters/drafts/{draft_id}",
        )

        resp.raise_for_status()
        return DraftResponse.model_validate(resp.json())
