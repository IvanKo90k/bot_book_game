# пробую відправляти повідомлення без участі користувачів

import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from Data.config import api_token

# Set up logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=api_token)
dp = Dispatcher(bot)

# List of user IDs to send messages to
user_ids = [560101130]  # Replace with actual user IDs

async def send_periodic_messages():
    while True:
        for user_id in user_ids:
            try:
                await bot.send_message(user_id, "Hello! This is a periodic message from your bot.")
            except Exception as e:
                logging.error(f"Failed to send message to user {user_id}: {e}")
        await asyncio.sleep(10)  # Send messages every hour

# @dp.message_handler(commands=['start'])
# async def start(message: types.Message):
#     await message.reply("Bot started. Periodic messages will be sent.")

async def on_startup(dp):
    await send_periodic_messages()


if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, on_startup=on_startup)