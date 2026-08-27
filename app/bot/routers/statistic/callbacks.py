from enum import StrEnum

from aiogram.filters.callback_data import CallbackData


class StatisticAction(StrEnum):
    START = "start"
    VIEW = "view"


class StatisticCallback(CallbackData, prefix="statistic"):
    action: StatisticAction
    start_date: float | None = None
    end_date: float | None = None
