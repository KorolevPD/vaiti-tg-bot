from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    WebAppInfo,
)

from app.bot.routers.menu.buttons import BACK_TO_MENU_BTN
from app.services.companies.schemas import CompanyResponse

from .callbacks import CompaniesAction, CompaniesCallback


def search_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[BACK_TO_MENU_BTN]])


def companies_kb(
    items: list[CompanyResponse],
    page: int,
    total_pages: int,
) -> InlineKeyboardMarkup:
    rows: list[list[InlineKeyboardButton]] = []

    for item in items:
        rows.append(
            [
                InlineKeyboardButton(
                    text=item.name,
                    callback_data=CompaniesCallback(
                        action=CompaniesAction.VIEW,
                        company_id=str(item.id),
                        page=page,
                    ).pack(),
                )
            ]
        )

    nav_row: list[InlineKeyboardButton] = []
    if page > 0:
        nav_row.append(
            InlineKeyboardButton(
                text=f"‹ {page}",
                callback_data=CompaniesCallback(
                    action=CompaniesAction.PAGE,
                    page=page - 1,
                ).pack(),
            )
        )
    if page != total_pages - 1:
        nav_row.append(
            InlineKeyboardButton(text=f"‧ {page + 1} ‧", callback_data="noop")
        )
    if page + 1 < total_pages:
        nav_row.append(
            InlineKeyboardButton(
                text=f"{page + 2} ›",
                callback_data=CompaniesCallback(
                    action=CompaniesAction.PAGE,
                    page=page + 1,
                ).pack(),
            )
        )
    if nav_row:
        rows.append(nav_row)

    rows.append([BACK_TO_MENU_BTN])

    return InlineKeyboardMarkup(inline_keyboard=rows)


def company_kb(c: CompanyResponse, page: int) -> InlineKeyboardMarkup:
    rows = [
        [
            InlineKeyboardButton(
                text="🔍 Подробнее",
                web_app=WebAppInfo(
                    url=f"https://vaiti.tech/companies/{c.slug}"
                ),
            )
        ],
        [
            InlineKeyboardButton(
                text="‹ Назад",
                callback_data=CompaniesCallback(
                    action=CompaniesAction.PAGE, page=page
                ).pack(),
            )
        ],
        [BACK_TO_MENU_BTN],
    ]

    return InlineKeyboardMarkup(inline_keyboard=rows)
