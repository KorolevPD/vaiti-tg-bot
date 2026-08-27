from typing import List

from app.clients import APIClient

from .protocol import TrainerServiceProtocol
from .schemas import (
    InterviewQuestion,
    InterviewResult,
    SaveAnswerRequest,
    StartInterviewRequest,
    StartInterviewResponse,
)


class TrainerService(APIClient, TrainerServiceProtocol):
    async def start_interview(
        self, data: StartInterviewRequest
    ) -> StartInterviewResponse:
        r = await self._client.post(
            "/api/v1/interview/start",
            headers=self.headers,
            json=data.model_dump(by_alias=True, exclude_none=True),
        )
        r.raise_for_status()
        return StartInterviewResponse.model_validate(r.json())

    async def get_questions(self, session_id: int) -> List[InterviewQuestion]:
        r = await self._client.get(
            f"/api/v1/interview/{session_id}/questions",
            headers=self.headers,
        )
        r.raise_for_status()
        return [InterviewQuestion(**item) for item in r.json()]

    async def save_answer(
        self, session_id: int, data: SaveAnswerRequest
    ) -> None:
        r = await self._client.post(
            f"/api/v1/interview/{session_id}/answers",
            json=data.model_dump(by_alias=True),
            headers=self.headers,
        )
        r.raise_for_status()

    async def finish(self, session_id: int) -> None:
        r = await self._client.post(
            f"/api/v1/interview/{session_id}/finish",
            headers=self.headers,
        )
        r.raise_for_status()

    async def get_result(self, session_id: int) -> InterviewResult:
        r = await self._client.get(
            f"/api/v1/interview/{session_id}/result",
            headers=self.headers,
        )
        r.raise_for_status()
        return InterviewResult.model_validate(r.json())
