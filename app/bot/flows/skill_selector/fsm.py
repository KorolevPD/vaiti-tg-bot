from aiogram.fsm.state import State, StatesGroup


class SkillSelectFSM(StatesGroup):
    specialization = State()
    domain = State()
    grade = State()
