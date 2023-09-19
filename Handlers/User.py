# Зробити перевірку на мову, тобто щоб клієнт не вносив українське слово, коли потрібно вносити англійське
from loader import dp, types, bot
from Data.config import api_token
import random
import asyncio
import logging
import time
import Functions.DB, Functions.Functions
from stickers.stickers import stickers_start, stickers_money, stickers_cute, stickers_thank, stickers_bye
from oxford import phonetic_transcription
from States.user import registration, nextmessage
from aiogram.dispatcher import FSMContext

# Set up logging
logging.basicConfig(level=logging.INFO)

# bot = Bot(token=api_token)

number_sec_2_hours, number_sec_4_hours, number_sec_day, number_sec_week, number_sec_month = 10, 20, 30, 40, 50  # test
# number_sec_2_hours, number_sec_4_hours, number_sec_day, number_sec_week, number_sec_month = 7200, 14400, 86400, 604800, 2592000
# number_sec_day, number_sec_3_days, number_sec_week, number_sec_half_month, number_sec_month = 86400, 3*86400, 7*86400, 15*86400, 31*86400 # за словами Черненко дослідження підтверджують, що це допомагає вивчити слово ледь не назавжди

word_id = 0
id_for_start = 0
indx = 0
flag_new_word = False
flag_first_client = False
number_row = 0
name_button1 = ''
name_button2 = 'Заробити гроші'
user_ask_2 = False
temporary = ''
text_for_callmessage = 'here must be text_for_callmessage'


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    global flag_first_client, id_for_start
    id_for_start = message.from_user.id
    print("Користувач {0.first_name} натиснув start".format(message.from_user))
    count_rows_with_value = Functions.DB.count_rows_with_value(message.from_user.id)
    if count_rows_with_value > 0:
        await message.answer('Радий тебе бачити.')
        await Functions.Functions.send_random_sticker(bot, id_for_start, stickers_start)
    else:
        flag_first_client = True
        await Functions.Functions.send_random_sticker(bot, id_for_start, stickers_start)
        markup = types.InlineKeyboardMarkup(row_width=2)
        item4 = [types.InlineKeyboardButton("Так", callback_data='yes_helper'),
                 types.InlineKeyboardButton("Ні", callback_data='no_helper')]
        markup.add(*item4)
        await bot.send_message(message.chat.id,
                               'Дозволю собі припустити, що ти бажаєш покращити свою англійську. Хочеш, щоб я був твоїм помічником?',
                               reply_markup=markup)
        # keyboard
        # markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        # items = [types.KeyboardButton("Заробити гроші"), types.KeyboardButton("Друга кнопка")]
        # markup.add(*items)

        # await bot.send_message(message.chat.id,
        #                        "Дозволю собі припустити, що ти бажаєш покращити свою англійську. Тоді ти в правильному місці. Хочеш, щоб я був твоїм помічником?",
        #                        parse_mode='html', reply_markup=markup)
        #
        # keyboard
        # markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        # items = [types.KeyboardButton("Маю слово"), types.KeyboardButton("Приведи сюди слово")]
        # markup.add(*items)

        # await bot.send_sticker(message.chat.id, sti)
        # await bot.send_message(message.chat.id,
        #                        "Привіт! Я — помічник, розроблений, щоб допомогти тобі збільшити словниковий запас англійської мови.",
        #                        parse_mode='html', reply_markup=markup)
        # await asyncio.sleep(1)
        # await bot.send_message(message.chat.id,
        #                        'Зі мною працювати легко.\nНатрапивши на слово, яке хочеш вивчити, тисни <b>"Маю слово"</b>.\nЯкщо хочеш повторити слово, яке бажаєш вивчити, тисни <b>"Приведи сюди слово"</b>.',
        #                        parse_mode='html', reply_markup=markup)
        # await asyncio.sleep(2)
        # await bot.send_message(message.chat.id, 'Вони знизу, якщо що ⬇️⬇️⬇️', parse_mode='html', reply_markup=markup)


@dp.message_handler(commands=['help'])
async def help(message: types.Message):
    print("Користувач {0.first_name} натиснув help".format(message.from_user))
    await message.answer('Тут буде довідка')


@dp.message_handler(text='Маю слово')
async def admin(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer('Введи слово англійською мовою')
    await registration.eng_word.set()


@dp.message_handler(state=registration.eng_word)
async def first(message: types.Message, state: FSMContext):
    global user_ask_2, temporary
    # Save new English word and ask for Ukrainian word
    transcription = phonetic_transcription(message.text.lower())
    print('Задіяно блок для збереження англійського слова')
    await state.update_data(eng_word=message.text.lower(), transcription=transcription)
    print(transcription)
    if transcription == None:
        markup = types.InlineKeyboardMarkup(row_width=2)
        item3 = [types.InlineKeyboardButton("Існує", callback_data='exist'),
                 types.InlineKeyboardButton("Не існує", callback_data='no_exist')]
        markup.add(*item3)
        # await bot.send_message(message.chat.id, 'Раджу перевірити, чи таке слово точно існує.', reply_markup=markup)
        print(user_ask_2)
        if not user_ask_2:
            temporary = message.text.lower()
            await message.answer('Раджу перевірити, чи таке слово точно існує і лише потім звертатися до мене.')
            user_ask_2 = True
            await state.finish()
        else:
            await message.answer('Введи слово українською мовою')
            await registration.ua_word.set()
    else:
        await message.answer('Введи слово українською мовою')
        await registration.ua_word.set()


@dp.message_handler(state=registration.ua_word)
async def second(message: types.Message, state: FSMContext):
    global flag_first_client
    if message.text == 'Приведи сюди слово':
        await bot.send_message(message.chat.id,
                               'Треба вводити слово українською мовою, а не тиснути <b>"Приведи сюди слово"</b>! Починай спочатку, тисни <b>"Маю слово"</b>.')
    else:
        date = time.time()
        data = await state.get_data()
        # Check if the word already exists in the database
        if Functions.DB.check_row_with_two_values('user_id', message.from_user.id, 'eng_word',
                                                  data['eng_word']):  # якщо слово вже є в базі
            # Handle existing word scenario
            markup = types.InlineKeyboardMarkup(row_width=2)
            item2 = [types.InlineKeyboardButton("Бажаю", callback_data='yes'),
                     types.InlineKeyboardButton("Не бажаю", callback_data='no'),
                     types.InlineKeyboardButton("Покажи", callback_data='show'),
                     types.InlineKeyboardButton('Що таке "оновити"?', callback_data='info_update')]
            markup.add(*item2)
            await bot.send_message(message.chat.id, 'Таке слово у нас вже є. Бажаєш оновити?',
                                   reply_markup=markup)
        else:
            Functions.DB.insert_7_values(message.from_user.id, data['eng_word'], message.text.lower(),
                                         data['transcription'],
                                         date, date + number_sec_2_hours, 1)
        print('Задіяно блок для збереження українського слова')
        count_rows_with_value = Functions.DB.count_rows_with_value(message.from_user.id)
        one_date = Functions.DB.get_one_value('date', 'user_id', message.from_user.id)
        if count_rows_with_value == 1 and one_date != 1:
            Functions.DB.update_one_value(word_id, 'check_date', date + 10)
            sti = open('stickers/AnimatedSticker_cup.tgs', 'rb')
            await bot.send_message(message.chat.id, 'Вітаю!!! Перше слово отримано.')
            await bot.send_sticker(message.chat.id, sti)
            await asyncio.sleep(1)  # Asynchronous delay
            await bot.send_message(message.chat.id, 'Оце так початок. Я в захваті від тебе! 🤩')
            await asyncio.sleep(2)  # Asynchronous delay
            await bot.send_message(message.chat.id,
                                   'Тепер ти вже знаєш, як працювати з кнопкою <b>"Маю слово"</b>',
                                   parse_mode='html')
            flag_first_client = True  # допомагає новому клієнту зрозуміти, коли потрібно тиснути "Приведи сюди слово"
            await asyncio.sleep(4)  # Asynchronous delay
            await bot.send_message(message.chat.id,
                                   'А зараз настав час познайомитися з функціоналом іншої кнопки. Тисни <b>"Приведи сюди слово"</b>!',
                                   parse_mode='html')
    await state.finish()


@dp.message_handler(text='Приведи сюди слово')
async def process_user_words(message: types.Message, state: FSMContext):
    global flag_first_client, text_for_callmessage, number_row
    # await state.finish()
    flag = False  # для позначення наявності слів, які можна подати клієнту
    number_rows = Functions.DB.count_rows_in_database() + 1
    for number in range(1, int(number_rows)):  # перебираємо, враховуючи к-сть рядків
        number_row = number
        word_id, user_id, eng_word, ua_word, transcription, time_now, digit, check_date, odds, level, score, column1, column2 = await Functions.Functions.read_time_data(
            number)
        print(level, odds, user_id, flag_first_client)

        if level == 1 and odds > 10 and user_id == message.from_user.id and flag_first_client:
            flag, text_for_callmessage, number_row = await Functions.Functions.send_word(ua_word, eng_word,
                                                                                         transcription, bot,
                                                                                         number, message, level,
                                                                                         time_now)
            Functions.DB.update_one_value(word_id, 'check_date', time_now + number_sec_2_hours)
            break

        if level == 1 and odds > number_sec_2_hours and user_id == message.from_user.id:
            flag, text_for_callmessage, number_row = await Functions.Functions.send_word(ua_word, eng_word,
                                                                                         transcription, bot,
                                                                                         number, message, level,
                                                                                         time_now)
            Functions.DB.update_one_value(word_id, 'check_date', time_now + number_sec_2_hours)
            break

        elif level == 2 and odds > number_sec_4_hours and user_id == message.from_user.id:
            flag, text_for_callmessage, number_row = await Functions.Functions.send_word(ua_word, eng_word,
                                                                                         transcription, bot,
                                                                                         number, message, level,
                                                                                         time_now)
            Functions.DB.update_one_value(word_id, 'check_date', time_now + number_sec_day)
            break

        elif level == 3 and odds > number_sec_day and user_id == message.from_user.id:
            flag, text_for_callmessage, number_row = await Functions.Functions.send_word(ua_word, eng_word,
                                                                                         transcription, bot,
                                                                                         number, message, level,
                                                                                         time_now)
            Functions.DB.update_one_value(word_id, 'check_date', time_now + number_sec_week)
            break

        elif level == 4 and odds > number_sec_week and user_id == message.from_user.id:
            flag, text_for_callmessage, number_row = await Functions.Functions.send_word(ua_word, eng_word,
                                                                                         transcription, bot,
                                                                                         number, message, level,
                                                                                         time_now)
            Functions.DB.update_one_value(word_id, 'check_date', time_now + number_sec_month)
            break

        elif level == 5 and odds > number_sec_month and user_id == message.from_user.id:
            flag, text_for_callmessage, number_row = await Functions.Functions.send_word(ua_word, eng_word,
                                                                                         transcription, bot,
                                                                                         number, message, level,
                                                                                         time_now)
            Functions.DB.update_one_value(word_id, 'check_date', time_now + number_sec_month)
            break

    if flag == False:
        await bot.send_message(message.chat.id,
                               'Наразі нема слів, які готові до зустрічі з тобою. Приходь пізніше.')
        sti = open(f'stickers/AnimatedSticker_gorilla.tgs', 'rb')
        await bot.send_sticker(message.chat.id, sti)
    await state.finish()
    # await registration.name.set()


@dp.message_handler(content_types=types.ContentType.TEXT)
async def process_just_words(message: types.Message):
    await bot.send_message(message.chat.id,
                           'Для того, щоб я прийняв слово потрібно, щоб ти спочатку натиснув <b>"Маю слово"</b>, а після того написав слово',
                           parse_mode='html')


@dp.callback_query_handler(lambda c: c.data == 'yes_helper')
async def process_callback_0(callback_query: types.CallbackQuery):
    # Send another message with the "Go on" button when the user presses it
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Go on", callback_data="go_on"))

    response_message = [
        'Ласкаво прошу у наш світ!',
        'Дякую за довіру!'
    ]

    await bot.send_message(
        callback_query.from_user.id,
        response_message[0],
    )

    await Functions.Functions.send_random_sticker(bot, id_for_start, stickers_thank)
    await bot.send_message(
        callback_query.from_user.id,
        response_message[1],
    )

    # Remove the inline keyboard markup
    await bot.delete_message(
        callback_query.from_user.id,
        callback_query.message.message_id,
    )

    response_message = 'Мої послуги коштують 5 *лексикрон* на день.'
    await asyncio.sleep(2)  # Asynchronous delay

    await bot.send_message(
        callback_query.from_user.id,
        response_message,
        reply_markup=markup,
        parse_mode='Markdown',
    )

    # Answer the callback query to remove the "Go on" button
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == 'go_on')
async def process_callback(callback_query: types.CallbackQuery):
    global indx
    # Send another message with the "Go on" button when the user presses it
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Go on", callback_data="go_on"))

    # Responses message
    responses = [
        "Мої послуги коштують 5 *лексикрон* на день.",
        "*Лексикрони* - це наша валюта.",
        "До речі, наша держава виділяє певну суму лексикрон кожному, хто намагається рухатися в напрямку розвитку. Такі, як Ти, дуже важливі для нас.",
        "Про це потім більш детально розповім. А зараз введу тебе в курс справ. І не звертай уваги на мій вигляд.",
        "Ми, *морфіти*, можемо приймати будь-який вигляд, який добровільно забажаємо.",
    ]

    response_message = responses[indx]

    if indx < 2:
        await bot.send_message(
            callback_query.from_user.id,
            response_message,
            parse_mode='Markdown',
        )
    elif indx == 2:
        await bot.send_message(
            callback_query.from_user.id,
            responses[3],
            parse_mode='Markdown',
        )

    # Remove the inline keyboard markup
    await bot.delete_message(
        callback_query.from_user.id,
        callback_query.message.message_id,
    )

    indx += 1
    response_message = responses[indx]

    if indx == 1:
        await bot.send_message(
            callback_query.from_user.id,
            response_message,
            reply_markup=markup,
            parse_mode='Markdown',
        )
    elif indx == 2:
        await Functions.Functions.send_random_sticker(bot, id_for_start, stickers_money)
        await bot.send_message(id_for_start, response_message, parse_mode='Markdown')
        await asyncio.sleep(4)  # Asynchronous delay
        await bot.send_message(
            callback_query.from_user.id,
            responses[3],
            reply_markup=markup,
        )
    elif indx == 3:
        await Functions.Functions.send_random_sticker(bot, id_for_start, stickers_cute)
        await bot.send_message(id_for_start, responses[4], parse_mode='Markdown')
        indx = 0

    # Answer the callback query to remove the "Go on" button
    await callback_query.answer()


@dp.callback_query_handler(lambda callback_query: True)
async def callback_handler(call: types.CallbackQuery):
    global number_row, text_for_callmessage, flag_first_client, id_for_start
    print('flag_first_client =', flag_first_client)
    count_rows_in_database = Functions.DB.count_rows_in_database()
    if count_rows_in_database > 0:
        word_id, user_id, eng_word, ua_word, transcription, time_now, digit, check_date, odds, lvl, score, column1, column2 = await Functions.Functions.read_time_data(
            number_row)

    if call.message:
        if call.data == 'good':
            Functions.DB.update_one_value(number_row, 'level', lvl + 1)  # бот збільшує рівень на одиницю
            if lvl == 5:
                Functions.DB.update_date_lvl(number_row, time_now, lvl)  # встановлює нову дату і фіксує рівень 5
        elif call.data == 'bad':
            Functions.DB.update_date_lvl(number_row, time_now, lvl - 1)  # бот зменшує рівень на одиницю
            if lvl == 1:
                Functions.DB.update_date_lvl(number_row, time_now, lvl)  # встановлює нову дату і фіксує рівень 1
        elif call.data == 'yes':
            pass
        elif call.data == 'no':
            text_for_callmessage = 'Ок, рухаємося далі.'
        elif call.data == 'show':
            text_for_callmessage = f'{eng_word} - {ua_word}'
        elif call.data == 'info_update':
            text_for_callmessage = 'Оновлення - це...'
        elif call.data == 'no_helper':
            text_for_callmessage = 'До побачення!'
        # elif call.data == 'exist':
        #     text_for_callmessage = 'Ок. Тоді тисни ще раз <b>"Маю слово"</b> і повторно введи своє слово.'
        # elif call.data == 'no_exist':
        #     text_for_callmessage = 'Радий бути корисним'

        # remove inline buttons
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=text_for_callmessage, reply_markup=None)

        if flag_first_client:
            if text_for_callmessage == 'До побачення!':
                await Functions.Functions.send_random_sticker(bot, id_for_start, stickers_bye)
            else:
                text_first = ("*Приведи сюди слово* ти вже теж освоїв. Мої вітання!!!\n\n"
                              "В подальшому я буду повідомляти тебе, коли будуть готові слова для роботи з ними. Тоді тобі треба буде просто натиснути *Приведи сюди слово*.\n\n"
                              "Кнопкою *Маю слово* ти й так знаєш як користуватися. Тож до роботи! Назбираймо найбільшу колекцію слів 😉"
                              )
                await bot.send_message(user_id, text_first, parse_mode='Markdown')
                flag_first_client = False
            # flag_first_client = False

# @dp.message_handler(content_types=types.ContentType.TEXT)
# async def process_user_words(message: types.Message):
#     # Global variables initialization
#     global flag_new_word, just_number, word_id, number_row, text_for_callmessage, flag_first_client
#
#     # Check if the message is in a private chat
#     if message.chat.type == 'private':
#         Functions.DB.create_table()
#         word_id = Functions.DB.count_rows_in_database()  # рахує кількість рядків у таблиці
#
#         # Initialize user's data if not already done
#         if word_id == 0:
#             Functions.DB.insert_user(message.from_user.id, 1)  # вставка ID і порядкового номера рядка

# Handling different user messages
# if message.text == 'Маю слово':
#     flag_new_word, just_number = True, 1
#     if word_id > 0:
#         Functions.DB.insert_user(message.from_user.id, word_id + 1) # вставка ID і порядкового номера рядка
#     await bot.send_message(message.chat.id, 'Введи слово англійською мовою')
#
# elif message.text != 'Маю слово' and message.text != 'Приведи сюди слово':
#     if flag_new_word:
#         if just_number == 1:
#             # Check if the word already exists in the database
#             if Functions.DB.check_row_with_two_values('user_id', message.from_user.id, 'eng_word',
#                                                       message.text.lower()):  # якщо слово вже є в базі
#                 Functions.DB.delete_row_with_empty_cell('level')
#                 # Handle existing word scenario
#                 markup = types.InlineKeyboardMarkup(row_width=2)
#                 item2 = [types.InlineKeyboardButton("Бажаю", callback_data='yes'),
#                          types.InlineKeyboardButton("Не бажаю", callback_data='no'),
#                          types.InlineKeyboardButton("Покажи", callback_data='show'),
#                          types.InlineKeyboardButton('Що таке "оновити"?', callback_data='info_update')]
#                 markup.add(*item2)
#                 await bot.send_message(message.chat.id, 'Таке слово у нас вже є. Бажаєш оновити?',
#                                        reply_markup=markup)
#             else:
#                 # Save new English word and ask for Ukrainian word
#                 transcription = phonetic_transcription(message.text.lower())
#                 word_id = Functions.DB.count_rows_in_database()
#                 Functions.DB.update_eng_word(message.text.lower(), transcription, word_id)
#                 print('Задіяно блок для збереження англійського слова')
#                 just_number = 2
#                 await bot.send_message(message.chat.id, 'Введи слово українською мовою')
#
#         elif just_number == 2:
#             # Save Ukrainian word and trigger further actions
#             date = time.time()
#             Functions.DB.update(word_id, message.text.lower(), date, date + number_sec_2_hours, 1)
#             print('Задіяно блок для збереження українського слова')
#             count_rows_with_value = Functions.DB.count_rows_with_value(message.from_user.id)
#             one_date = Functions.DB.get_one_value('date', 'user_id', message.from_user.id)
#             if count_rows_with_value == 1 and one_date != 1:
#                 Functions.DB.update_one_value(word_id, 'check_date', date + 10)
#                 sti = open('stickers/AnimatedSticker_cup.tgs', 'rb')
#                 await bot.send_message(message.chat.id, 'Вітаю!!! Перше слово отримано.')
#                 await bot.send_sticker(message.chat.id, sti)
#                 await asyncio.sleep(1)  # Asynchronous delay
#                 await bot.send_message(message.chat.id, 'Оце так початок. Я в захваті від тебе! 🤩')
#                 await asyncio.sleep(2)  # Asynchronous delay
#                 await bot.send_message(message.chat.id,
#                                        'Тепер ти вже знаєш, як працювати з кнопкою <b>"Маю слово"</b>',
#                                        parse_mode='html')
#                 flag_first_client = True  # допомагає новому клієнту зрозуміти, коли потрібно тиснути "Приведи сюди слово"
#                 await asyncio.sleep(4)  # Asynchronous delay
#                 await bot.send_message(message.chat.id,
#                                        'А зараз настав час познайомитися з функціоналом іншої кнопки. Тисни <b>"Приведи сюди слово"</b>!',
#                                        parse_mode='html')
#             flag_new_word, just_number = False, 0
#     elif flag_new_word == False:
#         print('Задіяно блок')
#         await bot.send_message(message.chat.id,
#                                'Для того, щоб я прийняв слово потрібно, щоб ти спочатку натиснув <b>"Маю слово"</b>, а після того написав слово',
#                                parse_mode='html')

# elif message.text == 'Приведи сюди слово' and just_number == 0:
#     flag = False  # для позначення наявності слів, які можна подати клієнту
#     word_id = Functions.DB.count_rows_in_database() + 1
#     for number in range(1, int(word_id)):  # перебираємо, враховуючи к-сть рядків
#         number_row = number
#         word_id, user_id, eng_word, ua_word, transcription, time_now, digit, check_date, odds, level, score = await Functions.Functions.read_time_data(
#             number)
#
#         if level == 1 and odds > 10 and user_id == message.from_user.id and flag_first_client == True:
#             flag, text_for_callmessage, number_row = await Functions.Functions.send_word(ua_word, eng_word,
#                                                                                          transcription, bot,
#                                                                                          number, message, level,
#                                                                                          time_now)
#             Functions.DB.update_one_value(word_id, 'check_date', time_now + number_sec_2_hours)
#             await asyncio.sleep(3)  # Asynchronous delay
#             await bot.send_message(message.chat.id,
#                                    '<b>"Приведи сюди слово"</b> ти вже теж освоїв. Мої вітання!!!'
#                                    '\n\nВ подальшому я буду повідомляти тебе, коли будуть готові слова для роботи з ними. Тоді тобі треба буде просто натиснути <b>"Приведи сюди слово"</b>.'
#                                    '\n\nКнопкою <b>"Маю слово"</b> ти й так знаєш як користуватися. Тож до роботи! Назбираймо найбільшу колекцію слів 😉',
#                                    parse_mode='html')
#             flag_first_client = False
#             # await asyncio.sleep(number_sec_2_hours)  # Asynchronous delay
#             # await bot.send_message(message.chat.id, 'Настав час тиснути <b>"Приведи сюди слово"</b>', parse_mode='html')
#             break
#
#         if level == 1 and odds > number_sec_2_hours and user_id == message.from_user.id:
#             flag, text_for_callmessage, number_row = await Functions.Functions.send_word(ua_word, eng_word,
#                                                                                          transcription, bot,
#                                                                                          number, message, level,
#                                                                                          time_now)
#             Functions.DB.update_one_value(word_id, 'check_date', time_now + number_sec_2_hours)
#             # await asyncio.sleep(number_sec_2_hours)  # Asynchronous delay
#             # await bot.send_message(message.chat.id, 'Настав час тиснути <b>"Приведи сюди слово"</b>', parse_mode='html')
#             break
#
#         elif level == 2 and odds > number_sec_4_hours and user_id == message.from_user.id:
#             flag, text_for_callmessage, number_row = await Functions.Functions.send_word(ua_word, eng_word,
#                                                                                          transcription, bot,
#                                                                                          number, message, level,
#                                                                                          time_now)
#             Functions.DB.update_one_value(word_id, 'check_date', time_now + number_sec_day)
#             # await asyncio.sleep(number_sec_day)  # Asynchronous delay
#             # await bot.send_message(message.chat.id, 'Настав час тиснути <b>"Приведи сюди слово"</b>', parse_mode='html')
#             break
#
#         elif level == 3 and odds > number_sec_day and user_id == message.from_user.id:
#             flag, text_for_callmessage, number_row = await Functions.Functions.send_word(ua_word, eng_word,
#                                                                                          transcription, bot,
#                                                                                          number, message, level,
#                                                                                          time_now)
#             Functions.DB.update_one_value(word_id, 'check_date', time_now + number_sec_week)
#             # await asyncio.sleep(number_sec_week)  # Asynchronous delay
#             # await bot.send_message(message.chat.id, 'Настав час тиснути <b>"Приведи сюди слово"</b>', parse_mode='html')
#             break
#
#         elif level == 4 and odds > number_sec_week and user_id == message.from_user.id:
#             flag, text_for_callmessage, number_row = await Functions.Functions.send_word(ua_word, eng_word,
#                                                                                          transcription, bot,
#                                                                                          number, message, level,
#                                                                                          time_now)
#             Functions.DB.update_one_value(word_id, 'check_date', time_now + number_sec_month)
#             # await asyncio.sleep(number_sec_month)  # Asynchronous delay
#             # await bot.send_message(message.chat.id, 'Настав час тиснути <b>"Приведи сюди слово"</b>', parse_mode='html')
#             break
#
#         elif level == 5 and odds > number_sec_month and user_id == message.from_user.id:
#             flag, text_for_callmessage, number_row = await Functions.Functions.send_word(ua_word, eng_word,
#                                                                                          transcription, bot,
#                                                                                          number, message, level,
#                                                                                          time_now)
#             Functions.DB.update_one_value(word_id, 'check_date', time_now + number_sec_month)
#             # await asyncio.sleep(number_sec_month)  # Asynchronous delay
#             # await bot.send_message(message.chat.id, 'Настав час тиснути <b>"Приведи сюди слово"</b>', parse_mode='html')
#             break
#
#     if flag == False:
#         await bot.send_message(message.chat.id,
#                                'Наразі нема слів, які готові до зустрічі з тобою. Приходь пізніше.')
#         sti = open(f'stickers/AnimatedSticker_gorilla.tgs', 'rb')
#         await bot.send_sticker(message.chat.id, sti)
