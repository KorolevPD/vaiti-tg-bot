from typing import Optional, Union

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.bot.utils import b, safe_response
from app.core.config import settings
from app.services.knowledge.schemas import DomainSummary, Grade, Specialization
from app.services.knowledge.service import KnowledgeService

from . import texts
from .fsm import SkillSelectFSM
from .keyboards import domains_kb, grades_kb, specializations_kb


async def format_header(state: FSMContext, text: str = "") -> str:
    data = await state.get_data()

    header = b(data.get("title", ""))

    parts = [
        data[key].name
        for key in ("specialization", "domain", "grade")
        if data.get(key)
    ]
    path = " | ".join(parts) if parts else None

    return "\n\n".join([s for s in (header, path, text) if s])


def get_service() -> KnowledgeService:
    return KnowledgeService(settings.SERVICES_URL)


async def choose_specialization(
    event: Union[CallbackQuery, Message],
    state: FSMContext,
) -> None:
    await state.set_state(SkillSelectFSM.specialization)
    service = get_service()
    tree = await service.get_tree()
    await safe_response(
        event,
        await format_header(state, texts.CHOOSE_SPECIALIZATION_TEXT),
        await specializations_kb(tree),
    )


async def choose_domain(
    event: Union[CallbackQuery, Message],
    state: FSMContext,
) -> None:
    await state.set_state(SkillSelectFSM.domain)
    specialization_slug = await state.get_value("specialization_slug")
    specialization = await get_specialization(specialization_slug)
    if specialization:
        await state.update_data(specialization_id=specialization.id)
        await safe_response(
            event,
            await format_header(state, texts.CHOOSE_DOMAIN_TEXT),
            await domains_kb(specialization),
        )


async def choose_grade(
    cb: CallbackQuery,
    state: FSMContext,
) -> None:
    await state.set_state(SkillSelectFSM.grade)
    service = get_service()
    domain_slug = await state.get_value("domain_slug", "")
    domain_matrix = await service.get_domain_matrix(domain_slug)
    if domain_matrix:
        await state.update_data(domain_id=domain_matrix.id)
        await safe_response(
            cb,
            await format_header(state, texts.CHOOSE_GRADE_TEXT),
            await grades_kb(domain_matrix),
        )


async def get_specialization(slug: str | None) -> Optional[Specialization]:
    tree: list[Specialization] = await get_service().get_tree()
    return next((i for i in tree if i.slug == slug), None)


async def get_domain(
    state: FSMContext, slug: str | None
) -> Optional[DomainSummary]:
    specialization_slug: Optional[str] = await state.get_value(
        "specialization_slug"
    )
    specialization = await get_specialization(specialization_slug)
    if not specialization:
        return None
    return next((d for d in specialization.domains if d.slug == slug), None)


async def get_grade(
    state: FSMContext, grade_id: int | None
) -> Optional[Grade]:
    service = get_service()
    domain_slug = await state.get_value("domain_slug", "")
    domain_matrix = await service.get_domain_matrix(domain_slug)
    if not domain_matrix:
        return None
    return next((g for g in domain_matrix.grades if g.id == grade_id), None)
