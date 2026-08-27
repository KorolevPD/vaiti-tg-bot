from aiogram import F, Router
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.types.bot_command import BotCommand

from .callbacks import VacanciesAction, VacanciesCallback
from .texts import BOT_COMMAND, BOT_COMMAND_DESCRIPTION
from .views import save_interacrion, search_vacancies

router = Router()
bot_command = BotCommand(
    command=BOT_COMMAND, description=BOT_COMMAND_DESCRIPTION
)


@router.message(Command(bot_command))
@router.callback_query(
    VacanciesCallback.filter(F.action == VacanciesAction.START)
)
async def vacancies_start(
    event: CallbackQuery | Message, state: FSMContext, auth_header: str
) -> None:
    await search_vacancies(event, state, auth_header)


@router.callback_query(
    VacanciesCallback.filter(F.action == VacanciesAction.REACTION)
)
async def vacancies_interaction(
    cb: CallbackQuery,
    state: FSMContext,
    callback_data: VacanciesCallback,
    auth_header: str,
) -> None:

    await save_interacrion(cb, state, auth_header, callback_data)
