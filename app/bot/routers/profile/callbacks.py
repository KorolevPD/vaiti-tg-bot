from enum import StrEnum

from aiogram.filters.callback_data import CallbackData


class ProfileAction(StrEnum):
    MENU = "menu"


class ProfileCallback(CallbackData, prefix="profile"):
    action: ProfileAction
