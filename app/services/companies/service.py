from typing import Any, List, Optional

from app.clients import APIClient

from .protocol import CompaniesServiceProtocol
from .schemas import (
    CompanyResponse,
    PagedModelCompanyResponse,
    ReviewRequest,
    ReviewResponse,
)


class CompaniesService(APIClient, CompaniesServiceProtocol):
    async def get_reviews(self, company_id: str) -> List[ReviewResponse]:
        r = await self._client.get(f"/api/v1/companies/{company_id}/reviews")
        r.raise_for_status()
        return [ReviewResponse.model_validate(item) for item in r.json()]

    async def add_review(
        self, company_id: str, data: ReviewRequest
    ) -> ReviewResponse:
        r = await self._client.post(
            f"/api/v1/companies/{company_id}/reviews",
            json=data.model_dump(by_alias=True, exclude_none=True),
        )
        r.raise_for_status()
        return ReviewResponse.model_validate(r.json())

    async def get_all(
        self,
        page: int = 0,
        size: int = 20,
        sort: Optional[List[str]] = None,
        query: Optional[str] = None,
    ) -> PagedModelCompanyResponse:
        params: dict[str, Any] = {"page": page, "size": size}
        if sort is not None:
            params["sort"] = sort
        if query is not None:
            params["query"] = query

        r = await self._client.get("/api/v1/companies", params=params)
        r.raise_for_status()
        return PagedModelCompanyResponse.model_validate(r.json())

    async def get_by_id(self, company_id: str) -> CompanyResponse:
        r = await self._client.get(f"/api/v1/companies/{company_id}")
        r.raise_for_status()
        return CompanyResponse.model_validate(r.json())
