from enum import StrEnum


class SkillBlock(StrEnum):
    DESCRIPTION = "description"
    SALARY = "salary"
    STACK = "stack"
    QUESTIONS = "questions"


BLOCK_LABELS: dict[SkillBlock, str] = {
    SkillBlock.DESCRIPTION: "📝 Описание",
    SkillBlock.SALARY: "💵 Зарплата",
    SkillBlock.STACK: "⚙️ Технологии",
    SkillBlock.QUESTIONS: "❓ Вопросы",
}
