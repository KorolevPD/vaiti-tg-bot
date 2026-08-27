from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.bot.utils import safe_response
from app.core.config import settings
from app.services.companies.service import CompaniesService

from .keyboards import companies_kb, company_kb, search_kb
from .texts import company_text, not_found_text, result_text

PAGE_SIZE = 5


def get_service() -> CompaniesService:
    return CompaniesService(settings.SERVICES_URL)


async def show_companies(
    event: CallbackQuery | Message,
    state: FSMContext,
    page: int = 0,
) -> None:
    data = await state.get_data()
    query: str | None = data.get("query")

    service = get_service()

    result = await service.get_all(
        page=page,
        size=PAGE_SIZE,
        query=query,
    )

    content = result.content if result.content else []
    total_pages = (
        result.page.total_pages
        if result.page and result.page.total_pages
        else 1
    )

    if not content:
        text = not_found_text(query)
        await safe_response(event, text, search_kb())
        return

    text = result_text(query, page, total_pages)

    kb = companies_kb(content if content else [], page, total_pages)

    await safe_response(event, text, reply_markup=kb)


async def show_company_view(
    event: CallbackQuery, company_id: str, page: int
) -> None:
    service = get_service()
    company = await service.get_by_id(company_id)

    await safe_response(
        event,
        company_text(company),
        company_kb(company, page),
        photo_url=company.logo_url,
    )
