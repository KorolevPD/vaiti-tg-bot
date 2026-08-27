from aiogram.fsm.state import State, StatesGroup


class CoverLettersState(StatesGroup):
    waiting_for_context = State()
