from html import escape
from typing import List

from app.bot.utils import a, b, quote
from app.services.knowledge.schemas import (
    DomainMatrixResponse,
    Skill,
    TypicalQuestion,
)

BOT_COMMAND = "skills"
BOT_COMMAND_DESCRIPTION = "Каталог навыков"

SKILLS_CATALOG_TITLE = "📖 Каталог навыков"


async def description_text(
    domain_matrix: DomainMatrixResponse, grade_id: int
) -> str:
    parts: List[str] = []
    for category in domain_matrix.skill_categories:
        lines = [f"<b>{category.category_name}</b>"]

        for skill in category.skills:
            if skill.criteria:
                criteria = skill.criteria.get(str(grade_id))
                if criteria:
                    lines.append(f" • {skill.name}: {criteria}")

        if len(lines) > 1:
            parts.append("\n".join(lines))

    return "\n\n".join(parts)


async def salary_text(
    domain_matrix: DomainMatrixResponse, grade_id: int
) -> str:
    return "💵 <b>Зарплата</b>\n\nИнформация пока недоступна."


async def stack_text(tools: List[Skill]) -> str:
    parts: List[str] = []

    for tool in tools:
        tool_parts: List[str] = []

        # Название
        tool_parts.append(a(b(escape(tool.name)), tool.documentation_url))

        # Описание
        if tool.description:
            tool_parts.append(escape(tool.description))

        # Области применения
        if tool.metadata and tool.metadata.application_areas:
            areas = "\n".join(
                f"• {escape(area)}"
                for area in tool.metadata.application_areas
            )
            tool_parts.append(f"\n{b('Применение:')}\n{areas}")

        tool_text = "\n".join(tool_parts)
        tool_quote = quote(tool_text, expandable=True)
        parts.append(f"{tool_quote}\n")

    return "".join(parts)


async def questions_text(questions: List[TypicalQuestion]) -> str:
    parts: List[str] = []
    for q in questions[:5]:
        question_quote = quote(
            f"{b('Ответ:')}\n{escape(q.answer)}\n"
            f"{b('Пояснение:')}\n{escape(q.explanation)}",
            expandable=True,
        )
        parts.append(f"{b(escape(q.question))}\n{question_quote}\n")
    return "\n".join(parts)
