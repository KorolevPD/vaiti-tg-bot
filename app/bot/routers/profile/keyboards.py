from aiogram.types import InlineKeyboardMarkup

from app.bot.routers.cover_letters.buttons import COVER_LETTERS_BTN
from app.bot.routers.menu.buttons import BACK_TO_MENU_BTN
from app.bot.routers.resume.buttons import DOWNLOAD_BTN, UPLOAD_BTN
from app.bot.routers.statistic.buttons import STATISTIC_BTN


def menu_kb() -> InlineKeyboardMarkup:
    rows = [
        [UPLOAD_BTN],
        [DOWNLOAD_BTN],
        [STATISTIC_BTN],
        [COVER_LETTERS_BTN],
        [BACK_TO_MENU_BTN],
    ]
    return InlineKeyboardMarkup(inline_keyboard=rows)
