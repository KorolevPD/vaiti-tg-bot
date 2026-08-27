from enum import StrEnum
from typing import Optional

from aiogram.filters.callback_data import CallbackData


class SkillSelectAction(StrEnum):
    START = "start"
    SPECIALIZATION = "specialization"
    DOMAIN = "domain"
    GRADE = "grade"
    BACK = "back"


class SkillSelectCallback(CallbackData, prefix="skill"):
    action: SkillSelectAction
    item_slug: Optional[str] = None
    item_id: Optional[int] = None
