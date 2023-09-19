# import os
# import openai
# import telebot
# from Data.config import api_token, openai_api_key
#
# openai.api_key = os.getenv('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')
# bot = telebot.TeleBot(token=api_token)
#
# @bot.message_handler(func=lambda message: True)
# def handle_message(message):
#     response = openai.Completion.create(
#       model="text-davinci-003",
#       prompt=message.text,
#       temperature=0.5,
#       max_tokens=100,
#       top_p=1.0,
#       frequency_penalty=0.5,
#       presence_penalty=0.0
#     )
#     bot.send_message(chat_id=message.from_user.id, text=response['choices'][0]['text'])
#
# bot.polling()

import os
import openai
from aiogram import Bot, Dispatcher, types
from Data.config import api_token, openai_api_key

openai.api_key = openai_api_key
bot = Bot(token=api_token)

dp = Dispatcher(bot)


@dp.message_handler(content_types=types.ContentType.TEXT)
async def handle_message(message: types.Message):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=message.text,
        temperature=0.5,
        max_tokens=60,
        top_p=1.0,
        frequency_penalty=0.5,
        presence_penalty=0.0,
    )
    reply = response.choices[0].text.strip()

    await bot.send_message(chat_id=message.chat.id, text=reply)


if __name__ == '__main__':
    from aiogram import executor

    executor.start_polling(dp)

# @dp.message_handler(content_types=types.ContentType.TEXT)
# async def handle_message(message: types.Message):
#     try:
#         response = openai.Completion.create(
#             model="text-davinci-003",
#             prompt=message.text,
#             temperature=0.5,
#             max_tokens=100,
#             top_p=1.0,
#             frequency_penalty=0.5,
#             presence_penalty=0.0
#         )
#         reply = response.choices[0].text.strip()
#         await bot.send_message(chat_id=message.from_user.id, text=reply)
#     except Exception as e:
#         # Handle the exception (e.g., logging, sending an error message, etc.)
#         print("An error occurred:", str(e))
#
#
# # async def handle_message(message: types.Message):
# #     response = openai.Completion.create(
# #         model="text-davinci-003",
# #         prompt=message.text,
# #         temperature=0.5,
# #         max_tokens=100,
# #         top_p=1.0,
# #         frequency_penalty=0.5,
# #         presence_penalty=0.0
# #     )
# #     bot.send_message(chat_id=message.from_user.id, text=response['choices'][0]['text'])
#
#
# async def start_polling():
#     await dp.start_polling(dp)
#
#
# if __name__ == '__main__':
#     executor.start_polling(dp)
