from aiogram.types import InlineKeyboardButton

from .callbacks import VacanciesAction, VacanciesCallback
from .texts import VACANCIES_TITLE

VACANCIES_BTN = InlineKeyboardButton(
    text=VACANCIES_TITLE,
    callback_data=VacanciesCallback(action=VacanciesAction.START).pack(),
)
