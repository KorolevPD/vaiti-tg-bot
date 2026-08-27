from enum import StrEnum

from aiogram.filters.callback_data import CallbackData


class CoverLettersAction(StrEnum):
    CREATE = "create"
    LIST = "list"
    VIEW = "view"


class CoverLettersCallback(CallbackData, prefix="cover_letters"):
    action: CoverLettersAction
    page: int | None = None
    draft_id: str | None = None
