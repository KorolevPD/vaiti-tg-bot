from typing import Union

from aiogram import F, Router
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, Message
from aiogram.types.bot_command import BotCommand

from app.bot.routers.menu.buttons import BACK_TO_MENU_BTN
from app.bot.utils import safe_response

from .callbacks import SupportAction, SupportCallback
from .fsm import SupportState
from .texts import FAILURE_FEEDBACK_TEXT, SUCCESS_FEEDBACK_TEXT, SUPPORT_TITLE
from .views import choose_feedback_type, send_feedback

router = Router()
bot_command = BotCommand(command="support", description=SUPPORT_TITLE)


@router.message(Command(bot_command))
@router.callback_query(SupportCallback.filter(F.action == SupportAction.START))
async def support_start_callback(event: Union[Message, CallbackQuery]) -> None:
    await choose_feedback_type(event)


@router.callback_query(
    SupportCallback.filter(F.action == SupportAction.FEEDBACK_TYPE)
)
async def support_feedback_type_callback(
    cb: CallbackQuery,
    callback_data: SupportCallback,
    state: FSMContext,
) -> None:
    await cb.answer()

    feedback_type = callback_data.feedback_type
    if feedback_type:
        await state.update_data(feedback_type=feedback_type)

    await safe_response(
        cb,
        "Опишите вашу проблему.",
        InlineKeyboardMarkup(inline_keyboard=[[BACK_TO_MENU_BTN]]),
    )
    await state.set_state(SupportState.waiting_for_feedback)


@router.message(SupportState.waiting_for_feedback)
async def handle_feedback(message: Message, state: FSMContext) -> None:
    success = await send_feedback(message, state)
    await safe_response(
        message,
        SUCCESS_FEEDBACK_TEXT if success else FAILURE_FEEDBACK_TEXT,
        InlineKeyboardMarkup(inline_keyboard=[[BACK_TO_MENU_BTN]]),
    )
