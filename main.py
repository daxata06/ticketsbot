from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()
bot = Bot(token='5769394778:AAGx8hEz0CFoploddQyE1NrtSH_89ZLQQc8')
dp = Dispatcher(bot, storage=storage)
