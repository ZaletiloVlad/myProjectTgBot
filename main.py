from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

from services.botAPI import bot_service

BOT_TOKEN = '5960706975:AAGec02BckR7g3ZE5Gl5VCnRUit7LQdeZKw'

bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot)


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
    print(user)

    await msg.answer(f"Здравствуйте {user['name']}")


@dp.message_handler(commands=['help'])
async def start_cmd(msg: types.Message):
    inline_kb = types.InlineKeyboardMarkup(row_width=1)
    user_spaces_response = bot_service.get_user_spaces(msg.from_user.id)
    print(user_spaces_response['results'])

    for space in user_spaces_response['results']:
        inline_kb.add(
            types.InlineKeyboardButton(space['title'])
        )

    inline_kb.add(types.InlineKeyboardButton('Создать новый SPACE', callback_data='create_new_space'))
    await msg.answer('Выберите SPACE, с которым хотите начать работу', reply_markup=inline_kb)


executor.start_polling(dp, skip_updates=True, on_startup=startup)
