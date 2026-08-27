from enum import StrEnum

from aiogram.filters.callback_data import CallbackData


class MenuAction(StrEnum):
    START = "start"


class MenuCallback(CallbackData, prefix="menu"):
    action: MenuAction
