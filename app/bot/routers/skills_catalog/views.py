from typing import Optional

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from app.bot.utils import b, safe_response
from app.core.config import settings
from app.services.knowledge.service import KnowledgeService

from . import texts
from .enums import BLOCK_LABELS, SkillBlock
from .keyboards import result_kb


def get_service(auth_header: Optional[str] = None) -> KnowledgeService:
    return KnowledgeService(settings.SERVICES_URL, auth_header)


async def show_results(
    cb: CallbackQuery,
    state: FSMContext,
    block: Optional[SkillBlock] = None,
) -> None:
    auth_header = await state.get_value("auth_header")
    knowledge_service = get_service(auth_header)
    domain_slug = await state.get_value("domain_slug")
    grade_id = await state.get_value("grade_id")
    block = block or SkillBlock.DESCRIPTION

    if not (domain_slug and grade_id):
        cb.answer()
        return

    header = b(BLOCK_LABELS[block])
    text = None
    match block:
        case SkillBlock.DESCRIPTION:
            domain_matrix = await knowledge_service.get_domain_matrix(
                domain_slug
            )
            text = await texts.description_text(domain_matrix, grade_id)
        case SkillBlock.SALARY:
            pass
        case SkillBlock.STACK:
            tools = await knowledge_service.get_domain_tools(domain_slug)
            text = await texts.stack_text(tools)
        case SkillBlock.QUESTIONS:
            questions = await knowledge_service.get_typical_questions(
                domain_slug, grade_id
            )
            text = await texts.questions_text(questions)

    if not text:
        text = "Информация пока недоступна."

    await safe_response(cb, f"{header}\n\n{text}", await result_kb(block))
