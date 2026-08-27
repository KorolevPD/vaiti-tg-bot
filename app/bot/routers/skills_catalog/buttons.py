from aiogram.types import InlineKeyboardButton

from .callbacks import SkillsCatalogAction, SkillsCatalogCallback
from .texts import SKILLS_CATALOG_TITLE

SKILLS_CATALOG_BTN = InlineKeyboardButton(
    text=SKILLS_CATALOG_TITLE,
    callback_data=SkillsCatalogCallback(
        action=SkillsCatalogAction.START
    ).pack(),
)
