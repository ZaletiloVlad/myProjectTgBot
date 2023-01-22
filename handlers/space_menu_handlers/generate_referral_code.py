from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text

from services.botAPI import bot_service
from utils.return_keyboard import return_kb


# @dp.callback_query_handler(Text(contains='generate_code'))
async def generate_code(callback: types.CallbackQuery):
    code_info ={
        'user': callback.data.split('_')[-2],
        'space': callback.data.split('_')[-1]
    }

    code = bot_service.generate_code(code_info)
    time = f"{code['expiration_time'][11:19]} {code['expiration_time'][:10]}"

    await callback.message.edit_text(f'Вы сгенерировали код подключения к этому SPACE:\n\n{code["code"]}\n\n'
                                 f'Сохраните его у себя и перешлите пользователю для подключения. '
                                 f'Код будет действителен до {time}, после этого для подключения новых пользователей '
                                 f'Вам необходимо будет сгенерировать новый код!!!',
                                 reply_markup=return_kb(callback.data.split('_')[-2]))
    await callback.answer()

def register_generate_code_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(generate_code, Text(contains='generate_code'))