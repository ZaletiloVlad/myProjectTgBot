from aiogram.dispatcher.filters.state import State, StatesGroup


class JoinSpaceState(StatesGroup):
    code = State()