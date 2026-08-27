import logging

from aiogram import Bot
from fastapi import APIRouter, Body, Depends

from app.api.dependencies import get_bot
from app.api.handlers.notification_handlers import send_notification_handler
from app.api.schemas import UsersNotificationRequest, UsersNotificationResponse

router = APIRouter()

logger = logging.getLogger(__name__)


@router.post(
    "/notifications/send",
    response_model=UsersNotificationResponse,
    summary="Отправка сообщения пользователям по Telegram ID.",
)
async def send_notification(
    data: UsersNotificationRequest = Body(...),
    bot: Bot = Depends(get_bot),
) -> UsersNotificationResponse:
    results = await send_notification_handler(data, bot)
    return UsersNotificationResponse(results=results)
