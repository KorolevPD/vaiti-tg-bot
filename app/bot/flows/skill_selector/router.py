from typing import Optional

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from .callbacks import SkillSelectAction, SkillSelectCallback
from .fsm import SkillSelectFSM
from .skill_finish_registry import FINISH_HANDLERS
from .views import (
    choose_domain,
    choose_grade,
    choose_specialization,
    get_domain,
    get_grade,
    get_specialization,
)

router = Router()

# ===== PUBLIC ENTRY POINT =====


async def start_skill_select(
    event: Message | CallbackQuery,
    state: FSMContext,
    title: Optional[str],
    on_finish: Optional[str],
) -> None:
    await state.update_data(title=title)
    await state.update_data(on_finish=on_finish)
    await choose_specialization(event, state)


# ===== HANDLERS =====


@router.callback_query(
    SkillSelectCallback.filter(F.action == SkillSelectAction.SPECIALIZATION)
)
async def specialization_handler(
    cb: CallbackQuery,
    callback_data: SkillSelectCallback,
    state: FSMContext,
) -> None:
    await cb.answer()

    specialization = await get_specialization(callback_data.item_slug)
    if specialization:
        await state.update_data(specialization_slug=specialization.slug)
    await choose_domain(cb, state)


@router.callback_query(
    SkillSelectCallback.filter(F.action == SkillSelectAction.DOMAIN)
)
async def domain_handler(
    cb: CallbackQuery,
    callback_data: SkillSelectCallback,
    state: FSMContext,
) -> None:
    await cb.answer()

    domain = await get_domain(state, callback_data.item_slug)
    if domain:
        await state.update_data(domain_slug=domain.slug)
    await choose_grade(cb, state)


@router.callback_query(
    SkillSelectCallback.filter(F.action == SkillSelectAction.GRADE)
)
async def grade_handler(
    cb: CallbackQuery,
    callback_data: SkillSelectCallback,
    state: FSMContext,
) -> None:
    await cb.answer()

    grade = await get_grade(state, callback_data.item_id)
    if grade:
        await state.update_data(grade_id=grade.id)

    await finish_skill_select(cb, state)


@router.callback_query(
    SkillSelectCallback.filter(F.action == SkillSelectAction.BACK)
)
async def back_handler(cb: CallbackQuery, state: FSMContext) -> None:
    await cb.answer()

    current = await state.get_state()

    if current == SkillSelectFSM.grade:
        await choose_domain(cb, state)
    elif current == SkillSelectFSM.domain:
        await choose_specialization(cb, state)


# ===== FLOW FINISH =====


async def finish_skill_select(
    cb: CallbackQuery,
    state: FSMContext,
) -> None:
    data = await state.get_data()
    key = data.get("on_finish")

    if key and key in FINISH_HANDLERS:
        await FINISH_HANDLERS[key](cb, state)
