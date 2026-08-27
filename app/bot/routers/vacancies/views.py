from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, Message

from app.bot.routers.menu.buttons import BACK_TO_MENU_BTN
from app.bot.utils import safe_response
from app.core.config import settings
from app.services.vacancies.schemas import InteractionRequest
from app.services.vacancies.service import VacancyService

from .callbacks import VacanciesCallback
from .keyboards import vacancy_kb
from .texts import VACANCIES_TITLE, vacancy_text


def get_service(auth_header: str) -> VacancyService:
    return VacancyService(settings.SERVICES_URL, auth_header)


async def search_vacancies(
    event: CallbackQuery | Message, state: FSMContext, auth_header: str
) -> None:
    service = get_service(auth_header)

    try:
        r = await service.search()
        vacancies = r.content
        if not vacancies:
            raise LookupError
    except Exception:
        await safe_response(
            event,
            f"{VACANCIES_TITLE}\n\n"
            "Не удалось найти подходящих ваканси. "
            "Попробуй добавить резюме или попробовть позже.",
            InlineKeyboardMarkup(inline_keyboard=[[BACK_TO_MENU_BTN]]),
        )
        return

    vacancies_ids = []
    for v in vacancies:
        vacancies_ids.append(v.id)

    await state.update_data(vacancies_ids=vacancies_ids)

    await show_vacancy(event, state, auth_header)


async def show_vacancy(
    event: CallbackQuery | Message, state: FSMContext, auth_header: str
) -> None:
    service = get_service(auth_header)

    vacancies_ids = await state.get_value("vacancies_ids")
    if not vacancies_ids:
        await search_vacancies(event, state, auth_header)
        return

    try:
        vacancy = await service.get_by_id(vacancies_ids.pop(0))
    except Exception:
        await safe_response(
            event,
            f"{VACANCIES_TITLE}\n\nНе удалось получить карточку вакансии.",
            InlineKeyboardMarkup(inline_keyboard=[[BACK_TO_MENU_BTN]]),
        )
        return

    await safe_response(
        event,
        vacancy_text(vacancy),
        vacancy_kb(vacancy),
        vacancy.company_logo_url,
    )


async def save_interacrion(
    cb: CallbackQuery,
    state: FSMContext,
    auth_header: str,
    callback_data: VacanciesCallback,
) -> None:
    if not (callback_data.vacancy_id and callback_data.interaction_type):
        return

    service = get_service(auth_header)
    data = InteractionRequest(
        vacancy_id=callback_data.vacancy_id,
        type=callback_data.interaction_type,
    )

    try:
        await service.record_interaction(data)
    except Exception:
        await cb.answer("Ошибка при обработке реакции.")
        return

    await show_vacancy(cb, state, auth_header)
