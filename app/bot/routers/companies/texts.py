from app.bot.utils import a, b
from app.core.config import settings
from app.services.companies.schemas import CompanyResponse

BOT_COMMAND = "companies"
BOT_COMMAND_DESCRIPTION = "Каталог компаний"

COMPANIES_TITLE = "🏢 Каталог компаний"


def _format_float(f: float) -> str:
    return f"{round(f, 1):.1f}".rstrip("0").rstrip(".")


def not_found_text(query: str | None) -> str:
    query = " " + b(query) + " " if query else " "
    return (
        f"По запросу{query}ничего не найдено.\n\n"
        "Попробуйте изменить поисковый запрос."
    )


def result_text(query: str | None, page: int, total_pages: int) -> str:
    header = f"Результаты по запросу{': ' + b(query) if query else ''}"
    pages = (
        f"\n\nСтраница {page + 1} из {total_pages}:"
        if page + 1 != total_pages
        else ""
    )
    return f"{header}{pages}"


def company_text(company: CompanyResponse) -> str:
    lines = []
    reviews_link = f"https://{settings.WEBHOOK_DOMAIN}/{company.slug}/reviews/"

    header = f"{a(b(company.name), company.website_url)}"
    lines.append(header)

    rating = (
        f"⭐ {b('Рейтинг:')} {_format_float(company.rating)}/10"
        if company.rating or company.review_count
        else ""
    )
    review_count = (
        f"({a(str(company.review_count), reviews_link)})"
        if company.review_count
        else ""
    )
    rating_line = "\n".join(ln for ln in [rating, review_count] if ln)

    complexity = (
        f"⚙️ {b('Сложность проектов: ')}"
        f"{_format_float(company.complexity_rating)}/10"
        if company.complexity_rating
        else ""
    )
    lines.append("\n".join(ln for ln in [rating_line, complexity] if ln))

    description = (
        f"📝 {b('Описание:')}\n{company.description}"
        if company.description
        else ""
    )
    lines.append(description)

    return "\n\n".join(ln for ln in lines if ln)
