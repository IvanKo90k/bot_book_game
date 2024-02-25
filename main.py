import asyncio
from Handlers import dp
from aiogram import executor
# from aiogram.contrib.middlewares.logging import LoggingMiddleware
from Functions.Functions import on_startup

# dp.middleware.setup(LoggingMiddleware())

if __name__ == '__main__':
    # Start the bot
    loop = asyncio.get_event_loop()
    # loop.create_task(on_startup(dp))

    executor.start_polling(dp, skip_updates=True)
