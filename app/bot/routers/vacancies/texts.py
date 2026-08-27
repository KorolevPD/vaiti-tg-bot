from app.bot.utils import a, b
from app.services.vacancies.schemas import VacancyResponse

BOT_COMMAND = "vacancies"
BOT_COMMAND_DESCRIPTION = "Поисковик вакансий"

VACANCIES_TITLE = "💼 Поисковик вакансий"


def vacancy_text(v: VacancyResponse) -> str:
    lines = []

    header = f"{a(b(v.position_title), v.source_url)}"
    lines.append(header)

    work_format = (
        f"💻 {b('Формат работы:')} {v.work_format}" if v.work_format else ""
    )

    employment_type = (
        f"💼 {b('Тип устройства:')} {v.employment_type}"
        if v.employment_type
        else ""
    )

    salary = f"💼 {b('Зарплата:')} {v.salary_text}" if v.salary_text else ""
    lines.append(
        "\n".join(ln for ln in [work_format, employment_type, salary] if ln)
    )

    description = f"📝 {b('Описание:')}\n{v.raw_text}" if v.raw_text else ""
    lines.append(description)

    return "\n\n".join(ln for ln in lines if ln)
