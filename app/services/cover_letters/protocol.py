from typing import Protocol

from .schemas import DraftResponse, GenerateRequest


class CoverLetterServiceProtocol(Protocol):
    async def generate(
        self,
        request: GenerateRequest,
    ) -> DraftResponse: ...

    async def get_draft(
        self,
        draft_id: str,
    ) -> DraftResponse: ...
