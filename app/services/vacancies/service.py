from typing import Any

from app.clients import APIClient
from app.services.vacancies.schemas import InteractionRequest

from .protocol import VacancyServiceProtocol
from .schemas import (
    PagedVacancyResponse,
    VacancyResponse,
    VacancySearchRequest,
)


class VacancyService(APIClient, VacancyServiceProtocol):
    async def search(
        self,
        data: VacancySearchRequest | None = None,
        page: int = 0,
        size: int = 20,
        sort: list[str] | None = None,
    ) -> PagedVacancyResponse:
        params: dict[str, Any] = {
            "page": page,
            "size": size,
        }

        if sort:
            params["sort"] = sort

        response = await self._client.post(
            "/api/v1/vacancies/search",
            params=params,
            json=(
                data.model_dump(by_alias=True, exclude_none=True)
                if data
                else None
            ),
        )

        response.raise_for_status()

        return PagedVacancyResponse.model_validate(response.json())

    async def get_by_id(self, vacancy_id: str) -> VacancyResponse:
        response = await self._client.get(f"/api/v1/vacancies/{vacancy_id}")

        response.raise_for_status()

        return VacancyResponse.model_validate(response.json())

    async def record_interaction(
        self,
        data: InteractionRequest,
    ) -> bool:
        response = await self._client.post(
            "/api/v1/profile/interactions/",
            json=data.model_dump(by_alias=True, exclude_none=True),
        )
        response.raise_for_status()
        return True
