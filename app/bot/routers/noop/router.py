from aiogram import F, Router
from aiogram.types import CallbackQuery

router = Router()


@router.callback_query(F.data == "noop")
async def noop_callback(cb: CallbackQuery) -> None:
    await cb.answer()
