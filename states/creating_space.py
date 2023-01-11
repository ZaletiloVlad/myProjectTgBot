from aiogram.dispatcher.filters.state import State, StatesGroup


class CreateSpaceState(StatesGroup):
    title = State()
    currency = State()