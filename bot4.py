# Цей бот щось середнє між 2 і 3
import telebot
import random
import time
import pandas as pd
from telebot import types

bot = telebot.TeleBot('5881819552:AAHdmb-kAi5zdGMaJkbjnw2VS8tlD0aO_wY')

# lst_eng = ['LEG', 'ARM', 'MUG', 'OPINION', 'CITY', 'CUP']
# lst_ua = ['НОГА', 'РУКА', 'КРУЖКА', 'ДУМКА', 'МІСТО', 'ЧАШКА']
stickers = ['sticker.webp', 'AnimatedSticker2.tgs', 'AnimatedSticker3.tgs', 'AnimatedSticker4.tgs',
            'AnimatedSticker5.tgs', 'sticker_lady.webp', 'sticker_prof.webp', 'sticker_gus.webp', 'sticker_bear.webp',
            'sticker_hi.webp', 'sticker_kianu.webp', 'AnimatedSticker_donkey.tgs', 'sticker_cat.webp',
            'sticker_bereg.webp']
stickers_finish = ['AnimatedSticker_congrat.tgs']
# stickers = ['AnimatedSticker.tgs'] на перспективу

number_seconds_2_hours, number_seconds_day, number_seconds_week, number_seconds_month = 7200, 86400, 604800, 2592000
message_for_cancel = "Don't give this word anymore"  # варто залишати?

# id_clients = [12, 560101130]
number_row, text_for_callmessage, just_number = 0, 0, 0
flag_new_word, flag, flag_vocabulary = False, False, False
name_file = ''
new_words = []
count_rows = []
words_for_writing = []
data = []


def send_word(bot, df, number, df_3000, df3, message, level, time_now):
    flag = True
    value = df.loc[number, 'ua_word']
    value_eng = df.loc[number, 'word']
    for value_tr in range(len(df_3000['word']) - 1):
        if df_3000.loc[value_tr, 'word'] == value_eng:
            value_t = df3.loc[number, 'transcription']
            count_is_transcription = 1
    bot.send_message(message.chat.id, f".\n.\n.\n{value}\n.\n.\n.")
    for i in range(3):
        time.sleep(1)
        bot.send_message(message.chat.id, i + 1)
    time.sleep(1)

    markup = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton("I know", callback_data='good')
    item2 = types.InlineKeyboardButton("I don't know", callback_data='bad')
    item3 = types.InlineKeyboardButton("Don't give this word anymore", callback_data='ok')
    markup.add(item1, item2, item3)
    if count_is_transcription == 1:
        bot.send_message(message.chat.id, f"⭐\n{value_eng} \n{value_t}\n⭐",
                         reply_markup=markup)  # бот дає переклад
        text_for_callmessage = f"⭐\n{value_eng} \n{value_t}\n⭐"
    elif count_is_transcription == 0:
        bot.send_message(message.chat.id, f"⭐\n{value_eng}\n⭐", reply_markup=markup)  # бот дає переклад
        text_for_callmessage = f"⭐\n{value_eng}\n⭐"

    number_row = number
    level_up = int(level + 1)
    if level_up < 4:
        df.loc[number, 'date'] = time_now  # бот змінює час на поточний
    elif level_up == 4:
        df.loc[number, 'month_date'] = time_now + number_seconds_month
    elif level_up > 4:
        df.loc[number, 'month_date'] = time_now + number_seconds_month
    df.loc[number, 'level'] = level_up  # бот збільшує рівень на одиницю
    df.to_csv(name_file, sep=';', index=False, encoding='cp1251')  # бот змінює дані в файлі csv
    print(f"Scenario {level_up}")
    return flag, text_for_callmessage, number_row


def read_time_data(df, number):
    time_now = time.time()
    digit, digit_week, digit_month, level = df.loc[number, ['date', 'week_date', 'month_date', 'level']].astype(float)
    odds, odds_week, odds_month = map(lambda d: time_now - d, [digit, digit_week, digit_month])
    return time_now, digit, digit_week, digit_month, odds, odds_week, odds_month, level


@bot.message_handler(commands=['start'])
def welcome(message):
    print("Користувач {0.first_name} натиснув start".format(message.from_user))
    digit_sti = random.randint(0, len(stickers) - 1)
    sti_0 = stickers[digit_sti]
    sti = open(sti_0, 'rb')
    bot.send_sticker(message.chat.id, sti)

    # keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    item1 = types.KeyboardButton("Give me a word")
    item2 = types.KeyboardButton("I want to enlarge my vocabulary")
    item3 = types.KeyboardButton("I am lazy. I want to learn your words")

    markup.add(item1, item2, item3)

    # bot.send_message(message.chat.id,
    #                  "Hi, {0.first_name}!\nI'm - <b>{1.first_name}</b>, I'll try to help you in learning English".format(
    #                      message.from_user, bot.get_me()), parse_mode='html', reply_markup=markup)
    bot.send_message(message.chat.id, "Hi, my sweetheart! I am glad to see here.", parse_mode='html',
                     reply_markup=markup)


@bot.message_handler(content_types=['text'])
def lalala(message):
    global word_eng, number_row, text_for_callmessage, flag_new_word, just_number, number_row_word, name_file
    # counter = 0
    if message.chat.type == 'private':

        df_id = pd.read_csv("id.csv", sep=';', encoding='cp1251')

        count_finded = 0
        for value in range(len(df_id['id'])):
            if message.chat.id == df_id.loc[value, 'id']:  # якщо інформація про клієнта вже є в базі
                count_finded += 1
                break

        if count_finded == 0:  # якщо клієнт новий, інформація про нього відсутня в базі
            df_id.loc[len(df_id['id']), 'id'] = message.chat.id  # записуємо id клієнта у файл з id
            name_file = 'words_client_' + str(message.chat.id) + '.csv'
            df_id.to_csv('id.csv', sep=';', index=False, encoding='cp1251')  # бот змінює дані в файлі csv
            data = [[1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1]]
            df_user_words = pd.DataFrame(data,
                                         columns=['word', 'ua_word', 'date', 'week_date', 'month_date', 'level'])
            df_user_words.to_csv(name_file, sep=';', index=False, encoding='cp1251')  # бот створює файл csv
            count_finded = 1
        if count_finded == 1:  # якщо інформація про клієнта вже є в базі
            name_file = 'words_client_' + str(message.chat.id) + '.csv'
            df_user_words = pd.read_csv(name_file, sep=';', encoding='cp1251')
            if message.text == 'Give me a word' and len(df_user_words['word']) == 2:
                bot.send_message(message.chat.id,
                                 'First you should to give me a word for learning. Press "I want to enlarge my vocabulary" or "I am lazy. I want to learn your words"')

        if message.text != 'Give me a word' and message.text != 'I want to enlarge my vocabulary' and flag_new_word == True:  # or message.text == 'I am lazy. Give me your word':
            if just_number == 1:  # and message.text != 'I am lazy. Give me your word':
                if len(df_user_words['word']) == 2 and df_user_words.loc[0, 'word'] == 1 and df_user_words.loc[
                    1, 'word'] == 1:
                    df_user_words.loc[0, 'word'] = message.text  # бот вносить перше англійське слово
                    df_user_words.to_csv(name_file, sep=';', index=False,
                                         encoding='cp1251')  # бот змінює дані в файлі csv
                    just_number = 2
                    bot.send_message(message.chat.id, 'Enter a word in Ukrainian')
                elif len(df_user_words['word']) == 2 and df_user_words.loc[1, 'date'] == 2 and df_user_words.loc[
                    1, 'week_date'] == 1:
                    df_user_words.loc[1, 'word'] = message.text  # бот вносить друге англійське слово
                    df_user_words.to_csv(name_file, sep=';', index=False,
                                         encoding='cp1251')  # бот змінює дані в файлі csv
                    just_number = 2
                    bot.send_message(message.chat.id, 'Enter a word in Ukrainian')
                elif len(df_user_words['word']) == 2 and df_user_words.loc[1, 'date'] == 2 and df_user_words.loc[
                    1, 'week_date'] == 2:
                    # print('зайшов 5')
                    number_row_word = len(df_user_words['word']) + 1
                    df_user_words.loc[number_row_word, 'word'] = message.text  # бот вносить англійське слово
                    df_user_words.loc[number_row_word, 'date'] = 1
                    df_user_words.loc[number_row_word, 'week_date'] = 1
                    df_user_words.loc[number_row_word, 'month_date'] = 1
                    df_user_words.loc[number_row_word, 'level'] = 1
                    df_user_words.to_csv(name_file, sep=';', index=False,
                                         encoding='cp1251')  # бот змінює дані в файлі csv
                    just_number = 2
                    bot.send_message(message.chat.id, 'Enter a word in Ukrainian')
                elif len(df_user_words['word']) > 2:
                    # print('зайшов 7')
                    count_flag = 0
                    for i in range(len(df_user_words['word']) - 1):
                        if message.text == df_user_words.loc[i, 'word']:
                            bot.send_message(message.chat.id, 'We have this word. I will send it to you later')
                            count_flag = 1
                            break

                    if count_flag == 0:
                        # print(message.text, df_user_words.loc[i, 'word'])
                        number_row_word = len(df_user_words['word'])
                        df_user_words.loc[number_row_word, 'word'] = message.text  # бот вносить англійське слово
                        df_user_words.loc[number_row_word, 'date'] = 1
                        df_user_words.loc[number_row_word, 'week_date'] = 1
                        df_user_words.loc[number_row_word, 'month_date'] = 1
                        df_user_words.loc[number_row_word, 'level'] = 1
                        df_user_words.to_csv(name_file, sep=';', index=False,
                                             encoding='cp1251')  # бот змінює дані в файлі csv
                        just_number = 2
                        bot.send_message(message.chat.id, 'Enter a word in Ukrainian')

            elif just_number == 2:
                if len(df_user_words['ua_word']) == 2 and df_user_words.loc[0, 'ua_word'] == 1 and df_user_words.loc[
                    1, 'ua_word'] == 1:
                    df_user_words.loc[0, 'ua_word'] = message.text  # бот вносить українське слово
                    df_user_words.loc[1, 'date'] = 2
                    df_user_words.to_csv(name_file, sep=';', index=False,
                                         encoding='cp1251')  # бот змінює дані в файлі csv
                elif len(df_user_words['ua_word']) == 2 and df_user_words.loc[1, 'date'] == 2 and df_user_words.loc[
                    1, 'week_date'] == 1:
                    df_user_words.loc[1, 'ua_word'] = message.text  # бот вносить українське слово
                    df_user_words.loc[1, 'week_date'] = 2
                    df_user_words.to_csv(name_file, sep=';', index=False,
                                         encoding='cp1251')  # бот змінює дані в файлі csv
                elif len(df_user_words['ua_word']) > 2 and df_user_words.loc[1, 'date'] == 2 and df_user_words.loc[
                    1, 'week_date'] == 2:
                    df_user_words.loc[number_row_word - 1, 'ua_word'] = message.text  # бот вносить українське слово
                    df_user_words.loc[1, 'date'] = 1
                    df_user_words.loc[1, 'week_date'] = 1
                    df_user_words.to_csv(name_file, sep=';', index=False,
                                         encoding='cp1251')  # бот змінює дані в файлі csv
                elif len(df_user_words['ua_word']) > 2:
                    df_user_words.loc[number_row_word, 'ua_word'] = message.text  # бот вносить українське слово
                    df_user_words.to_csv(name_file, sep=';', index=False,
                                         encoding='cp1251')  # бот змінює дані в файлі csv
                just_number = 0

        elif message.text != 'Give me a word' and message.text != 'I want to enlarge my vocabulary' and message.text != "I am lazy. I want to learn your words":
            bot.send_message(message.chat.id, 'Я не знаю що відповісти 😢')

        df = pd.read_csv(name_file, sep=';', encoding='cp1251')
        df3 = pd.read_csv("3000_transcription.csv", sep=';', encoding='UTF-8')
        df_3000 = pd.read_csv('3000_words.csv', sep=';', encoding='cp1251')

        for number in range(len(df['ua_word'])):  # перебираємо, враховуючи к-сть рядків
            flag = False
            count_is_transcription = 0
            time_now, digit, digit_week, digit_month, odds, odds_week, odds_month, level = read_time_data(df,
                                                                                                          number)
            if not digit:  # якщо пусто
                pass
            else:
                if level == 1 and odds < number_seconds_day:  # якщо пройшло менше 1 дня від дати останньої спроби
                    print('Scenario 1')
                # elif level == 2 and odds > number_seconds_day and digit_week == 1 and message.text == 'Give me a word':  # якщо пройшла година, але менше дня
                #     pass

                elif level == 1 and digit == 1 and message.text == 'Give me a word' and len(
                        df_user_words['word']) != 2:  # клієнт вперше бачить слово
                    flag, text_for_callmessage, number_row = send_word(bot, df, number, df_3000, df3, message, level,
                                                                       time_now)
                    break

                elif level == 2 and odds > number_seconds_2_hours and message.text == 'Give me a word' and len(
                        df_user_words['word']) != 2:  # якщо пройшло мінімум 2 години
                    flag, text_for_callmessage, number_row = send_word(bot, df, number, df_3000, df3, message, level,
                                                                       time_now)
                    break

                elif level == 3 and odds > number_seconds_day and message.text == 'Give me a word' and len(
                        df_user_words['word']) != 2:  # якщо пройшло мінімум 1 день і 2 години
                    flag, text_for_callmessage, number_row = send_word(bot, df, number, df_3000, df3, message, level,
                                                                       time_now)
                    break

                elif level == 4 and odds_week > number_seconds_week and digit_month == 1 and message.text == 'Give me a word' and len(
                        df_user_words['word']) != 2:  # якщо пройшов тиждень
                    flag, text_for_callmessage, number_row = send_word(bot, df, number, df_3000, df3, message, level,
                                                                       time_now)
                    break

                elif level == 5 and odds_month > number_seconds_month and message.text == 'Give me a word' and len(
                        df_user_words['word']) != 2:  # якщо пройшов місяць від останнього контакту клієнта зі словом
                    flag, text_for_callmessage, number_row = send_word(bot, df, number, df_3000, df3, message, level,
                                                                       time_now)
                    break

                elif message.text == 'I want to enlarge my vocabulary':
                    bot.send_message(message.chat.id, 'Enter a word in English')
                    flag_new_word, just_number = True, 1
                    break

                elif message.text == "I am lazy. I want to learn your words" and len(df['word']) == 2:
                    df_3000 = pd.read_csv('3000_words.csv', sep=';', encoding='cp1251')
                    bot.send_message(message.chat.id, 'Wait a minute')

                    # df.loc[:len(df_3000['word']) - 1, ['word', 'ua_word', 'date', 'week_date', 'month_date', 'level']] = \
                    #     df_3000.loc[:len(df_3000['word']) - 1,
                    #     ['word', 'ua_word', 'date', 'week_date', 'month_date', 'level']]
                    # df.to_csv(name_file, sep=';', index=False, encoding='cp1251')
                    for value_new in range(len(df_3000['word']) - 1):
                        df.loc[value_new, 'word'] = df_3000.loc[value_new, 'word']
                        df.loc[value_new, 'ua_word'] = df_3000.loc[value_new, 'ua_word']
                        df.loc[value_new, 'date'] = df_3000.loc[value_new, 'date']
                        df.loc[value_new, 'week_date'] = df_3000.loc[value_new, 'week_date']
                        df.loc[value_new, 'month_date'] = df_3000.loc[value_new, 'month_date']
                        df.loc[value_new, 'level'] = df_3000.loc[value_new, 'level']
                        df.to_csv(name_file, sep=';', index=False, encoding='cp1251')  # бот змінює дані в файлі csv
                    # Перевірити індекси. Бо таке враження, ніби при заповненні останній рядок лише перша колонка заповнюється
                    bot.send_message(message.chat.id, 'Job is done')

        if flag == False and message.text == 'Give me a word' and len(df_user_words['word']) > 2:
            bot.send_message(message.chat.id, 'The words for checking are absent')
            digit_sti = random.randint(0, len(stickers_finish) - 1)
            sti_0 = stickers_finish[digit_sti]
            sti = open(sti_0, 'rb')
            bot.send_sticker(message.chat.id, sti)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    global number_row, text_for_callmessage, name_file
    # name_file = 'words_client_' + str(message.chat.id) + '.csv'
    df = pd.read_csv(name_file, sep=';', encoding='cp1251')
    time_now, digit, digit_week, digit_month, odds, odds_week, odds_month, level = read_time_data(df, number_row)

    if call.message:
        # if call.data == 'good':
        #     bot.send_message(call.message.chat.id, "It's great 😊")
        if call.data == 'bad':
            df.loc[number_row, 'level'] = int(int(df.loc[number_row, 'level']) - 1)  # бот зменшує рівень на одиницю
            df.to_csv(name_file, sep=';', index=False, encoding='cp1251')  # бот змінює дані в файлі csv
        elif call.data == 'ok':
            df.loc[number_row, 'level'] = 100  # бот зменшує рівень на одиницю
            df.to_csv(name_file, sep=';', index=False, encoding='cp1251')  # бот змінює дані в файлі csv

        # remove inline buttons
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=text_for_callmessage, reply_markup=None)


# RUN
bot.polling(none_stop=True)
