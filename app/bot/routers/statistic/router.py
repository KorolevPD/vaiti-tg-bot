from aiogram import F, Router
from aiogram.filters.command import Command
from aiogram.types import CallbackQuery, Message
from aiogram.types.bot_command import BotCommand

from app.bot.utils import safe_response

from .callbacks import StatisticAction, StatisticCallback
from .keyboards import period_kb
from .texts import BOT_COMMAND, BOT_COMMAND_DESCRIPTION
from .views import show_statistic

router = Router()
bot_command = BotCommand(
    command=BOT_COMMAND, description=BOT_COMMAND_DESCRIPTION
)


@router.message(Command(bot_command))
@router.callback_query(
    StatisticCallback.filter(F.action == StatisticAction.START)
)
async def statistic_start(event: CallbackQuery | Message) -> None:
    await safe_response(event, "Выбери период:", period_kb())


@router.callback_query(
    StatisticCallback.filter(F.action == StatisticAction.VIEW)
)
async def statistic_view(
    cb: CallbackQuery,
    callback_data: StatisticCallback,
    auth_header: str,
) -> None:
    if not (callback_data.start_date and callback_data.end_date):
        return

    await show_statistic(
        cb,
        auth_header,
        callback_data.start_date,
        callback_data.end_date,
    )
