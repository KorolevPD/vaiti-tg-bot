from typing import List, Optional

from app.clients import APIClient

from .protocol import KnowledgeServiceProtocol
from .schemas import (
    DomainMatrixResponse,
    Skill,
    Specialization,
    TypicalQuestion,
)


class KnowledgeService(APIClient, KnowledgeServiceProtocol):
    async def get_tree(self) -> List[Specialization]:
        r = await self._client.get("/api/v1/knowledge/tree")
        r.raise_for_status()
        return [Specialization(**item) for item in r.json()]

    async def get_domain_matrix(self, slug: str) -> DomainMatrixResponse:
        r = await self._client.get(f"/api/v1/knowledge/domain/{slug}")
        r.raise_for_status()
        return DomainMatrixResponse(**r.json())

    async def get_typical_questions(
        self, slug: str, grade_id: Optional[int] = None
    ) -> List[TypicalQuestion]:
        params = {"gradeId": grade_id} if grade_id is not None else {}
        r = await self._client.get(
            f"/api/v1/knowledge/domain/{slug}/typical-questions", params=params
        )
        r.raise_for_status()
        return [TypicalQuestion(**item) for item in r.json()]

    async def get_domain_tools(self, slug: str) -> List[Skill]:
        r = await self._client.get(f"/api/v1/knowledge/domain/{slug}/tools")
        r.raise_for_status()
        return [Skill(**item) for item in r.json()]
