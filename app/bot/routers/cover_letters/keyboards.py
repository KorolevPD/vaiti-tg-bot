from typing import List

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.bot.routers.menu.buttons import BACK_TO_MENU_BTN
from app.services.cover_letters.schemas import DraftResponse

from .callbacks import CoverLettersAction, CoverLettersCallback


def cover_letters_menu_kb(
    drafts: List[DraftResponse],
    page: int,
    total_pages: int,
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for draft in drafts:
        builder.button(
            text=f"{draft.status} | {draft.tone}",
            callback_data=CoverLettersCallback(
                action=CoverLettersAction.VIEW,
                draft_id=str(draft.id),
            ).pack(),
        )

    if page > 0:
        builder.button(
            text="⬅",
            callback_data=CoverLettersCallback(
                action=CoverLettersAction.LIST, page=page - 1
            ).pack(),
        )
    if page < total_pages - 1:
        builder.button(
            text="➡",
            callback_data=CoverLettersCallback(
                action=CoverLettersAction.LIST, page=page + 1
            ).pack(),
        )

    builder.button(
        text="➕ Создать новое",
        callback_data=CoverLettersCallback(
            action=CoverLettersAction.CREATE
        ).pack(),
    )

    builder.adjust(1)
    return builder.as_markup()


def list_kb(
    drafts: List[DraftResponse], page: int, total_pages: int
) -> InlineKeyboardMarkup:
    rows: list[list[InlineKeyboardButton]] = []

    for draft in drafts:
        rows.append(
            [
                InlineKeyboardButton(
                    text=f"{draft.status} | {draft.tone}",
                    callback_data=CoverLettersCallback(
                        action=CoverLettersAction.VIEW,
                        draft_id=str(draft.id),
                    ).pack(),
                )
            ]
        )

    nav_row: list[InlineKeyboardButton] = []
    if page > 0:
        nav_row.append(
            InlineKeyboardButton(
                text=f"‹ {page}",
                callback_data=CoverLettersCallback(
                    action=CoverLettersAction.LIST, page=page - 1
                ).pack(),
            )
        )
    if total_pages > 1:
        nav_row.append(
            InlineKeyboardButton(text=f"‧ {page + 1} ‧", callback_data="noop")
        )
    if page < total_pages - 1:
        nav_row.append(
            InlineKeyboardButton(
                text=f"{page + 2} ›",
                callback_data=CoverLettersCallback(
                    action=CoverLettersAction.LIST, page=page + 1
                ).pack(),
            )
        )
    if nav_row:
        rows.append(nav_row)

    rows.append(
        [
            InlineKeyboardButton(
                text="➕ Создать новое",
                callback_data=CoverLettersCallback(
                    action=CoverLettersAction.CREATE
                ).pack(),
            ),
            InlineKeyboardButton(
                text="🔄 Обновить",
                callback_data=CoverLettersCallback(
                    action=CoverLettersAction.LIST
                ).pack(),
            ),
        ]
    )

    rows.append([BACK_TO_MENU_BTN])

    return InlineKeyboardMarkup(inline_keyboard=rows)


def back_kb() -> InlineKeyboardMarkup:
    rows = [
        [
            InlineKeyboardButton(
                text="‹ Назад",
                callback_data=CoverLettersCallback(
                    action=CoverLettersAction.LIST
                ).pack(),
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=rows)
