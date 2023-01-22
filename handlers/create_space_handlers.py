from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from services.botAPI import bot_service
from states.creating_space import CreateSpaceState
from utils.return_keyboard import return_kb


# @dp.callback_query_handler(Text(contains='create_space'))
async def create_space(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.data.split('_')[-1]

    await state.set_state(CreateSpaceState.title.state)

    async with state.proxy() as data:
        data['id'] = user_id

    await callback.message.edit_text('Введите название SPACE\n* не более 50 символов\n** в названии не может быть '
                                  'использован символ "_"')
    await callback.answer()



# @dp.message_handler(state=CreateSpaceState.title)
async def load_title(msg: types.Message, state: FSMContext):

    if msg.text.startswith('/'):
        await msg.reply('Название не может начинаться с  "/"\nВведите новое название')
        return

    elif '_' not in msg.text:
        async with state.proxy() as data:
            data['title'] = msg.text

    else:
        await msg.reply('Недопустимый символ "_"\nВведите новое название')
        return

    inline_kb = types.InlineKeyboardMarkup(row_width=1)
    inline_kb.add(types.InlineKeyboardButton('BYN', callback_data='main_currency_BYN'))
    inline_kb.add(types.InlineKeyboardButton('USD', callback_data='main_currency_USD'))
    inline_kb.add(types.InlineKeyboardButton('EUR', callback_data='main_currency_EUR'))
    inline_kb.add(types.InlineKeyboardButton('Вернуться в меню', callback_data=f"return_{data['id']}"))

    await CreateSpaceState.next()
    await msg.answer('Выберите основную валюту\nВ эту валюту в дальнейшем будут конвертироваться все Ваши расходы',
                    reply_markup=inline_kb)


#@dp.callback_query_handler(Text(contains='main_currency'), state=CreateSpaceState.currency)
async def load_main_currency(callback: types.CallbackQuery, state: FSMContext):

    currency = callback.data.split('_')[-1]

    async with state.proxy() as data:
        data['currency'] = currency

    new_state_data = await state.get_data()
    user_id = new_state_data['id']


    space = bot_service.create_space(new_state_data)
    await state.finish()
    await callback.message.edit_text(f"Создан новый SPACE\n"
                                 f"Название: {space['title']}\n"
                                 f"Основная валюта: {space['currency']}", reply_markup=return_kb(user_id))

    await callback.answer('Создан новый SPACE')


def register_create_space_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(create_space, Text(contains='create_space'))
    dp.register_message_handler(load_title, state=CreateSpaceState.title)
    dp.register_callback_query_handler(load_main_currency, Text(contains='main_currency'), state=CreateSpaceState.currency)
