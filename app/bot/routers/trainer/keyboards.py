from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.bot.routers.menu.buttons import BACK_TO_MENU_BTN
from app.services.trainer.schemas import (
    InterviewQuestion,
    InterviewResult,
    QuestionType,
)

from .buttons import RESTART_BTN
from .callbacks import TrainerAction, TrainerCallback


def question_kb(
    q: InterviewQuestion, current_question: int, total_questions: int
) -> InlineKeyboardMarkup:
    rows = []
    for option in q.options:
        if q.question_type == QuestionType.SINGLE_CHOICE:
            prefix = "🔘 " if option.id in q.selected_option_ids else "⚪ "
        else:
            prefix = "⏹️ " if option.id in q.selected_option_ids else "◻️ "

        rows.append(
            [
                InlineKeyboardButton(
                    text=f"{prefix} {option.text}",
                    callback_data=TrainerCallback(
                        action=TrainerAction.SELECT, option_id=option.id
                    ).pack(),
                )
            ]
        )

    nav = []
    if current_question != 1:
        nav.append(
            InlineKeyboardButton(
                text="⬅️ Назад",
                callback_data=TrainerCallback(
                    action=TrainerAction.BACK
                ).pack(),
            )
        )
    nav.append(
        InlineKeyboardButton(
            text=(
                "Далее ➡️"
                if current_question != total_questions
                else "Готово ✅"
            ),
            callback_data=TrainerCallback(action=TrainerAction.SUBMIT).pack(),
        ),
    )

    return InlineKeyboardMarkup(
        inline_keyboard=[
            *rows,
            nav,
            [BACK_TO_MENU_BTN],
        ]
    )


def results_kb(results: InterviewResult) -> InlineKeyboardMarkup:
    nav = [
        RESTART_BTN,
        InlineKeyboardButton(
            text="🔍 Подробнее",
            callback_data=TrainerCallback(
                action=TrainerAction.RESULTS,
            ).pack(),
        ),
    ]

    return InlineKeyboardMarkup(
        inline_keyboard=[
            nav,
            [BACK_TO_MENU_BTN],
        ]
    )


def result_question_kb(
    current_question: int,
    total_questions: int,
) -> InlineKeyboardMarkup:
    nav = []

    if current_question > 1:
        nav.append(
            InlineKeyboardButton(
                text="⬅️ Назад",
                callback_data=TrainerCallback(
                    action=TrainerAction.BACK
                ).pack(),
            )
        )

    if current_question < total_questions:
        nav.append(
            InlineKeyboardButton(
                text="Далее ➡️",
                callback_data=TrainerCallback(
                    action=TrainerAction.RESULTS
                ).pack(),
            )
        )

    return InlineKeyboardMarkup(
        inline_keyboard=[
            nav,
            [RESTART_BTN],
            [BACK_TO_MENU_BTN],
        ]
    )
