from datetime import datetime as dt
from typing import Any, Dict

from app.bot.utils import b

BOT_COMMAND = "statistic"
BOT_COMMAND_DESCRIPTION = "Статистика откликов"

STATISTIC_TITLE = "📊 Статистика откликов"


def statistic_text(stats: Dict[Any, Any], s_date: float, e_date: float) -> str:
    s_text = dt.fromtimestamp(s_date).strftime("%d.%m.%Y")
    e_text = dt.fromtimestamp(e_date).strftime("%d.%m.%Y")
    period_text = f"{b(s_text)} — {b(e_text)}"

    if not stats:
        return f"Статистика за {period_text} отсутствует."

    stats_text = [f"{key}: {value}" for key, value in stats]

    return f"Статистика за {period_text}:\n\n" "\n".join(stats_text)
