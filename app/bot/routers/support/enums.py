from typing import Dict

from app.services.support.schemas import FeedbackType

FEELBACK_LABLES: Dict[FeedbackType, str] = {
    FeedbackType.BUG: "Баг",
    FeedbackType.REQUEST: "Предложение",
    FeedbackType.QUESTION: "Вопрос",
    FeedbackType.OTHER: "Другое",
}
