from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.bot.routers.menu.buttons import BACK_TO_MENU_BTN
from app.bot.routers.trainer.callbacks import TrainerAction, TrainerCallback

from .callbacks import SkillsCatalogAction, SkillsCatalogCallback
from .enums import BLOCK_LABELS, SkillBlock


def _action_button(
    text: str,
    action: SkillsCatalogAction,
    *,
    item_slug: str | None = None,
    item_id: int | None = None,
    block: SkillBlock | None = None,
) -> InlineKeyboardButton:
    return InlineKeyboardButton(
        text=text,
        callback_data=SkillsCatalogCallback(
            action=action,
            item_slug=item_slug,
            item_id=item_id,
            block=block,
        ).pack(),
    )


async def result_kb(active: SkillBlock | None = None) -> InlineKeyboardMarkup:
    active = active or SkillBlock.DESCRIPTION

    extra_rows = await _extra_rows(active)

    nav_rows = [
        _action_button(
            BLOCK_LABELS[block], SkillsCatalogAction.BLOCK, block=block
        )
        for block in SkillBlock
        if block != active
    ]

    return InlineKeyboardMarkup(
        inline_keyboard=[
            nav_rows,
            *extra_rows,
            [BACK_TO_MENU_BTN],
        ]
    )


async def _extra_rows(active: SkillBlock) -> list[list[InlineKeyboardButton]]:

    if active == SkillBlock.QUESTIONS:
        return [
            [
                InlineKeyboardButton(
                    text="🧠 Запустить тренажер",
                    callback_data=TrainerCallback(
                        action=TrainerAction.START,
                    ).pack(),
                )
            ],
        ]
    else:
        return []
