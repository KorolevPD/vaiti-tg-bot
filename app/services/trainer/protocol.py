from typing import List, Protocol

from .schemas import (
    InterviewQuestion,
    InterviewResult,
    SaveAnswerRequest,
    StartInterviewRequest,
    StartInterviewResponse,
)


class TrainerServiceProtocol(Protocol):
    async def start_interview(
        self, data: StartInterviewRequest
    ) -> StartInterviewResponse: ...

    async def get_questions(
        self, session_id: int
    ) -> List[InterviewQuestion]: ...

    async def save_answer(
        self, session_id: int, data: SaveAnswerRequest
    ) -> None: ...

    async def finish(self, session_id: int) -> None: ...
    async def get_result(self, session_id: int) -> InterviewResult: ...
