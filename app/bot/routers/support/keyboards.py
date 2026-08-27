from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.bot.routers.menu.buttons import BACK_TO_MENU_BTN

from .callbacks import SupportAction, SupportCallback
from .enums import FEELBACK_LABLES


def support_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[BACK_TO_MENU_BTN]])


async def choose_feedback_kb() -> InlineKeyboardMarkup:
    rows = []
    for key, value in FEELBACK_LABLES.items():
        rows.append(
            [
                InlineKeyboardButton(
                    text=value,
                    callback_data=SupportCallback(
                        action=SupportAction.FEEDBACK_TYPE,
                        feedback_type=key,
                    ).pack(),
                )
            ]
        )

    return InlineKeyboardMarkup(
        inline_keyboard=[
            *rows,
            [BACK_TO_MENU_BTN],
        ]
    )
