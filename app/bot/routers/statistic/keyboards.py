from datetime import timedelta
from time import time

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.bot.routers.menu.buttons import BACK_TO_MENU_BTN

from .callbacks import StatisticAction, StatisticCallback

PERIODS = [
    ("За день", timedelta(days=1).total_seconds()),
    ("За неделю", timedelta(weeks=1).total_seconds()),
    ("За месяц", timedelta(days=30).total_seconds()),
]


def period_kb() -> InlineKeyboardMarkup:

    now = time()

    rows = []
    for period_name, period_time in PERIODS:
        rows.append(
            [
                InlineKeyboardButton(
                    text=period_name,
                    callback_data=StatisticCallback(
                        action=StatisticAction.VIEW,
                        start_date=(now - period_time),
                        end_date=now,
                    ).pack(),
                )
            ]
        )

    rows.append([BACK_TO_MENU_BTN])

    return InlineKeyboardMarkup(inline_keyboard=rows)


def statistic_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[BACK_TO_MENU_BTN]])
