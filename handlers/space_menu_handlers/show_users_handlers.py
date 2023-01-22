from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text

from services.botAPI import bot_service
from utils.return_keyboard import return_kb


# @dp.callback_query_handler(Text(contains='show_users'))
async def show_users(callback: types.CallbackQuery):
    space_title = callback.data.split('_')[-1]
    main_user_grade = callback.data.split('_')[-2]
    user_id = callback.data.split('_')[-3]
    space_info = bot_service.get_space_info({'title': space_title})

    user_grade = {
        'A': 'Admin user',
        'C': 'Casual user',
        'M': 'Master user'
    }

    inline_kb = types.InlineKeyboardMarkup(row_width=1)

    if main_user_grade == 'C':
        users = f"Участники {space_info['title']}:\n\n"
        for user in space_info['status']:
            if not user['is_banned']:
                users += f"- {user['user']} | {user_grade[user['grade']]}\n"
            else:
                users += f"- {user['user']} | {user_grade[user['grade']]} | Забаненн\n"

        await callback.message.edit_text(users, reply_markup=return_kb(user_id))

    else:
        for user in space_info['status']:
            if not user['is_banned']:
                inline_kb.add(types.InlineKeyboardButton(f"{user['user']} | {user_grade[user['grade']]}",
                callback_data=f"update_user_{user_id}_{user['is_banned']}_{user['grade']}_{main_user_grade}_"
                              f"{user['user']}_{user['space']}"))
            else:
                inline_kb.add(types.InlineKeyboardButton(f"{user['user']} | {user_grade[user['grade']]} | Забанен",
                callback_data=f"update_user_{user_id}_{user['is_banned']}_{user['grade']}_{main_user_grade}_"
                              f"{user['user']}_{user['space']}"))

        inline_kb.add(types.InlineKeyboardButton('Вернуться в меню', callback_data=f"return_{user_id}"))

        await callback.message.edit_text(f"Участники {space_info['title']}:", reply_markup=inline_kb)

    await callback.answer()



# @dp.callback_query_handler(Text(contains='update_user'))
async def update_user(callback: types.CallbackQuery):
    space_title = callback.data.split('_')[-1]
    change_user = callback.data.split('_')[-2]
    main_user_grade = callback.data.split('_')[-3]
    change_user_grade = callback.data.split('_')[-4]
    change_user_is_banned = False if callback.data.split('_')[-5] == 'False' else True
    user_id = callback.data.split('_')[-6]

    inline_kb = types.InlineKeyboardMarkup(row_width=1)

    if change_user_grade == 'A':
        await callback.message.edit_text(f"Этот пользователь является администратором", reply_markup=return_kb(user_id))
        return

    if not change_user_is_banned:
        inline_kb.add(types.InlineKeyboardButton('Изменить статус пользователя',
                                    callback_data=f"change_{user_id}_{change_user}_{space_title}"))

    if main_user_grade == 'M' and change_user_is_banned == True:
        await callback.message.edit_text(f"Этот пользователь забанен администратором.", reply_markup=return_kb(user_id))
        return

    if main_user_grade == 'A' and change_user_is_banned == False:
        inline_kb.add(types.InlineKeyboardButton('Забанить этого пользователя',
                                    callback_data=f"ban_{user_id}_{change_user}_{change_user_is_banned}_{space_title}"))
    elif main_user_grade == 'A' and change_user_is_banned == True:
        inline_kb.add(types.InlineKeyboardButton('Разабанить этого пользователя',
                                    callback_data=f"ban_{user_id}_{change_user}_{change_user_is_banned}_{space_title}"))
    inline_kb.add(types.InlineKeyboardButton('Вернуться в меню', callback_data=f"return_{user_id}"))

    await callback.message.edit_text(f"Выберите действие:", reply_markup=inline_kb)
    await callback.answer()


# @dp.callback_query_handler(Text(contains='change'))
async def change_user(callback: types.CallbackQuery):
    user_grade = {
        'C': 'Casual user',
        'M': 'Master user'
    }

    change_user_info = {
        'user_id': callback.data.split('_')[-3],
        'change_user': callback.data.split('_')[-2],
        'space_title': callback.data.split('_')[-1]
    }

    change_user_response = bot_service.update_user(change_user_info)

    if len(change_user_response) == 1:
        await callback.message.edit_text('Вы не можете изменить собственный статус',
                                         reply_markup=return_kb(callback.data.split('_')[-3]))
    else:
        await callback.message.edit_text(f"Статус пользователя {change_user_response['user']} изменен на "
                                        f"{user_grade[change_user_response['grade']]}",
                                        reply_markup=return_kb(callback.data.split('_')[-3]))
    await callback.answer()


# @dp.callback_query_handler(Text(contains='ban'))
async def ban_user(callback: types.CallbackQuery):

    is_banned = False if callback.data.split('_')[-2] == 'False' else True

    ban_user_info = {
        'user_id': callback.data.split('_')[-4],
        'ban_user': callback.data.split('_')[-3],
        'is_banned': is_banned,
        'space_title': callback.data.split('_')[-1]
    }

    ban_user_response = bot_service.ban_user(ban_user_info)

    if is_banned:
        await callback.message.edit_text(f"Вы разабанили пользователя {ban_user_response['user']}",
                                         reply_markup=return_kb(callback.data.split('_')[-4]))
    else:
        await callback.message.edit_text(f"Вы забанили пользователя {ban_user_response['user']}",
                                         reply_markup=return_kb(callback.data.split('_')[-4]))
    await callback.answer()


def register_show_users_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(show_users, Text(contains='show_users'))
    dp.register_callback_query_handler(update_user, Text(contains='update_user'))
    dp.register_callback_query_handler(change_user, Text(contains='change'))
    dp.register_callback_query_handler(ban_user, Text(contains='ban'))
