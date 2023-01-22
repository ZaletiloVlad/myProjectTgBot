from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text

from services.botAPI import bot_service
from utils.return_keyboard import return_kb


# @dp.callback_query_handler(Text(contains='delete_space'))
async def delete_space(callback: types.CallbackQuery):
    user_id = callback.data.split('_')[-2]
    space = callback.data.split('_')[-1]

    inline_kb = types.InlineKeyboardMarkup(row_width=1)
    inline_kb.add(types.InlineKeyboardButton('Да', callback_data=f'yes_space_delete_{user_id}_{space}'))
    inline_kb.add(types.InlineKeyboardButton('Нет', callback_data=f"return_{user_id}"))

    await callback.message.edit_text(f"Вы уверены, что хотите удалить этот SPACE?", reply_markup=inline_kb)
    await callback.answer()


# @dp.callback_query_handler(Text(contains='yes_delete_space'))
async def yes_delete_space(callback: types.CallbackQuery):
    user_id = callback.data.split('_')[-2]
    space = callback.data.split('_')[-1]

    space_delete_info = {
        'user_id': user_id,
        'space': space
    }

    delete_space_response = bot_service.delete_space(space_delete_info)

    await callback.message.edit_text(f'Вы удалили "{space}"', reply_markup=return_kb(user_id))
    await callback.answer('SPACE был удален')


# @dp.callback_query_handler(Text(contains='delete_me_from_space'))
async def delete_me_from_space(callback: types.CallbackQuery):
    user_id = callback.data.split('_')[-2]
    space = callback.data.split('_')[-1]

    inline_kb = types.InlineKeyboardMarkup(row_width=1)
    inline_kb.add(types.InlineKeyboardButton('Да', callback_data=f'get_out_space_{user_id}_{space}'))
    inline_kb.add(types.InlineKeyboardButton('Нет', callback_data=f"return_{user_id}"))


    await callback.message.edit_text(f"Вы уверены, что хотите выйти из этого SPACE?", reply_markup=inline_kb)
    await callback.answer()


# @dp.callback_query_handler(Text(contains='get_out_space'))
async def yes_delete_me(callback: types.CallbackQuery):
    user_id = callback.data.split('_')[-2]
    space = callback.data.split('_')[-1]


    delete_me_info = {
        'user_id': user_id,
        'space': space
    }

    delete_me_from_space_response = bot_service.delete_me_from_space(delete_me_info)

    await callback.message.edit_text(f'Вы вышли из "{space}"', reply_markup=return_kb(user_id))
    await callback.answer('Выход из SPACE')


def register_delete_space_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(delete_space, Text(contains='delete_space'))
    dp.register_callback_query_handler(yes_delete_space, Text(contains='yes_space_delete'))
    dp.register_callback_query_handler(delete_me_from_space, Text(contains='delete_me_from_space'))
    dp.register_callback_query_handler(yes_delete_me, Text(contains='get_out_space'))
