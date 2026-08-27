from aiogram.types import InlineKeyboardMarkup

from app.bot.routers.companies.buttons import COMPANIES_BTN
from app.bot.routers.profile.buttons import PROFILE_BTN
from app.bot.routers.skills_catalog.buttons import SKILLS_CATALOG_BTN
from app.bot.routers.support.buttons import SUPPORT_BTN
from app.bot.routers.trainer.buttons import TRAINER_BTN
from app.bot.routers.vacancies.buttons import VACANCIES_BTN


def menu_kb() -> InlineKeyboardMarkup:
    rows = [
        [COMPANIES_BTN],
        [SKILLS_CATALOG_BTN],
        [VACANCIES_BTN],
        [TRAINER_BTN],
        [PROFILE_BTN],
        [SUPPORT_BTN],
    ]
    return InlineKeyboardMarkup(inline_keyboard=rows)
