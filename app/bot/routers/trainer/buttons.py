from aiogram.types import InlineKeyboardButton

from .callbacks import TrainerAction, TrainerCallback
from .texts import TRAINER_TITLE

TRAINER_BTN = InlineKeyboardButton(
    text=TRAINER_TITLE,
    callback_data=TrainerCallback(action=TrainerAction.SETUP).pack(),
)

RESTART_BTN = InlineKeyboardButton(
    text="🔄 Повторить",
    callback_data=TrainerCallback(
        action=TrainerAction.START,
    ).pack(),
)
