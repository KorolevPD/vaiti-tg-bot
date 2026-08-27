from enum import StrEnum

from aiogram.filters.callback_data import CallbackData


class CompaniesAction(StrEnum):
    START = "start"
    VIEW = "view"
    PAGE = "page"


class CompaniesCallback(CallbackData, prefix="companies"):
    action: CompaniesAction
    company_id: str | None = None
    page: int | None = None
