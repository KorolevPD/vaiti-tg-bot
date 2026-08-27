from enum import StrEnum
from typing import List, Optional, Sequence

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class QuestionType(StrEnum):
    SINGLE_CHOICE = "SINGLE_CHOICE"
    MULTIPLE_CHOICE = "MULTIPLE_CHOICE"


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        validate_by_name=True,
        alias_generator=to_camel,
    )


class StartInterviewRequest(BaseSchema):
    domain_id: int
    specialization_id: Optional[int] = None
    grade_id: Optional[int] = None
    total_questions: Optional[int] = None


class SaveAnswerRequest(BaseSchema):
    question_id: int
    selected_option_ids: Sequence[int]


class StartInterviewResponse(BaseSchema):
    session_id: int


class AnswerOption(BaseSchema):
    id: int
    text: str


class QuestionResult(BaseSchema):
    question_id: int
    question_text: str
    question_type: QuestionType
    options: List[AnswerOption]
    user_answer_option_ids: List[int]
    correct_answer_option_ids: List[int]
    correct: bool


class InterviewQuestion(BaseSchema):
    question_id: int
    text: str
    question_type: QuestionType
    options: List[AnswerOption]
    selected_option_ids: List[int]


class InterviewResult(BaseSchema):
    total_questions: int
    correct_answers: int
    questions: List[QuestionResult]
