from aiogram.types import InlineKeyboardButton

from .callbacks import ProfileAction, ProfileCallback
from .texts import PROFILE_TITLE

PROFILE_BTN = InlineKeyboardButton(
    text=PROFILE_TITLE,
    callback_data=ProfileCallback(action=ProfileAction.MENU).pack(),
)
