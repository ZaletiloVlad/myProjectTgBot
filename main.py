from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text
from aiogram.utils import executor
from handlers import create_space_handlers

from services.botAPI import bot_service

storage = MemoryStorage()

BOT_TOKEN = '5960706975:AAGec02BckR7g3ZE5Gl5VCnRUit7LQdeZKw'

bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot, storage=storage)


async def startup(_):
    bot_service.check_availability()


@dp.message_handler(commands=['start'])
async def help_cmd(msg: types.Message):
    user_info = {
        'name': msg.from_user.first_name,
        'telegram_id': msg.from_user.id,
    }

    if msg.from_user.last_name:
        user_info['name'] += f" {msg.from_user.last_name}"

    if msg.from_user.username:
        user_info['name'] += f" | @{msg.from_user.username}"

    user = bot_service.get_user_id(user_info)

    ikb = types.InlineKeyboardMarkup(row_width=1)
    ikb.add(types.InlineKeyboardButton("Начать работу со SPACE'ами", callback_data=f"start_{user['id']}"))

    await msg.answer(f"Здравствуйте, {user['name']}", reply_markup=ikb)

@dp.message_handler(commands=['help'])
async def start_cmd(msg: types.Message):
    pass

@dp.callback_query_handler(Text(contains='start'))
async def start_work(callback: types.CallbackQuery):
    user_id = callback.data.split('_')[-1]
    inline_kb = types.InlineKeyboardMarkup(row_width=1)
    user_spaces_response = bot_service.get_user_spaces(user_id)
    print(user_spaces_response)
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
    await callback.message.answer('Выберите SPACE, с которым хотите начать работу', reply_markup=inline_kb)
    await callback.answer()


create_space_handlers.register_create_space_handlers(dp)

executor.start_polling(dp, skip_updates=True, on_startup=startup)
