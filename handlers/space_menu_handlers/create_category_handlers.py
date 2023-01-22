from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from services.botAPI import bot_service
from states.creating_category import CreateCategoryState
from utils.return_keyboard import return_kb


# @dp.callback_query_handler(Text(contains='create_category'))
async def create_category(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.data.split('_')[-2]
    space = callback.data.split('_')[-1]

    await state.set_state(CreateCategoryState.title.state)

    async with state.proxy() as data:
        data['id'] = user_id
        data['space'] = space

    inline_kb = types.InlineKeyboardMarkup(row_width=1)
    inline_kb.add(types.InlineKeyboardButton('Вернуться в меню', callback_data=f"return_{user_id}"))

    await callback.message.edit_text('Введите название категории\n* не более 30 символов\n** в названии не может быть '
                                     'использован символ "_"')
    await callback.answer()

# @dp.message_handler(state=CreateCategoryState.title)
async def add_category_title(msg: types.Message, state: FSMContext):

    if msg.text.startswith('/'):
        await msg.reply('Название не может начинаться с  "/"\nВведите новое название')
        return

    elif '_' not in msg.text:
        async with state.proxy() as data:
            data['title'] = msg.text

    else:
        await msg.reply('Недопустимый символ "_"\nВведите новое название')
        return

    new_category_data = await state.get_data()

    category = bot_service.create_category(new_category_data)
    user_id = new_category_data['id']

    if len(category) == 1:
        await msg.reply(f"У вас уже есть категория с таким названием. Пожалуйста, введите новое название")
    else:
        await state.finish()
        await msg.answer(f"Добавлена новая категория: {category['title']}", reply_markup=return_kb(user_id))


def register_create_category_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(create_category, Text(contains='create_category'))
    dp.register_message_handler(add_category_title, state=CreateCategoryState.title)