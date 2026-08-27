from typing import List, Optional, Protocol

from .schemas import CompanyResponse, PagedModelCompanyResponse


class CompaniesServiceProtocol(Protocol):
    async def get_all(
        self,
        page: int = 0,
        size: int = 20,
        sort: Optional[List[str]] = None,
    ) -> PagedModelCompanyResponse: ...

    async def get_by_id(self, company_id: str) -> CompanyResponse: ...
