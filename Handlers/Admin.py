from loader import dp
from aiogram import types
from Data.config import admins
from Data import text


@dp.message_handler(commands=['admin'])
async def admin(message: types.Message):
    if message.from_user.id in admins:
        await message.answer(text.admin_msg)
