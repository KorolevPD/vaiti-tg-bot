from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    WebAppInfo,
)

from app.bot.routers.menu.buttons import BACK_TO_MENU_BTN
from app.services.vacancies.schemas import InteractionType, VacancyResponse

from .callbacks import VacanciesAction, VacanciesCallback


def vacancy_kb(v: VacancyResponse) -> InlineKeyboardMarkup:
    rows = [
        [
            InlineKeyboardButton(
                text="👍",
                callback_data=VacanciesCallback(
                    action=VacanciesAction.REACTION,
                    vacancy_id=v.id,
                    interaction_type=InteractionType.LIKE,
                ).pack(),
            ),
            InlineKeyboardButton(
                text="👎",
                callback_data=VacanciesCallback(
                    action=VacanciesAction.REACTION,
                    vacancy_id=v.id,
                    interaction_type=InteractionType.DISLIKE,
                ).pack(),
            ),
        ],
        [
            InlineKeyboardButton(
                text="♥️ В избранное",
                callback_data=VacanciesCallback(
                    action=VacanciesAction.REACTION,
                    vacancy_id=v.id,
                    interaction_type=InteractionType.FAVORITE,
                ).pack(),
            )
        ],
        [
            InlineKeyboardButton(
                text="🔍 Подробнее",
                web_app=WebAppInfo(url=f"https://vaiti.tech/vacancies/{v.id}"),
            )
        ],
        [BACK_TO_MENU_BTN],
    ]

    return InlineKeyboardMarkup(inline_keyboard=rows)
