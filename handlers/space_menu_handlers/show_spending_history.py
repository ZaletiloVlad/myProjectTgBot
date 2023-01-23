from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text

from services.botAPI import bot_service
from utils.return_keyboard import return_kb


# @dp.callback_query_handler(Text(contains='look_spending'))
async def look_spending(callback: types.CallbackQuery):
    space = callback.data.split('_')[-1]
    user_id = callback.data.split('_')[-2]

    inline_kb = types.InlineKeyboardMarkup(row_width=1)
    inline_kb.add(types.InlineKeyboardButton('Посмотреть историю моих расходов',
                                             callback_data=f"show_history_my_{user_id}_{space}"))
    inline_kb.add(types.InlineKeyboardButton('Посмотреть общую историю расходов для этого SPACE',
                                             callback_data=f"show_history_whole_{user_id}_{space}"))
    inline_kb.add(types.InlineKeyboardButton('Вернуться в меню', callback_data=f"return_{user_id}"))

    await callback.message.edit_text('Выберите действие:', reply_markup=inline_kb)
    await callback.answer()

# @dp.callback_query_handler(Text(contains='show_history'))
async def show_history(callback: types.CallbackQuery):
    space = callback.data.split('_')[-1]
    user_id = callback.data.split('_')[-2]
    callback_part = callback.data.split('_')[-3]


    inline_kb = types.InlineKeyboardMarkup(row_width=1)
    inline_kb.add(types.InlineKeyboardButton('За день',
                                             callback_data=f"day_spending_{callback_part}_{user_id}_{space}"))
    inline_kb.add(types.InlineKeyboardButton('За неделю',
                                             callback_data=f"week_spending_{callback_part}_{user_id}_{space}"))
    inline_kb.add(types.InlineKeyboardButton('За месяц',
                                             callback_data=f"month_spending_{callback_part}_{user_id}_{space}"))
    inline_kb.add(types.InlineKeyboardButton('За квартал',
                                             callback_data=f"threemonths_spending_{callback_part}_{user_id}_{space}"))
    inline_kb.add(types.InlineKeyboardButton('За полгода',
                                             callback_data=f"sixmonths_spending_{callback_part}_{user_id}_{space}"))
    inline_kb.add(types.InlineKeyboardButton('За год',
                                             callback_data=f"year_spending_{callback_part}_{user_id}_{space}"))
    inline_kb.add(types.InlineKeyboardButton('Вернуться в меню', callback_data=f"return_{user_id}"))

    await callback.message.edit_text('Выберите, за какое время Вы хотите увидеть свои расходы', reply_markup=inline_kb)
    await callback.answer()

# @dp.callback_query_handler(Text(contains='spending_my'))
async def show_my_spending(callback: types.CallbackQuery):
    space = callback.data.split('_')[-1]
    user_id = callback.data.split('_')[-2]

    expenses_info = {
        'user': user_id,
        'space': space,
        'time': callback.data.split('_')[0]
    }

    expenses_response = bot_service.get_expenses_history(expenses_info)
    print(expenses_response)
    if not expenses_response:
        await callback.message.edit_text(f'У Вас нет расходов за выбранный промежуток времени',
                                         reply_markup=return_kb(user_id))
        await callback.answer()
        return

    expenses_data = {}

    for expense in expenses_response:
        expenses_data[expense['category']] = float(expenses_data.get(expense['category'], 0)) + float(expense['expense'])

    response = ''
    currency = expenses_response[0]['currency']
    total = 0

    for key, value in expenses_data.items():
        response += f"- {key}: {round(value, 2)} {currency}\n\n"
        total += value

    response += f"Всего: {round(total, 2)} {currency}"

    await callback.message.edit_text(f'Ваши расходы за выбранный промежуток времени:\n\n {response}',
                                     reply_markup=return_kb(user_id))
    await callback.answer()


# @dp.callback_query_handler(Text(contains='spending_whole'))
async def show_whole_spending(callback: types.CallbackQuery):
    space = callback.data.split('_')[-1]
    user_id = callback.data.split('_')[-2]

    expenses_info = {
        'space': space,
        'time': callback.data.split('_')[0]
    }

    expenses_response = bot_service.get_expenses_history(expenses_info)
    print(expenses_response)

    if not expenses_response:
        await callback.message.edit_text(f'За выбранный промежуток времени расходы отсутствуют',
                                         reply_markup=return_kb(user_id))
        await callback.answer()
        return

    expenses_data = {}

    for expense in expenses_response:
        expenses_data[expense['category']] = float(expenses_data.get(expense['category'], 0)) + float(expense['expense'])
    print(expenses_data)
    response = ''
    currency = expenses_response[0]['currency']
    total = 0

    for key, value in expenses_data.items():
        response += f"- {key}: {round(value, 2)} {currency}\n\n"
        total += value

    response += f"Всего: {round(total, 2)} {currency}"

    await callback.message.edit_text(f'Расходы за выбранный промежуток времени:\n\n {response}',
                                     reply_markup=return_kb(user_id))
    await callback.answer()

def register_show_users_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(look_spending, Text(contains='look_spending'))
    dp.register_callback_query_handler(show_history, Text(contains='show_history'))
    dp.register_callback_query_handler(show_my_spending, Text(contains='spending_my'))
    dp.register_callback_query_handler(show_whole_spending, Text(contains='spending_whole'))