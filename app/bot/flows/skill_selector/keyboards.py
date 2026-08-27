from typing import List, Optional

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.bot.routers.menu.buttons import BACK_TO_MENU_BTN
from app.services.knowledge.schemas import DomainMatrixResponse, Specialization

from .callbacks import SkillSelectAction, SkillSelectCallback
from .texts import BACK_BTN_TEXT


def _action_button(
    text: str,
    action: SkillSelectAction,
    *,
    item_slug: str | None = None,
    item_id: int | None = None,
) -> InlineKeyboardButton:
    return InlineKeyboardButton(
        text=text,
        callback_data=SkillSelectCallback(
            action=action,
            item_slug=item_slug,
            item_id=item_id,
        ).pack(),
    )


BACK_BTN = _action_button(BACK_BTN_TEXT, SkillSelectAction.BACK)


async def specializations_kb(
    tree: List[Specialization],
) -> InlineKeyboardMarkup:
    rows = [
        [
            _action_button(
                item.name,
                SkillSelectAction.SPECIALIZATION,
                item_slug=item.slug,
            )
        ]
        for item in tree or []
    ]
    rows.append([BACK_TO_MENU_BTN])

    return InlineKeyboardMarkup(inline_keyboard=rows)


async def domains_kb(
    specialization: Optional[Specialization],
) -> InlineKeyboardMarkup:

    rows = (
        [
            [
                _action_button(
                    item.name, SkillSelectAction.DOMAIN, item_slug=item.slug
                )
            ]
            for item in specialization.domains
        ]
        if specialization
        else []
    )

    rows.append([BACK_BTN])

    return InlineKeyboardMarkup(inline_keyboard=rows)


async def grades_kb(
    domain_matrix: Optional[DomainMatrixResponse],
) -> InlineKeyboardMarkup:

    rows = (
        [
            [
                _action_button(
                    item.name, SkillSelectAction.GRADE, item_id=item.id
                )
            ]
            for item in domain_matrix.grades
        ]
        if domain_matrix
        else []
    )

    rows.append([BACK_BTN])

    return InlineKeyboardMarkup(inline_keyboard=rows)
