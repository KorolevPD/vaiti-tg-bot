from enum import StrEnum
from typing import Optional

from aiogram.filters.callback_data import CallbackData

from .enums import SkillBlock


class SkillsCatalogAction(StrEnum):
    START = "start"
    BLOCK = "block"


class SkillsCatalogCallback(CallbackData, prefix="skills_catalog"):
    action: SkillsCatalogAction

    item_slug: Optional[str] = None
    item_id: Optional[int] = None
    block: Optional[SkillBlock] = None
