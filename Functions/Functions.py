import time
import asyncio
import logging
import string
from loader import bot, types
from Functions.DB import get_one_row, get_values_if_conditions
import random


async def send_random_sticker(bot, chat_id, sticker_list):
    if not sticker_list:
        return

    # Select a random sticker from the list using random.choice
    selected_sticker = random.choice(sticker_list)

    # Construct the sticker file path
    sticker_path = f'stickers/{selected_sticker}'

    # Send the sticker to the specified chat_id
    with open(sticker_path, 'rb') as sticker_file:
        await bot.send_sticker(chat_id, sticker_file)


async def read_time_data(number):
    time_now = time.time()
    word_id, user_id, eng_word, ua_word, transcription, digit, check_date, level, score, column1, column2 = get_one_row(
        number)
    odds = time_now - digit
    return word_id, user_id, eng_word, ua_word, transcription, time_now, digit, check_date, odds, level, score, column1, column2


async def send_word(ua_word, eng_word, transcription, bot, number, message, level, time_now):
    flag = True
    value, value_eng, value_t = ua_word, eng_word, transcription
    await bot.send_message(message.chat.id, f".\n.\n.\n{value}\n.\n.\n.")
    for i in range(3, 0, -1):
        await asyncio.sleep(1)
        await bot.send_message(message.chat.id, i)
    time.sleep(1)

    markup = types.InlineKeyboardMarkup(row_width=2)
    item1 = [types.InlineKeyboardButton("Я знаю", callback_data='good'),
             types.InlineKeyboardButton("Не пригадаю", callback_data='bad')]
    markup.add(*item1)
    await bot.send_message(message.chat.id, f"⭐\n {value_eng} \n{value_t}\n⭐", reply_markup=markup)  # бот дає переклад
    # await bot.send_message(message.chat.id, f"⭐\n{value_eng}\n⭐", reply_markup=markup)  # бот дає переклад
    text_for_callmessage = f"⭐\n{value_eng}\n⭐"

    number_row = number
    print(f"Scenario {level}")
    return flag, text_for_callmessage, number_row


# user_ids = get_unique_values('user_id')

# List of user IDs to send messages to
# user_ids = [] # get_values_if_conditions('user_id', 'check_date')

async def send_periodic_messages(bot, user_ids):
    print('Bot entered the sending loop')
    while True:
        user_ids = get_values_if_conditions('user_id', 'check_date')
        if user_ids:
            for user_id in user_ids:
                try:
                    await bot.send_message(user_id, 'Час тиснути <b>"Приведи сюди слово"</b>.')
                except Exception as e:
                    logging.error(f"Failed to send message to user {user_id}: {e}")
        await asyncio.sleep(20)  # Send messages every 20 seconds


async def on_startup(dp):
    while True:
        user_ids = get_values_if_conditions('user_id', 'check_date')
        print(user_ids, 'on_startup/Functions.py')
        if user_ids:
            await send_periodic_messages(bot, user_ids)
        await asyncio.sleep(20)


# async def send_periodic_messages(bot, user_ids):
#     print('Бот зайшов у розсилку (Functions.py)')
#     while True:
#         for user_id in user_ids:
#             try:
#                 await bot.send_message(user_id,
#                                        'Час тиснути <b>"Приведи сюди слово"</b>.')  # "Hello! This is a periodic message from your bot.")
#             except Exception as e:
#                 logging.error(f"Failed to send message to user {user_id}: {e}")
#         await asyncio.sleep(20)  # Send messages every hour
#
#
# async def on_startup(dp):
#     user_ids = get_values_if_conditions('user_id', 'check_date')
#     print(user_ids, 'on_startup/Functions.py')
#     await send_periodic_messages(bot, user_ids)
#     await asyncio.sleep(20)


def is_english_word(word):
    alphabet = set(string.ascii_lowercase)
    for char in word.replace(" ", ""):  # Ignore spaces
        if char.lower() not in alphabet:
            return False
    return True


def is_ukrainian_word(word):
    ukrainian_alphabet = set("абвгґдеєжзиіїйклмнопрстуфхцчшщьюя")
    for char in word.replace(" ", ""):  # Ignore spaces
        if char.lower() not in ukrainian_alphabet:
            return False
    return True
