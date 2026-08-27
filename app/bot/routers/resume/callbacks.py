from enum import StrEnum

from aiogram.filters.callback_data import CallbackData


class ResumeAction(StrEnum):
    UPLOAD = "upload"
    DOWNLOAD = "download"


class ResumeCallback(CallbackData, prefix="resume"):
    action: ResumeAction
