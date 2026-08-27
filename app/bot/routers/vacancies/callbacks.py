from enum import StrEnum
from typing import Optional

from aiogram.filters.callback_data import CallbackData

from app.services.vacancies.schemas import InteractionType


class VacanciesAction(StrEnum):
    START = "start"
    REACTION = "reaction"


class VacanciesCallback(CallbackData, prefix="vacancy"):
    action: VacanciesAction
    vacancy_id: Optional[str] = None
    interaction_type: Optional[InteractionType] = None
