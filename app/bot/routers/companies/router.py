from aiogram import F, Router
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.types.bot_command import BotCommand

from app.bot.utils import safe_response

from .callbacks import CompaniesAction, CompaniesCallback
from .fsm import CompaniesState
from .keyboards import search_kb
from .texts import BOT_COMMAND, BOT_COMMAND_DESCRIPTION
from .views import show_companies, show_company_view

router = Router()
bot_command = BotCommand(
    command=BOT_COMMAND, description=BOT_COMMAND_DESCRIPTION
)


@router.message(Command(bot_command))
@router.callback_query(
    CompaniesCallback.filter(F.action == CompaniesAction.START)
)
async def companies_start(
    event: CallbackQuery | Message, state: FSMContext
) -> None:
    await state.set_state(CompaniesState.waiting_for_query)
    text = "Введите текст для поиска компаний:"

    await safe_response(event, text, search_kb())


@router.message(CompaniesState.waiting_for_query)
async def companies_search(
    message: Message,
    state: FSMContext,
) -> None:
    await state.update_data(query=message.text)
    await state.set_state(None)

    await show_companies(message, state, page=0)


@router.callback_query(
    CompaniesCallback.filter(F.action == CompaniesAction.PAGE)
)
async def companies_page(
    cb: CallbackQuery,
    callback_data: CompaniesCallback,
    state: FSMContext,
) -> None:
    page = callback_data.page if callback_data.page else 0
    await show_companies(cb, state, page=page)


@router.callback_query(
    CompaniesCallback.filter(F.action == CompaniesAction.VIEW)
)
async def companies_view(
    cb: CallbackQuery,
    callback_data: CompaniesCallback,
) -> None:
    company_id = callback_data.company_id
    page = callback_data.page if callback_data.page else 0
    if company_id:
        await show_company_view(cb, company_id, page)
