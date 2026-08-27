from typing import List, Optional, Protocol

from .schemas import (
    DomainMatrixResponse,
    Skill,
    Specialization,
    TypicalQuestion,
)


class KnowledgeServiceProtocol(Protocol):
    async def get_tree(self) -> List[Specialization]: ...
    async def get_domain_matrix(self, slug: str) -> DomainMatrixResponse: ...

    async def get_typical_questions(
        self, slug: str, grade_id: Optional[int] = None
    ) -> List[TypicalQuestion]: ...

    async def get_domain_tools(self, slug: str) -> List[Skill]: ...
