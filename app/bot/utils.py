import logging
import re
from typing import Optional

from aiogram.exceptions import TelegramBadRequest
from aiogram.types import (
    CallbackQuery,
    InaccessibleMessage,
    InlineKeyboardMarkup,
    InputMediaPhoto,
    Message,
    TelegramObject,
)
from pydantic import HttpUrl

logger = logging.getLogger(__name__)


def a(s: str, url: Optional[str | HttpUrl]) -> str:
    if url:
        return f"<a href='{url}'>{s}</a>"
    return s


def b(s: str) -> str:
    return f"<b>{s}</b>"


def quote(text: str, expandable: bool = False) -> str:
    expandable_str = " expandable" if expandable else ""
    return f"<blockquote{expandable_str}>{text}</blockquote>"


def remove_html_tags(text: str) -> str:
    return re.sub(r"<[^>]+>", "", text)


def same_buttons(
    a: Optional[InlineKeyboardMarkup], b: Optional[InlineKeyboardMarkup]
) -> bool:
    if not a or not b:
        return False
    a_rows = [[btn.text for btn in row] for row in a.inline_keyboard]
    b_rows = [[btn.text for btn in row] for row in b.inline_keyboard]
    return a_rows == b_rows


async def safe_response(
    telegram_object: Optional[TelegramObject],
    text: str,
    reply_markup: Optional[InlineKeyboardMarkup] = None,
    photo_url: Optional[str] = None,
) -> None:

    # Message
    if isinstance(telegram_object, Message):
        if photo_url:
            await telegram_object.answer_photo(
                photo=photo_url,
                caption=text,
                reply_markup=reply_markup,
            )
        else:
            await telegram_object.answer(
                text,
                reply_markup=reply_markup,
                disable_web_page_preview=True,
            )
        return

    # CallbackQuery
    if isinstance(telegram_object, CallbackQuery):
        try:
            await telegram_object.answer()
        except TelegramBadRequest:
            pass

        msg = telegram_object.message

        # Если нет сообщения, тогда отправляем новое
        if msg is None or isinstance(msg, InaccessibleMessage):
            if telegram_object.bot:
                if photo_url:
                    await telegram_object.bot.send_photo(
                        telegram_object.from_user.id,
                        photo=photo_url,
                        caption=text,
                        reply_markup=reply_markup,
                    )
                else:
                    await telegram_object.bot.send_message(
                        telegram_object.from_user.id,
                        text,
                        reply_markup=reply_markup,
                        disable_web_page_preview=True,
                    )
            return

        # Если текст и клавиатура совпадают, не трогаем
        if (
            not photo_url
            and remove_html_tags(text) == (msg.text or "")
            and same_buttons(msg.reply_markup, reply_markup)
        ):
            await telegram_object.answer()
            return

        # Пытаемся изменить сообщение
        try:
            if photo_url:
                media = InputMediaPhoto(media=photo_url, caption=text)
                await msg.edit_media(media=media, reply_markup=reply_markup)
            else:
                await msg.edit_text(
                    text,
                    reply_markup=reply_markup,
                    disable_web_page_preview=True,
                )
        except TelegramBadRequest:
            # fallback — отправляем новое сообщение
            if photo_url:
                await msg.answer_photo(
                    photo=photo_url,
                    caption=text,
                    reply_markup=reply_markup,
                )
            else:
                await msg.answer(
                    text,
                    reply_markup=reply_markup,
                    disable_web_page_preview=True,
                )
            await msg.delete()
