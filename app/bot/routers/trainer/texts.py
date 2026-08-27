from app.services.trainer.schemas import (
    InterviewQuestion,
    InterviewResult,
    QuestionResult,
)

BOT_COMMAND = "trainer"
BOT_COMMAND_DESCRIPTION = "Тренажер собеседований"

TRAINER_TITLE = "🧠 Тренажер собеседований"

TRAINER_START_TEXT = "<b>Тренажер</b>\n" "Здесь будет тренажер."


def result_text(results: InterviewResult) -> str:
    return (
        "<b>Результаты:</b>\n\n"
        f"Верно {results.correct_answers} из {len(results.questions)}"
    )


def question_text(
    q: InterviewQuestion, current_question: int, total_questions: int
) -> str:
    return (
        f"<b>Вопрос {current_question} из {total_questions}</b>\n\n"
        f"{q.text}"
    )


def result_question_text(
    q: QuestionResult, current_question: int, total_questions: int
) -> str:
    lines = [
        f"<b>Вопрос {current_question} из {total_questions}</b>\n",
        q.question_text,
        "",
    ]

    for option in q.options:
        is_correct = option.id in q.correct_answer_option_ids
        is_user = option.id in q.user_answer_option_ids

        if is_correct and is_user:
            prefix = "✅"
        elif is_correct and not is_user:
            prefix = "🟩"
        elif not is_correct and is_user:
            prefix = "❌"
        else:
            prefix = "⬜"

        lines.append(f"{prefix} {option.text}")

    return "\n".join(lines)
