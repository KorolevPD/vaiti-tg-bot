from enum import StrEnum
from typing import Optional

from aiogram.filters.callback_data import CallbackData


class SupportAction(StrEnum):
    START = "start"
    FEEDBACK_TYPE = "feedback_type"


class SupportCallback(CallbackData, prefix="support"):
    action: SupportAction
    feedback_type: Optional[str] = None
