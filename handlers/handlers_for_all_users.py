from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text


# @dp.callback_query_handler(Text(contains='userspace'))
async def space_menu(callback: types.CallbackQuery):
    user_id = callback.data.split('_')[1]
    space = callback.data.split('_')[2]
    user_grade = callback.data.split('_')[3]
    is_banned = False if callback.data.split('_')[-1] == 'False' else True

    inline_kb = types.InlineKeyboardMarkup(row_width=1)

    if is_banned:

        inline_kb.add(types.InlineKeyboardButton('Выйти из этого SPACE', callback_data=f"delete_space_{user_id}_{space}"))
        inline_kb.add(types.InlineKeyboardButton('Вернуться в меню', callback_data=f"return_{user_id}"))

        await callback.message.edit_text('Вы были забанены. Вы можете выйти из этого SPACE или дождаться, когда '
                                         'Вас разбанит администратоh.', reply_markup=inline_kb)
        await callback.answer()
        return

    inline_kb.add(types.InlineKeyboardButton('Внести расход', callback_data=f"make_spending_{user_id}_{space}"))
    inline_kb.add(types.InlineKeyboardButton('Посмотреть историю расходов',
                                             callback_data=f"look_spending_{user_id}_{space}"))

    if user_grade in ['A', 'M']:
        inline_kb.add(types.InlineKeyboardButton('Добавить категорию расходов',
                                                 callback_data=f"create_category_{user_id}_{space}"))

    inline_kb.add(types.InlineKeyboardButton('Посмотреть доступные категории',
                                             callback_data=f"available_categories_{user_grade}_{user_id}_{space}"))
    inline_kb.add(types.InlineKeyboardButton('Посмотреть всех пользователей',
                                             callback_data=f"show_users_{user_id}_{user_grade}_{space}"))

    if user_grade == 'A':
        inline_kb.add(types.InlineKeyboardButton('Сгенерировать реферальный код',
                                                 callback_data=f"generate_code_{user_id}_{space}"))
        inline_kb.add(types.InlineKeyboardButton('Удалить SPACE', callback_data=f"delete_space_{user_id}_{space}"))


    if user_grade in ['M', 'C']:
        inline_kb.add(types.InlineKeyboardButton('Выйти из этого SPACE',
                                                 callback_data=f"delete_me_from_space_{user_id}_{space}"))

    inline_kb.add(types.InlineKeyboardButton('Вернуться в меню', callback_data=f"return_{user_id}"))

    await callback.message.edit_text('Выберите действие', reply_markup=inline_kb)
    await callback.answer()


def register_all_users_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(space_menu, Text(contains='userspace'))
