from app.bot.utils import b
from app.core.config import settings

SUPPORT_TITLE = "🛟 Сообщить об ошибке"

SUPPORT_TEXT = (
    f"{b(SUPPORT_TITLE)}\n\n"
    "Если у вас возникли вопросы или проблемы — смело пишите сюда 👉 "
    f"@{settings.BOT_SUPPORT_USERNAME}"
)

CHOOSE_FEEDBACK_TYPE_TEXT = "Выбери тип обращения:"

SUCCESS_FEEDBACK_TEXT = (
    "Спасибо за ваше обращение!\n\nМы уже работаем над исправлением ситуации, "
    "как только всё исправим, мы с вами обязательно свяжемся."
)
FAILURE_FEEDBACK_TEXT = (
    "Не удалось обработать ваше обращение из-за проблем с нашим сервером, "
    "попробуйте повторить запрос позже."
)
