import logging
from typing import Dict

from aiogram import Bot
from aiogram.exceptions import TelegramAPIError, TelegramForbiddenError

from app.api.schemas import UsersNotificationRequest
from app.core.config import settings

logger = logging.getLogger(__name__)

bot = Bot(token=settings.BOT_TOKEN)


async def send_notification_handler(
    data: UsersNotificationRequest,
    bot: Bot,
) -> Dict[int, str]:
    results: Dict[int, str] = {}
    for user_id in data.user_ids:
        try:
            await bot.send_message(
                chat_id=user_id,
                text=data.message,
                disable_web_page_preview=True,
            )
            results[user_id] = "ok"

        except TelegramForbiddenError:
            results[user_id] = "bot_blocked"

        except TelegramAPIError as e:
            if "chat not found" in str(e).lower():
                results[user_id] = "not_found"
            else:
                results[user_id] = f"error: {e}"

        except Exception as e:
            results[user_id] = f"error: {e}"

    return results
