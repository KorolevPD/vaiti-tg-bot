from typing import Awaitable, Callable

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

FinishHandler = Callable[[CallbackQuery, FSMContext], Awaitable[None]]

FINISH_HANDLERS: dict[str, FinishHandler] = {}
