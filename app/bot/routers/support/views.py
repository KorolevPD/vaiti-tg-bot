from typing import Optional, Union

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.bot.utils import safe_response
from app.core.config import settings
from app.services.support import SupportService
from app.services.support.schemas import FeedbackRequest, FeedbackType

from .keyboards import choose_feedback_kb
from .texts import CHOOSE_FEEDBACK_TYPE_TEXT


def get_service() -> SupportService:
    return SupportService(settings.SERVICES_URL)


async def choose_feedback_type(event: Union[CallbackQuery, Message]) -> None:
    await safe_response(
        event,
        CHOOSE_FEEDBACK_TYPE_TEXT,
        await choose_feedback_kb(),
    )


async def send_feedback(message: Message, state: FSMContext) -> bool:
    service = get_service()
    feedback_type: Optional[FeedbackType] = await state.get_value(
        "feedback_type"
    )
    user = message.from_user
    text = message.text

    if not (feedback_type and user and text):
        return False

    data = FeedbackRequest(
        type=feedback_type,
        contact=user.username or str(user.id),
        message=text,
    )

    return await service.send_feedback(data=data)
