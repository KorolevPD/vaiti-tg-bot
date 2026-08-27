from aiogram.types import InlineKeyboardButton

from .callbacks import CompaniesAction, CompaniesCallback
from .texts import COMPANIES_TITLE

COMPANIES_BTN = InlineKeyboardButton(
    text=COMPANIES_TITLE,
    callback_data=CompaniesCallback(action=CompaniesAction.START).pack(),
)
