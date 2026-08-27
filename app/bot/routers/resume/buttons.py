from aiogram.types import InlineKeyboardButton

from .callbacks import ResumeAction, ResumeCallback
from .texts import DOWNLOAD_TITLE, UPLOAD_TITLE

UPLOAD_BTN = InlineKeyboardButton(
    text=UPLOAD_TITLE,
    callback_data=ResumeCallback(action=ResumeAction.UPLOAD).pack(),
)

DOWNLOAD_BTN = InlineKeyboardButton(
    text=DOWNLOAD_TITLE,
    callback_data=ResumeCallback(action=ResumeAction.DOWNLOAD).pack(),
)
