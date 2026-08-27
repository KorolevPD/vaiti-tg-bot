from typing import Optional

BOT_COMMAND = "menu"
BOT_COMMAND_DESCRIPTION = "Главное меню"

BACK_TO_MENU_TITLE = "« Главное меню"
MENU_START_TEXT = "Выбери нужный раздел:"


def greetings_text(name: Optional[str]) -> str:
    return (
        f"Привет{', ' + name if name else ''}! Я — карьерный ассистент Вайти. "
        "Помогаю автоматизировать отклики, присылать свежие вакансии и "
        "разбираться в компаниях."
    )
