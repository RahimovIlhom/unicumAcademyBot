from aiogram.fsm.state import StatesGroup, State


class Registration(StatesGroup):
    name = State()
    contact = State()
    phone = State()
    preferred_time_slot = State()
