from enum import StrEnum
from typing import Optional

from aiogram.filters.callback_data import CallbackData


class TrainerAction(StrEnum):
    START = "start"
    SETUP = "setup"
    OPTION = "option"
    SELECT = "select"
    SUBMIT = "submit"
    RESULTS = "results"
    BACK = "back"


class TrainerCallback(CallbackData, prefix="trainer"):
    action: TrainerAction
    domain_id: Optional[int] = None
    option_id: Optional[int] = None
