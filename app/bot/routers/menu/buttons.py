from aiogram.types import InlineKeyboardButton

from .callbacks import MenuAction, MenuCallback
from .texts import BACK_TO_MENU_TITLE

BACK_TO_MENU_BTN = InlineKeyboardButton(
    text=BACK_TO_MENU_TITLE,
    callback_data=MenuCallback(action=MenuAction.START).pack(),
)
