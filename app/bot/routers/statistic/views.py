from aiogram.types import CallbackQuery

from app.bot.utils import safe_response
from app.core.config import settings
from app.services.application.service import ApplicationService

from .keyboards import statistic_kb
from .texts import statistic_text


def get_service(auth_header: str) -> ApplicationService:
    return ApplicationService(settings.SERVICES_URL, auth_header)


async def show_statistic(
    cb: CallbackQuery, auth_header: str, s_date: float, e_date: float
) -> None:

    service = get_service(auth_header)
    stats = await service.get_stats(s_date, e_date)

    await safe_response(
        cb, statistic_text(stats, s_date, e_date), statistic_kb()
    )
