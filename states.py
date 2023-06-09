from aiogram.dispatcher.filters.state import State, StatesGroup

class FSM(StatesGroup):
    city = State()
    when = State()
    price = State()
