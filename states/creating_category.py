from aiogram.dispatcher.filters.state import State, StatesGroup


class CreateCategoryState(StatesGroup):
    title = State()