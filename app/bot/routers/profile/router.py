from aiogram import F, Router
from aiogram.filters.command import Command
from aiogram.types import CallbackQuery, Message
from aiogram.types.bot_command import BotCommand

from app.bot.utils import b, safe_response

from .callbacks import ProfileAction, ProfileCallback
from .keyboards import menu_kb
from .texts import BOT_COMMAND, BOT_COMMAND_DESCRIPTION, PROFILE_TITLE

router = Router()
bot_command = BotCommand(
    command=BOT_COMMAND, description=BOT_COMMAND_DESCRIPTION
)


@router.message(Command(bot_command))
@router.callback_query(ProfileCallback.filter(F.action == ProfileAction.MENU))
async def profile_menu(event: CallbackQuery | Message) -> None:
    await send_profile_menu(event)


async def send_profile_menu(event: CallbackQuery | Message) -> None:
    await safe_response(
        event,
        b(PROFILE_TITLE),
        menu_kb(),
    )
