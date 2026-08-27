from aiogram.fsm.state import State, StatesGroup


class CompaniesState(StatesGroup):
    waiting_for_query = State()
