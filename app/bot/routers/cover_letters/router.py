from typing import Optional

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.types.bot_command import BotCommand

from app.bot.utils import safe_response
from app.services.cover_letters.storage import CoverLettersStorage

from .callbacks import CoverLettersAction, CoverLettersCallback
from .fsm import CoverLettersState
from .keyboards import back_kb
from .texts import BOT_COMMAND, BOT_COMMAND_DESCRIPTION
from .views import request_cl_generation, show_list

router = Router()
bot_command = BotCommand(
    command=BOT_COMMAND, description=BOT_COMMAND_DESCRIPTION
)


@router.callback_query(
    CoverLettersCallback.filter(F.action == CoverLettersAction.LIST)
)
async def cover_letters_list(
    cb: CallbackQuery,
    callback_data: CoverLettersCallback,
    cl_storage: CoverLettersStorage,
    state: FSMContext,
) -> None:
    await state.set_state(None)
    page = callback_data.page or 0
    await show_list(cb, cl_storage, page)


@router.callback_query(
    CoverLettersCallback.filter(F.action == CoverLettersAction.CREATE)
)
async def cover_letter_create(
    cb: CallbackQuery,
    state: FSMContext,
) -> None:
    await state.set_state(CoverLettersState.waiting_for_context)
    await safe_response(
        cb,
        "Отправьте ссылку на вакансию или текст вакансии.",
        back_kb(),
    )


@router.message(CoverLettersState.waiting_for_context)
async def cover_letter_generate(
    message: Message,
    auth_header: str,
    cl_storage: Optional[CoverLettersStorage],
    state: FSMContext,
) -> None:
    await request_cl_generation(message, auth_header, cl_storage)
    await state.clear()
