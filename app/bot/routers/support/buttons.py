from aiogram.types import InlineKeyboardButton

from .callbacks import SupportAction, SupportCallback
from .texts import SUPPORT_TITLE

SUPPORT_BTN = InlineKeyboardButton(
    text=SUPPORT_TITLE,
    callback_data=SupportCallback(action=SupportAction.START).pack(),
)
