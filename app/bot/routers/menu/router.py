from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.types.bot_command import BotCommand

from app.bot.utils import safe_response

from .callbacks import MenuAction, MenuCallback
from .keyboards import menu_kb
from .texts import (
    BOT_COMMAND,
    BOT_COMMAND_DESCRIPTION,
    MENU_START_TEXT,
    greetings_text,
)

router = Router()
bot_command = BotCommand(
    command=BOT_COMMAND, description=BOT_COMMAND_DESCRIPTION
)


@router.message(CommandStart())
async def start_handler(msg: Message, state: FSMContext) -> None:
    user = msg.from_user
    name = (user.first_name or user.username) if user else None

    await state.set_state(None)
    await safe_response(msg, greetings_text(name))
    await send_main_menu(msg)


@router.message(Command(bot_command))
@router.callback_query(MenuCallback.filter(F.action == MenuAction.START))
async def menu_start(
    event: CallbackQuery | Message, state: FSMContext
) -> None:
    await state.set_state(None)
    await send_main_menu(event)


async def send_main_menu(event: CallbackQuery | Message) -> None:
    await safe_response(
        event,
        MENU_START_TEXT,
        menu_kb(),
    )
