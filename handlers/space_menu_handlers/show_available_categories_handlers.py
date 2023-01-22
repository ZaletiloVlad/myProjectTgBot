from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text

from services.botAPI import bot_service
from utils.return_keyboard import return_kb


# @dp.callback_query_handler(Text(contains='available_categories'))
async def show_categories(callback: types.CallbackQuery):
    user_id = callback.data.split('_')[-2]
    user_grade = callback.data.split('_')[-3]
    space = callback.data.split('_')[-1]

    categories_info = {
        'space_title': space
    }

    categories_response = bot_service.get_categories(categories_info)

    if user_grade == 'A':

        inline_kb = types.InlineKeyboardMarkup(row_width=1)

        for category in categories_response:
            inline_kb.add(types.InlineKeyboardButton(category['title'],
                                                     callback_data=f"delete_category_{user_id}_{category['title']}_{space}"))

        inline_kb.add(types.InlineKeyboardButton('Вернуться в меню', callback_data=f"return_{user_id}"))
        await callback.message.edit_text(f"Для этого SPACE доступны категории:\n\n", reply_markup=inline_kb)

    else:

        categories = ""

        for category in categories_response:
            categories += f"- {category['title']}\n"

        await callback.message.edit_text(f"Для этого SPACE доступны категории:\n\n{categories}",
                                         reply_markup=return_kb(user_id))

    await callback.answer()


# @dp.callback_query_handler(Text(contains='delete_category'))
async def delete_category(callback: types.CallbackQuery):
    user_id = callback.data.split('_')[-3]
    space = callback.data.split('_')[-1]
    category = callback.data.split('_')[-2]

    inline_kb = types.InlineKeyboardMarkup(row_width=1)
    inline_kb.add(types.InlineKeyboardButton('Удалить эту категорию', callback_data=f'maybe_off_this_category_{user_id}_'
                                                                                    f'{category}_{space}'))
    inline_kb.add(types.InlineKeyboardButton('Вернуться в меню', callback_data=f"return_{user_id}"))

    await callback.message.edit_text(f"Выберите действие:", reply_markup=inline_kb)
    await callback.answer()

# @dp.callback_query_handler(Text(contains='maybe_off_this_category'))
async def maybe_off_this_category(callback: types.CallbackQuery):
    user_id = callback.data.split('_')[-3]
    space = callback.data.split('_')[-1]
    category = callback.data.split('_')[-2]

    inline_kb = types.InlineKeyboardMarkup(row_width=1)
    inline_kb.add(types.InlineKeyboardButton('Да', callback_data=f'off_category_{user_id}_{category}_{space}'))
    inline_kb.add(types.InlineKeyboardButton('Нет', callback_data=f"return_{user_id}"))

    await callback.message.edit_text(f"Вы уверены, что хотите удалить эту категорию?", reply_markup=inline_kb)
    await callback.answer()


# @dp.callback_query_handler(Text(contains='off_category'))
async def yes_delete_category(callback: types.CallbackQuery):
    user_id = callback.data.split('_')[-3]
    category = callback.data.split('_')[-2]
    space = callback.data.split('_')[-1]

    delete_category_info = {
        'user_id': user_id,
        'category': category,
        'space': space
    }

    delete_category_response = bot_service.delete_category(delete_category_info)

    await callback.message.edit_text(f'Вы удалили категорию "{category}"', reply_markup=return_kb(user_id))
    await callback.answer('Категория удалена')


def register_show_categories_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(show_categories, Text(contains='available_categories'))
    dp.register_callback_query_handler(delete_category, Text(contains='delete_category'))
    dp.register_callback_query_handler(maybe_off_this_category, Text(contains='maybe_off_this_category'))
    dp.register_callback_query_handler(yes_delete_category, Text(contains='off_category'))