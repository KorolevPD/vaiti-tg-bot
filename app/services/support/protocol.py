from typing import Protocol

from .schemas import FeedbackRequest


class SupportServiceProtocol(Protocol):
    async def send_feedback(self, data: FeedbackRequest) -> bool: ...
