from typing import Protocol

from app.services.vacancies.schemas import InteractionRequest

from .schemas import (
    PagedVacancyResponse,
    VacancyResponse,
    VacancySearchRequest,
)


class VacancyServiceProtocol(Protocol):
    async def search(
        self,
        body: VacancySearchRequest,
        page: int = 0,
        size: int = 20,
        sort: list[str] | None = None,
    ) -> PagedVacancyResponse: ...

    async def get_by_id(self, vacancy_id: str) -> VacancyResponse: ...

    async def record_interaction(
        self,
        data: InteractionRequest,
    ) -> bool: ...
