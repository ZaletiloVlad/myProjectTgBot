from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from services.botAPI import bot_service
from states.make_spendings import MakeSpendingState
from utils.return_keyboard import return_kb

# @dp.callback_query_handler(Text(contains='make_spending'))
async def make_spending(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.data.split('_')[-2]
    space = callback.data.split('_')[-1]

    await state.set_state(MakeSpendingState.category.state)

    async with state.proxy() as data:
        data['user'] = user_id
        data['space'] = space

    spending_categories_response = bot_service.get_categories({'space_title': space})

    if not spending_categories_response:
        await callback.message.edit_text('Для этого SPACE пока что не создано ни одной категории расходов. Пожалуйста, '
                                         'создайте категорию, для внесения расхода', reply_markup=return_kb(user_id))
        await state.finish()
        await callback.answer()
        return

    inline_kb = types.InlineKeyboardMarkup(row_width=1)

    for category in spending_categories_response:
        inline_kb.add(types.InlineKeyboardButton(f"{category['title']}",
                                                 callback_data=f"load_category_{category['title']}"))

    inline_kb.add(types.InlineKeyboardButton('Вернуться в меню', callback_data=f"return_{user_id}"))

    await callback.message.edit_text('Выберите категорию для внесения расходов:', reply_markup=inline_kb)
    await callback.answer()



# @dp.callback_query_handler(Text(contains='load_category'), state=MakeSpendingState.category)
async def load_spending_category(callback: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    user_id = state_data['user']

    async with state.proxy() as data:
        data['category'] = callback.data.split('_')[-1]

    inline_kb = types.InlineKeyboardMarkup(row_width=1)
    inline_kb.add(types.InlineKeyboardButton('BYN', callback_data=f'spend_currency_BYN'))
    inline_kb.add(types.InlineKeyboardButton('USD', callback_data=f'spend_currency_USD'))
    inline_kb.add(types.InlineKeyboardButton('EUR', callback_data=f'spend_currency_EUR'))
    inline_kb.add(types.InlineKeyboardButton('Вернуться в меню', callback_data=f"return_{user_id}"))

    await MakeSpendingState.next()

    await callback.message.edit_text('Выберите валюту', reply_markup=inline_kb)
    await callback.answer()



# @dp.callback_query_handler(Text(contains='spend_currency'), state=MakeSpendingState.currency)
async def load_spending_currency(callback: types.CallbackQuery, state: FSMContext):

    async with state.proxy() as data:
        data['currency'] = callback.data.split('_')[-1]

    await MakeSpendingState.next()

    await callback.message.edit_text('Введите потраченную сумму денег')
    await callback.answer()


# @dp.message_handler(state=MakeSpendingState.amount_of_money)
async def exchange_rate_spending(msg: types.Message, state=FSMContext):

    state_data = await state.get_data()
    user_id = state_data['user']

    if msg.text.isdigit():
        async with state.proxy() as data:
            data['expense'] = float(msg.text)
    else:
        await msg.answer('Расход должен быть числом!\nПожалуйста, попробуйте еще раз', reply_markup=return_kb(user_id))
        return

    spending_data = await state.get_data()

    spending_response = bot_service.create_spending(spending_data)

    await state.finish()

    if spending_response['currency'] == spending_data['currency']:
        await msg.answer(f"В категорию {spending_data['category']} был внесен расход, равный "
                        f"{spending_response['expense']} {spending_response['currency']}",
                        reply_markup=return_kb(user_id))

    else:
        await msg.answer(f"В категорию {spending_data['category']} был внесен расход, равный "
                        f"{spending_response['expense']} {spending_response['currency']} "
                        f"({spending_data['expense']} {spending_data['currency']})", reply_markup=return_kb(user_id))


def register_make_spending_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(make_spending, Text(contains='make_spending'))
    dp.register_callback_query_handler(load_spending_category, Text(contains='load_category'),
                                       state=MakeSpendingState.category)
    dp.register_callback_query_handler(load_spending_currency, Text(contains='spend_currency'),
                                       state=MakeSpendingState.currency)
    dp.register_message_handler(exchange_rate_spending, state=MakeSpendingState.amount_of_money)