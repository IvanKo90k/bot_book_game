from aiogram.contrib.fsm_storage.memory import MemoryStorage
from Data.config import api_token
from aiogram import Bot, Dispatcher, types


bot = Bot(token=api_token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())
