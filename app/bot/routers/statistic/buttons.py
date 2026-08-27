from aiogram.types import InlineKeyboardButton

from .callbacks import StatisticAction, StatisticCallback
from .texts import STATISTIC_TITLE

STATISTIC_BTN = InlineKeyboardButton(
    text=STATISTIC_TITLE,
    callback_data=StatisticCallback(action=StatisticAction.START).pack(),
)
