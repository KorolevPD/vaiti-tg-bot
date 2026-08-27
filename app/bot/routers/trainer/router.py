from aiogram import F, Router
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.types.bot_command import BotCommand

from app.bot.flows.skill_selector.router import start_skill_select
from app.bot.flows.skill_selector.skill_finish_registry import FINISH_HANDLERS

from .callbacks import TrainerAction, TrainerCallback
from .texts import BOT_COMMAND, BOT_COMMAND_DESCRIPTION, TRAINER_TITLE
from .views import (
    back,
    select_option,
    show_results_question,
    start_interview,
    submit,
)

router = Router()
bot_command = BotCommand(
    command=BOT_COMMAND, description=BOT_COMMAND_DESCRIPTION
)

FINISH_HANDLERS["start_interview"] = start_interview


@router.message(Command(bot_command))
@router.callback_query(TrainerCallback.filter(F.action == TrainerAction.SETUP))
async def trainer_setup(
    event: CallbackQuery | Message, state: FSMContext, auth_header: str
) -> None:
    await start_skill_select(
        event,
        state,
        title=TRAINER_TITLE,
        on_finish="start_interview",
    )


@router.callback_query(TrainerCallback.filter(F.action == TrainerAction.START))
async def trainer_start(
    cb: CallbackQuery,
    state: FSMContext,
) -> None:
    if await state.get_value("domain_id"):
        await start_interview(cb, state)
    else:
        await start_skill_select(
            cb,
            state,
            title=TRAINER_TITLE,
            on_finish="start_interview",
        )


@router.callback_query(
    TrainerCallback.filter(F.action == TrainerAction.SELECT)
)
async def select_handler(
    cb: CallbackQuery,
    state: FSMContext,
    callback_data: TrainerCallback,
    auth_header: str,
) -> None:
    if callback_data.option_id:
        await select_option(cb, state, callback_data.option_id, auth_header)


@router.callback_query(TrainerCallback.filter(F.action == TrainerAction.BACK))
async def results_back(
    cb: CallbackQuery, state: FSMContext, auth_header: str
) -> None:
    current_result_question = await state.get_value(
        "current_result_question", 0
    )

    if current_result_question:
        await show_results_question(cb, state, auth_header, -1)
    else:
        await back(cb, state)


@router.callback_query(
    TrainerCallback.filter(F.action == TrainerAction.SUBMIT)
)
async def submit_handler(
    cb: CallbackQuery, state: FSMContext, auth_header: str
) -> None:
    await submit(cb, state, auth_header)


@router.callback_query(
    TrainerCallback.filter(F.action == TrainerAction.RESULTS)
)
async def results_next(
    cb: CallbackQuery, state: FSMContext, auth_header: str
) -> None:
    await show_results_question(cb, state, auth_header, 1)
