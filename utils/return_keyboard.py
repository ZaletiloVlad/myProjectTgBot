from aiogram import types


def return_kb(user_id):
    inline_keyboard = types.InlineKeyboardMarkup(row_width=1)
    inline_keyboard.add(types.InlineKeyboardButton('Вернуться в меню', callback_data=f"return_{user_id}"))
    return inline_keyboard