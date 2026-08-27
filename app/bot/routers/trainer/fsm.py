from aiogram.fsm.state import State, StatesGroup


class TrainerFSM(StatesGroup):
    question = State()
    review = State()
