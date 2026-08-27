from typing import Dict, List

from pydantic import BaseModel, Field, computed_field


class UsersNotificationRequest(BaseModel):
    """Запрос на отправку уведомления пользователям."""

    user_ids: List[int] = Field(...)
    message: str = Field(...)


class UsersNotificationResponse(BaseModel):
    """Ответ с результатами отправки сообщений."""

    results: Dict[int, str] = Field(
        ..., description="Статус по каждому user_id: 'ok' или текст ошибки"
    )

    @computed_field
    def total(self) -> int:
        return len(self.results)

    @computed_field
    def sent(self) -> int:
        return sum(1 for status in self.results.values() if status == "ok")
