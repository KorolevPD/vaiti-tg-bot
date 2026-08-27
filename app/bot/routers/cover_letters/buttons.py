from aiogram.types import InlineKeyboardButton

from .callbacks import CoverLettersAction, CoverLettersCallback
from .texts import COVER_LETTERS_TITLE

COVER_LETTERS_BTN = InlineKeyboardButton(
    text=COVER_LETTERS_TITLE,
    callback_data=CoverLettersCallback(action=CoverLettersAction.LIST).pack(),
)
