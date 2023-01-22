from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.utils import executor
from handlers import handlers_for_all_users, create_space_handlers
from handlers.space_menu_handlers import show_users_handlers, create_category_handlers, generate_referral_code, \
    show_available_categories_handlers, delete_space_handlers, make_spending_handlers, show_spending_history

from services.botAPI import bot_service
from states.join_space import JoinSpaceState
from utils.return_keyboard import return_kb

storage = MemoryStorage()

BOT_TOKEN = '5960706975:AAGec02BckR7g3ZE5Gl5VCnRUit7LQdeZKw'

bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot, storage=storage)


async def startup(_):
    bot_service.check_availability()

@dp.message_handler(commands=['отмена'], state='*')
@dp.message_handler(Text(equals='отмена', ignore_case=True), state='*')
async def cancel_cmd(msg: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await msg.answer('Произведена отмена')

@dp.message_handler(commands=['help'])
async def help_cmd(msg: types.Message):
    await msg.answer("""Добро пожаловать в @familyFinancial_bot!\n
Это бот для контроля за расходами при помощи SPACE'ов, которые вы можете создавать.
При содании SPACE Вы автоматически становитесь его администратом. К Вашему SPACE могут присоединиться другие пользователи, для этого администратор должен сгенерировать реферальный код и передать его пользователю, которого он хочет пригласить.
Присоединившийся пользователь автоматически получает статус "Casual user", но администратор может расширить его права посредством присвоения статуса "Master user".\n
Если что-то пойдет не так, Вы можеете написать в чат "отмена" или "/отмена" и сразу после этого ввести команду "/start" """)

@dp.message_handler(commands=['start'])
async def start_cmd(msg: types.Message):
    user_info = {
        'name': msg.from_user.first_name,
        'telegram_id': msg.from_user.id,
    }

    if msg.from_user.last_name:
        user_info['name'] += f" {msg.from_user.last_name}"

    # if msg.from_user.username:
    #     user_info['name'] += f" | @{msg.from_user.username}"

    user = bot_service.get_user_id(user_info)

    ikb = types.InlineKeyboardMarkup(row_width=1)
    ikb.add(types.InlineKeyboardButton("Начать работу со SPACE'ами", callback_data=f"menu_{user['id']}"))

    await msg.answer(f"Здравствуйте, {user['name']}", reply_markup=ikb)


@dp.callback_query_handler(Text(contains='menu'))
async def menu_cmd(callback: types.CallbackQuery):
    user_id = callback.data.split('_')[-1]
    inline_kb = types.InlineKeyboardMarkup(row_width=1)
    user_spaces_response = bot_service.get_user_spaces(user_id)

    user_grade = {
        'A': 'Admin user',
        'C': 'Casual user',
        'M': 'Master user'
    }

    for space in user_spaces_response['user_space']:
        inline_kb.add(
            types.InlineKeyboardButton(f"{space['space']} | {user_grade[space['grade']]}",
                                       callback_data=f"userspace_{user_id}_{space['space']}_"
                                                     f"{space['grade']}_{space['is_banned']}")
        )

    inline_kb.add(types.InlineKeyboardButton('Создать новый SPACE', callback_data=f"create_space_{user_id}"))
    inline_kb.add(types.InlineKeyboardButton('Присоединиться к SPACE', callback_data=f"join_space_{user_id}"))
    await callback.message.edit_text('Выберите SPACE, с которым хотите начать работу', reply_markup=inline_kb)
    await callback.answer()


@dp.callback_query_handler(Text(contains="return"), state="*")
async def return_cmd(callback: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await menu_cmd(callback)
    await callback.answer("Возврат в меню")


@dp.callback_query_handler(Text(contains='join_space'))
async def join_to_space(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.data.split('_')[-1]

    await state.set_state(JoinSpaceState.code.state)

    async with state.proxy() as data:
         data['user'] = user_id

    await callback.message.edit_text('Введите реферальный код для подключения к SPACE')
    await callback.answer()


@dp.message_handler(state=JoinSpaceState.code)
async def add_category_title(msg: types.Message, state: FSMContext):

    async with state.proxy() as data:
        data['code'] = msg.text

    join_space_data = await state.get_data()

    user_id = join_space_data['user']

    join_space_response = bot_service.join_space(join_space_data)
#
    if len(join_space_response) == 1:
        if join_space_response['text'] =='Invalid code':
            await msg.reply(f"Срок действия этого реферального кода истек.\nАдминистратору необходимо " 
                            f"сгенерировать новый код подключения!", reply_markup=return_kb(user_id))
            await state.finish()
        else:
            await msg.reply(f"Такого реферального кода не существует. Попробуйте еще раз", reply_markup=return_kb(user_id))
            await state.finish()

    elif len(join_space_response) == 2:
            await msg.reply(f'Вы уже находитесь в "{join_space_response["space"]}"', reply_markup=return_kb(user_id))
            await state.finish()
    else:
        await msg.reply(f'Вы присоединились к "{join_space_response["space"]}"', reply_markup=return_kb(user_id))
        await state.finish()

create_space_handlers.register_create_space_handlers(dp)
handlers_for_all_users.register_all_users_handlers(dp)
show_available_categories_handlers.register_show_categories_handlers(dp)
generate_referral_code.register_generate_code_handlers(dp)
show_users_handlers.register_show_users_handlers(dp)
create_category_handlers.register_create_category_handlers(dp)
delete_space_handlers.register_delete_space_handlers(dp)
make_spending_handlers.register_make_spending_handlers(dp)
show_spending_history.register_show_users_handlers(dp)

executor.start_polling(dp, skip_updates=True, on_startup=startup)

