from multiprocessing import Process
import aiohttp
import asyncio
from Handlers import dp
from aiogram import executor, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from Functions.Functions import on_startup

dp.middleware.setup(LoggingMiddleware())

if __name__ == '__main__':
    # Start the bot
    loop = asyncio.get_event_loop()
    loop.create_task(on_startup(dp))

    executor.start_polling(dp, skip_updates=True)

    # tracemalloc.start()
    # Optionally, print memory statistics here
    # current, peak = tracemalloc.get_traced_memory()
    # print(f"Current memory usage: {current / 10 ** 6} MB")
    # print(f"Peak memory usage: {peak / 10 ** 6} MB")
    # tracemalloc.stop()

# if __name__ == '__main__':
#     executor.start_polling(dp, on_startup=on_startup, skip_updates=True)

# Your main function
# async def main():
#     try:
#         executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
#     finally:
#         # Close the client session and connector when the bot is exiting
#         async with bot.session as session:
#             await session.close()

# bot = Bot(token='6278513334:AAF4IKJsO6hiYtchRfERBrKdqG-clygvho0')
# dp = Dispatcher(bot)
# stickers = ['sticker.webp', 'AnimatedSticker2.tgs', 'AnimatedSticker3.tgs', 'AnimatedSticker4.tgs',
#             'AnimatedSticker5.tgs', 'sticker_lady.webp', 'sticker_prof.webp', 'sticker_gus.webp', 'sticker_bear.webp',
#             'sticker_hi.webp', 'sticker_kianu.webp', 'AnimatedSticker_donkey.tgs', 'sticker_cat.webp',
#             'sticker_bereg.webp']
# stickers_finish = ['AnimatedSticker_congrat.tgs']
# # stickers = ['AnimatedSticker.tgs'] на перспективу
#
# number_seconds_2_hours, number_seconds_day, number_seconds_week, number_seconds_month = 20, 86400, 604800, 2592000
#
# number_row, text_for_callmessage, just_number = 0, 0, 0
# flag_new_word, flag, flag_vocabulary = False, False, False
# name_file = ''
# new_words = []
# count_rows = []
# words_for_writing = []
# data = []
# encodings = ['utf-8', 'cp1252']
# separator = ';'
# time_first_word = 0
#
#
# @dp.message_handler(commands=['start'])
# async def start(message: types.Message):
#     print("Користувач {0.first_name} натиснув start".format(message.from_user))
#     digit_sti = random.randint(0, len(stickers) - 1)
#     sti_0 = stickers[digit_sti]
#     sti = open(sti_0, 'rb')
#
#     # keyboard
#     markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
#     items = [types.KeyboardButton("Маю слово"), types.KeyboardButton("Приведи сюди слово")]
#     markup.add(*items)
#
#     await bot.send_sticker(message.chat.id, sti)
#     await bot.send_message(message.chat.id,
#                            "Привіт! Я — помічник, розроблений, щоб допомогти тобі збільшити словниковий запас англійської мови.",
#                            parse_mode='html', reply_markup=markup)
#     await asyncio.sleep(3)
#     await bot.send_message(message.chat.id,
#                            'Зі мною працювати легко.\nНатрапивши на слово, яке хочеш вивчити, тисни "Маю слово".\nЯкщо хочеш повторити слово, яке бажаєш вивчити, тисни "Приведи сюди слово".',
#                            parse_mode='html', reply_markup=markup)
#
#
# async def send_word(bot, df, number, message, level, time_now):
#     flag = True
#     value = df.loc[number, 'ua_word']
#     value_eng = df.loc[number, 'word']
#     await bot.send_message(message.chat.id, f".\n.\n.\n{value}\n.\n.\n.")
#     for i in range(3):
#         await asyncio.sleep(1)
#         await bot.send_message(message.chat.id, i + 1)
#     time.sleep(1)
#
#     markup = types.InlineKeyboardMarkup(row_width=2)
#     item1 = [types.InlineKeyboardButton("Я знаю", callback_data='good'),
#              types.InlineKeyboardButton("Не пригадаю", callback_data='bad')]
#     markup.add(*item1)
#     await bot.send_message(message.chat.id, f"⭐\n{value_eng}\n⭐", reply_markup=markup)  # бот дає переклад
#     text_for_callmessage = f"⭐\n{value_eng}\n⭐"
#
#     number_row = number
#     level_up = int(level + 1)
#     if level_up < 4:
#         df.loc[number, 'date'] = time_now  # бот змінює час на поточний
#     elif level_up == 4:
#         df.loc[number, 'month_date'] = time_now + number_seconds_month
#     elif level_up > 4:
#         df.loc[number, 'month_date'] = time_now + number_seconds_month
#     df.loc[number, 'level'] = level_up  # бот збільшує рівень на одиницю
#     df.to_csv(name_file, sep=separator, index=False, encoding='cp1251')  # бот змінює дані в файлі csv
#     print(f"Scenario {level_up}")
#     return flag, text_for_callmessage, number_row
#
#
# @dp.message_handler(content_types=types.ContentType.TEXT)
# async def process_user_words(message: types.Message):
#     global word_eng, number_row, text_for_callmessage, flag_new_word, just_number, number_row_word, name_file, separator, time_first_word, encodings
#
#     if message.chat.type == 'private':
#         df_id = pd.read_csv("id.csv", sep=';', encoding='cp1251')
#         count_finded = 0
#         for value in range(len(df_id['id'])):
#             if message.chat.id == df_id.loc[value, 'id']:  # якщо інформація про клієнта вже є в базі
#                 count_finded += 1
#                 break
#
#         if count_finded == 0:  # якщо клієнт новий, інформація про нього відсутня в базі
#             df_id.loc[len(df_id['id']), 'id'] = message.chat.id  # записуємо id клієнта у файл з id
#             name_file = 'words_client_' + str(message.chat.id) + '.csv'
#             df_id.to_csv('id.csv', sep=separator, index=False, encoding='cp1251')  # бот змінює дані в файлі csv
#             data = [[1, 1, 1, 1, 1, 0], [1, 1, 1, 1, 1, 0]]
#             df_user_words = pd.DataFrame(data,
#                                          columns=['word', 'ua_word', 'date', 'week_date', 'month_date', 'level'])
#             df_user_words.to_csv(name_file, sep=separator, index=False, encoding='cp1251')  # бот створює файл csv
#             count_finded = 1
#         if count_finded == 1:  # якщо інформація про клієнта вже є в базі
#             name_file = 'words_client_' + str(message.chat.id) + '.csv'
#             df_user_words = pd.read_csv(name_file, sep=';', encoding='cp1251')
#
#         if message.text == 'Маю слово':
#             flag_new_word, just_number = True, 1
#             await bot.send_message(message.chat.id, 'Введи слово англійською мовою')
#
#         if message.text != 'Маю слово' and message.text != 'Приведи сюди слово':
#             if flag_new_word == False:
#                 await bot.send_message(message.chat.id,
#                                        'Для того, щоб я прийняв слово потрібно, щоб ти спочатку натиснув "Маю слово", а після того написав слово')
#
#         if message.text != 'Маю слово' and message.text != 'Приведи сюди слово':
#             if flag_new_word == True:
#                 if just_number == 1:
#                     if len(df_user_words['word']) == 2 and df_user_words.loc[0, 'word'] == 1 and df_user_words.loc[
#                         1, 'word'] == 1:
#                         print('Задіяно блок для збереження англійського слова 1')
#                         df_user_words.loc[0, 'word'] = message.text  # бот вносить перше англійське слово
#
#                     elif len(df_user_words['word']) == 2 and df_user_words.loc[0, 'level'] == 1 and int(
#                             df_user_words.loc[1, 'date']) == 1:
#                         print('Задіяно блок для збереження англійського слова 2')
#                         df_user_words.loc[1, 'word'] = message.text  # бот вносить друге англійське слово
#
#                     elif len(df_user_words['word']) == 2 and df_user_words.loc[1, 'level'] == 1:
#                         print('Задіяно блок для збереження англійського слова 3')
#                         number_row_word = len(df_user_words['word']) + 1
#                         df_user_words.loc[number_row_word, 'word'] = message.text  # бот вносить англійське слово
#                         df_user_words.loc[number_row_word, 'date'] = 1
#                         df_user_words.loc[number_row_word, 'week_date'] = 1
#                         df_user_words.loc[number_row_word, 'month_date'] = 1
#                         df_user_words.loc[number_row_word, 'level'] = 1
#
#                     elif len(df_user_words['word']) > 2:
#                         print('Задіяно блок для збереження англійського слова 4 або більше')
#                         count_flag = 0
#                         for i in range(len(df_user_words['word']) - 1):
#                             if message.text == df_user_words.loc[i, 'word']:
#                                 bot.send_message(message.chat.id, 'We have this word. I will send it to you later')
#                                 count_flag = 1
#                                 break
#
#                         if count_flag == 0:
#                             number_row_word = len(df_user_words['word'])
#                             df_user_words.loc[number_row_word, 'word'] = message.text  # бот вносить англійське слово
#                             df_user_words.loc[number_row_word, 'date'] = 1
#                             df_user_words.loc[number_row_word, 'week_date'] = 1
#                             df_user_words.loc[number_row_word, 'month_date'] = 1
#                             df_user_words.loc[number_row_word, 'level'] = 1
#
#                     just_number = 2
#                     df_user_words.to_csv(name_file, sep=separator, index=False,
#                                          encoding='cp1251')  # Save data to the CSV file
#
#                     await bot.send_message(message.chat.id, 'Введи слово українською мовою')
#
#                 elif just_number == 2:
#                     if len(df_user_words['ua_word']) == 2 and df_user_words.loc[0, 'ua_word'] == 1 and \
#                             df_user_words.loc[1, 'ua_word'] == 1:
#                         print('Задіяно блок для збереження українського слова 1')
#                         df_user_words.loc[0, 'ua_word'] = message.text  # бот вносить українське слово
#                         df_user_words.loc[0, 'date'] = time.time()
#                         df_user_words.loc[0, 'level'] = 1
#                         time_first_word = time.time() + number_seconds_2_hours
#                         sti = open('AnimatedSticker_cup.tgs', 'rb')
#                         await bot.send_message(message.chat.id, 'Вітаю!!! Перше слово отримано.')
#                         await bot.send_sticker(message.chat.id, sti)
#
#                     elif len(df_user_words['ua_word']) == 2 and df_user_words.loc[0, 'level'] == 1 and \
#                             df_user_words.loc[1, 'date'] == 1:
#                         print('Задіяно блок для збереження українського слова 2')
#                         df_user_words.loc[1, 'ua_word'] = message.text  # бот вносить українське слово
#                         df_user_words.loc[1, 'date'] = time.time()
#                         df_user_words.loc[1, 'level'] = 1
#
#                     elif len(df_user_words['word']) == 3:
#                         print('Задіяно блок для збереження українського слова 3')
#                         df_user_words.loc[number_row_word - 1, 'ua_word'] = message.text  # бот вносить українське слово
#                         df_user_words.loc[number_row_word - 1, 'date'] = time.time()
#
#                     elif len(df_user_words['word']) > 2:
#                         print('Задіяно блок для збереження українського слова 4 або більше')
#                         df_user_words.loc[number_row_word, 'ua_word'] = message.text  # бот вносить українське слово
#                         df_user_words.loc[number_row_word, 'date'] = time.time()
#
#                     df_user_words.to_csv(name_file, sep=separator, index=False,
#                                          encoding='cp1251')  # Save data to the CSV file
#                     print(df_user_words)
#                     flag_new_word, just_number = False, 0
#
#         if message.text == 'Приведи сюди слово' and just_number == 0:
#             df = pd.read_csv(name_file, sep=';', encoding='cp1251')
#             for number in range(len(df_user_words['ua_word'])):  # перебираємо, враховуючи к-сть рядків
#                 time_now, digit, digit_week, digit_month, odds, odds_week, odds_month, level = read_time_data(
#                     df_user_words, number)
#
#                 if level == 1 and odds > number_seconds_2_hours:
#                     flag, text_for_callmessage, number_row = await send_word(bot, df, number, message, level, time_now)
#                     break
#
#                 elif level == 2 and odds > number_seconds_day:
#                     flag, text_for_callmessage, number_row = await send_word(bot, df, number, message, level, time_now)
#                     break
#
#                 elif level == 3 and odds_week > number_seconds_week:
#                     flag, text_for_callmessage, number_row = await send_word(bot, df, number, message, level, time_now)
#                     break
#
#                 else:
#                     await bot.send_message(message.chat.id,
#                                            'Наразі нема слів, які готові до зустрічі з тобою. Приходь пізніше.')
#                     sti = open('AnimatedSticker_gorilla.tgs', 'rb')
#                     await bot.send_sticker(message.chat.id, sti)
#                     break
#
#
# @dp.callback_query_handler(lambda callback_query: True)
# async def callback_handler(call: types.CallbackQuery):
#     global number_row, text_for_callmessage, name_file, separator
#     df = pd.read_csv(name_file, sep=';', encoding='cp1251')
#     time_now, digit, digit_week, digit_month, odds, odds_week, odds_month, level = read_time_data(df, number_row)
#
#     if call.message:
#         if call.data == 'bad':
#             df.loc[number_row, 'level'] = int(int(df.loc[number_row, 'level']) - 1)  # бот зменшує рівень на одиницю
#             df.to_csv(name_file, sep=separator, index=False, encoding='cp1251')  # бот змінює дані в файлі csv
#
#         # remove inline buttons
#         await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
#                                     text=text_for_callmessage, reply_markup=None)
#
#
# def main():
#     executor.start_polling(dispatcher=dp, skip_updates=True) # skip if not work
#
#
# if __name__ == '__main__':
#     main()
