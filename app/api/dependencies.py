from aiogram import Bot
from fastapi import Request


def get_bot(request: Request) -> Bot:
    bot: Bot = request.app.state.bot
    return bot
