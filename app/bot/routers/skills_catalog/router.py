from aiogram import F, Router
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.types.bot_command import BotCommand

from app.bot.flows.skill_selector.router import start_skill_select
from app.bot.flows.skill_selector.skill_finish_registry import FINISH_HANDLERS

from . import texts
from .callbacks import SkillsCatalogAction, SkillsCatalogCallback
from .views import show_results

router = Router()
bot_command = BotCommand(
    command=texts.BOT_COMMAND,
    description=texts.BOT_COMMAND_DESCRIPTION,
)

FINISH_HANDLERS["show_results"] = show_results


@router.message(Command(bot_command))
@router.callback_query(
    SkillsCatalogCallback.filter(F.action == SkillsCatalogAction.START)
)
async def skills_catalog_start(
    event: CallbackQuery | Message, state: FSMContext
) -> None:
    await start_skill_select(
        event,
        state,
        title=texts.SKILLS_CATALOG_TITLE,
        on_finish="show_results",
    )


@router.callback_query(
    SkillsCatalogCallback.filter(F.action == SkillsCatalogAction.BLOCK)
)
async def block_handler(
    cb: CallbackQuery,
    callback_data: SkillsCatalogCallback,
    state: FSMContext,
) -> None:
    await cb.answer()
    await show_results(cb, state, callback_data.block)
