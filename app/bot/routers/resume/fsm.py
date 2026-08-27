from aiogram.fsm.state import State, StatesGroup


class ResumeState(StatesGroup):
    waiting_for_pdf = State()
