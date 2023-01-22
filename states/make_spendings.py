from aiogram.dispatcher.filters.state import State, StatesGroup


class MakeSpendingState(StatesGroup):
    category = State()
    currency = State()
    amount_of_money = State()