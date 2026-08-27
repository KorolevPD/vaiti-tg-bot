from math import ceil
from typing import Optional

from aiogram.types import CallbackQuery, Message
from httpx import HTTPStatusError

from app.bot.utils import b, safe_response
from app.core.config import settings
from app.services.cover_letters.schemas import GenerateRequest
from app.services.cover_letters.service import CoverLetterService
from app.services.cover_letters.storage import CoverLettersStorage

from .keyboards import back_kb, list_kb
from .texts import COVER_LETTERS_TITLE

PAGE_SIZE = 5


def get_service(auth_header: str) -> CoverLetterService:
    return CoverLetterService(settings.SERVICES_URL, auth_header)


async def show_list(
    cb: CallbackQuery,
    cl_storage: Optional[CoverLettersStorage] = None,
    page: int = 0,
) -> None:
    drafts = []
    total_pages = 0
    if cl_storage:
        user_id = cb.from_user.id
        total_pages = ceil(await cl_storage.count(user_id) / PAGE_SIZE)

        ids = await cl_storage.get_page_ids(user_id, page, PAGE_SIZE)

        for draft_id in ids:
            cached = await cl_storage.get_cached_draft(
                user_id,
                str(draft_id),
            )

            if cached:
                drafts.append(cached)
                continue

    kb = list_kb(drafts, page, total_pages)

    await safe_response(cb, b(COVER_LETTERS_TITLE), kb)


async def request_cl_generation(
    message: Message,
    auth_header: str,
    cl_storage: Optional[CoverLettersStorage] = None,
) -> None:
    service = get_service(auth_header)
    user_id = message.from_user.id if message.from_user else None
    text = message.text

    if not (user_id and text):
        return

    request = GenerateRequest()
    if text.startswith("http"):
        request.vacancy_url = text
    else:
        request.raw_vacancy_text = text

    draft = None
    text = (
        "Не удалось сгенерировать сопроводительно письмо по вашему "
        "запросу. Попробуйте повторить запрос позже или изменить его."
    )
    try:
        draft = await service.generate(request)
        if cl_storage and draft:
            await cl_storage.save_draft(user_id, draft)
        text = (
            f"Письмо поставлено в генерацию.\n"
            f"Статус: {draft.status}\n\n"
            f"Проверить можно в разделе «Сопроводительные письма»."
        )
    except HTTPStatusError:
        pass

    await safe_response(message, text, back_kb())
