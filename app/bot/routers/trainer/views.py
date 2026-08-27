from typing import List, Optional

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from app.bot.utils import safe_response
from app.core.config import settings
from app.services.trainer.schemas import (
    InterviewQuestion,
    QuestionType,
    SaveAnswerRequest,
    StartInterviewRequest,
)
from app.services.trainer.service import TrainerService

from .keyboards import question_kb, result_question_kb, results_kb
from .texts import question_text, result_question_text, result_text


def get_service(auth_header: str) -> TrainerService:
    return TrainerService(settings.SERVICES_URL, auth_header)


async def start_interview(cb: CallbackQuery, state: FSMContext) -> None:
    auth_header = await state.get_value("auth_header")
    if not auth_header:
        return

    service = get_service(auth_header)

    domain_id = await state.get_value("domain_id")
    specialization_id = await state.get_value("specialization_id")
    grade_id = await state.get_value("grade_id")

    if domain_id:
        data = StartInterviewRequest(
            domain_id=domain_id,
            specialization_id=specialization_id,
            grade_id=grade_id,
            total_questions=None,
        )
        r = await service.start_interview(data)
        session_id = r.session_id
        await state.update_data(session_id=session_id)

        questions = await service.get_questions(session_id)
        await state.update_data(
            questions_ids=[q.question_id for q in questions]
        )
        await state.update_data(total_questions=len(questions))

        await state.update_data(current_question=1)
        await show_question(cb, state, questions[0])


async def show_question(
    cb: CallbackQuery,
    state: FSMContext,
    q: InterviewQuestion,
) -> None:
    current_question: int = await state.get_value("current_question", None)
    total_questions: int = await state.get_value("total_questions", None)
    await safe_response(
        cb,
        question_text(q, current_question, total_questions),
        question_kb(q, current_question, total_questions),
    )


async def select_option(
    cb: CallbackQuery,
    state: FSMContext,
    option_id: int,
    auth_header: str,
) -> None:
    service = get_service(auth_header)
    session_id = await state.get_value("session_id", default=[])
    questions = await service.get_questions(session_id)
    current_question: Optional[int] = await state.get_value(
        "current_question", None
    )
    total_questions: Optional[int] = await state.get_value(
        "total_questions", None
    )

    if questions and current_question and total_questions:
        q = questions[current_question - 1]
        prev_selection = list(q.selected_option_ids)

        if q.question_type == QuestionType.SINGLE_CHOICE:
            q.selected_option_ids = [option_id]
        else:
            if option_id in q.selected_option_ids:
                q.selected_option_ids.remove(option_id)
            else:
                q.selected_option_ids.append(option_id)

        if prev_selection != q.selected_option_ids:
            await safe_response(
                cb,
                question_text(q, current_question, total_questions),
                question_kb(q, current_question, total_questions),
            )
        else:
            await cb.answer()


async def submit(
    cb: CallbackQuery,
    state: FSMContext,
    auth_header: str,
) -> None:
    service = get_service(auth_header)
    session_id: Optional[int] = await state.get_value("session_id", None)
    if not session_id:
        return
    questions = await service.get_questions(session_id)
    current_question: Optional[int] = await state.get_value(
        "current_question", None
    )
    total_questions: Optional[int] = await state.get_value(
        "total_questions", None
    )

    if session_id and questions and current_question and total_questions:
        q = questions[current_question - 1]
        save_answer_request = SaveAnswerRequest(
            question_id=q.question_id,
            selected_option_ids=q.selected_option_ids,
        )
        await service.save_answer(session_id, save_answer_request)

        await state.update_data(current_question=(current_question + 1))
        if current_question != total_questions:
            await show_question(cb, state, questions[current_question])
        else:
            await show_results(cb, state, auth_header)


async def back(
    cb: CallbackQuery,
    state: FSMContext,
) -> None:
    current_question: Optional[int] = await state.get_value(
        "current_question", None
    )
    questions: Optional[List[InterviewQuestion]] = await state.get_value(
        "questions", None
    )
    if questions and current_question:
        next_question = current_question - 1
        if next_question != 0:
            await state.update_data(current_question=next_question)
            await show_question(cb, state, questions[next_question - 1])


async def show_results(
    cb: CallbackQuery,
    state: FSMContext,
    auth_header: str,
) -> None:
    service = get_service(auth_header)
    session_id: Optional[int] = await state.get_value("session_id", None)
    if not session_id:
        return

    await service.finish(session_id)
    results = await service.get_result(session_id)

    await state.update_data(current_result_question=0)

    await safe_response(
        cb,
        result_text(results),
        results_kb(results),
    )


async def show_results_question(
    cb: CallbackQuery,
    state: FSMContext,
    auth_header: str,
    direction: int = 1,
) -> None:
    service = get_service(auth_header)
    session_id: Optional[int] = await state.get_value("session_id", None)
    if not session_id:
        return

    results = await service.get_result(session_id)

    current: int = await state.get_value("current_result_question", 0)

    if not results:
        await cb.answer()
        return

    total = len(results.questions)
    current += direction

    if not (1 <= current <= total):
        await cb.answer()
        return

    await state.update_data(current_result_question=current)

    q = results.questions[current - 1]
    await safe_response(
        cb,
        result_question_text(q, current, total),
        result_question_kb(current, total),
    )
