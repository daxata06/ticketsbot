from main import dp
from aiogram import executor
from keyboards import start_keyboard
from handlers import start_handlers, support_handler, inline_button_handler, message_handler





dp.message_handler(message_handler)
dp.register_message_handler(start_handlers, commands=['start'], state=None)
dp.register_message_handler(support_handler, commands=['support'], state=None)
dp.register_callback_query_handler(inline_button_handler, lambda c: c.data)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)