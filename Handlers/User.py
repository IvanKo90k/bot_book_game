# в тексті 4 реалізувати +1 ВИКОНАНО
# а по тексту врахувати стелю витривалості, тобто коли не можна збільшити витривалість
# схоже наявна проблема, коли користувач програє, він може натиснути на попередній варіант і продовжити гру. Мабуть, треба кожного програшу обнуляти
# рукопашний бій в тексті 3, то треба врахувати правила бою без зброї
# по п. 44 є питання щодо 20 кредитів і 4 пунктів Витривалості
# п. 72 про бій без зброї
# доопрацювати п. 79
# проглянути чи є сенс щось змінювати в п. 81
# п. 89 чи враховано -40 кредитів? ВИКОНАНО
# п. 107 відмінусував в кінці бою 1 майстерності?
# п. 110: подумати над реалізацією списку
# п. 117: подумати над реалізацією списку + є 2 колонки (infrared_scanner_117 і scaner110_117_381)
# п. 124: як взяти меч і чи треба повідомляти про удар хвостом
# п. 134: реалізувати перевірку на те, чи призначена зустріч
# п. 145 визначити, де відбувається вбивство та прописати в коді
# п. 149: що мається на увазі під альтернативою. доопрацювати!
# п. 161: про всяк випадок перевірити коректність виконання
# п. 165: що робимо з мечем стражника? повідомляти про випадкову смерть
# п. 190: подумати над реалізацією Ви можете використовувати Удачу звичайним способом, щоб щоразу зменшувати шкоду на 1 бал
# п. 191: на час вашого перебування тут, ви повинні втратити 1 бал Майстерності, тобто потім потрібно передбачити відновлення того балу
# п. 198: про 366 і 295 залишати в усіх пунктах чи лише в одному?
# п. 207 реалізувати визначення поїв +3 чи не поїв +2
# подумати над 219, можливо зробити картинку + гарно розписати 3 функції (вже є, але треба зробити по суті)
# додати колонку "без зброї", щоб розуміти, як проводиться бій; поруч має бути колонка "зі зброєю"
# п. 234: допрацювати повідомлення, якщо аркадіанець зачепив хвостом
# п. 235: "Якщо у вас було зіткнення з шефом поліції" - нехай гравець сам пам'ятає таке?
# п. 256: уважно перевірити, як функціонує
# п. 270:
# п. 289: до нього був п. 248 (там зменшилася майстерність, потрібно відновити)
# п. 292 видаляти, щоб користувач не міг повернутися і знайти код 110
# п. 295 і 366: потрібно заповнити колонку "366_or_295"
# п. 309: это Дворец Жирдяя, и вы не были здесь раньше, то заплатите 50 кредитов за комнату на ночь.
# п. 312: Если у вас есть альтернатива, можете вернуться на 381 и выбрать снова.
# п. 316: реалізувати викидання одного предмету
# п. 336: звідки береться пара кусачек?
# п. 343: Повстанцы также предлагают вам купить у них за 50 кредитов флакон с зельем
# п. 355: Запишите на лист персонажа все, что вы берете!!! ВИКОНАНО
# п. 376: Все ваше снаряжение, в том числе и меч, отбирают, но они не находят тонкий пояс с деньгами
# п. 377: вы должны вычесть 100 из номера параграфа, на котором находитесь, чтобы перейти на следующий
# п. 396: вычеркните их из списка снаряжения
# обмеження щодо кількості предметів у сумці

import text
from loader import dp, types, bot
import ast
from Data.config import api_token
import asyncio
import logging
import Functions.DB, Functions.Functions
from stickers.stickers import stickers_start, stickers_money, stickers_cute, stickers_thank, stickers_bye, \
    stickers_flight
from States.user import registration
from aiogram.dispatcher import FSMContext
import random
import math
import time

# Set up logging
logging.basicConfig(level=logging.INFO)

word_id = 0
id_for_start = 0
indx = 0
flag_new_word = False
flag_first_client = False
number_row = 0
name_button1, name_button2 = 'Бійка', 'Мир'
user_ask_2 = False
temporary = ''
text_for_callmessage = 'here must be text_for_callmessage'
count_rounds = 0


@dp.message_handler(commands=['start'])
async def start(message: types.Message, state: FSMContext):
    print("Користувач {0.first_name} натиснув start".format(message.from_user))
    await Functions.Functions.send_random_sticker(bot, message.from_user.id, stickers_start)

    # Send another message with the "Go on" button when the user presses it
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Продовжити", callback_data="character_data"))
    await bot.send_message(message.chat.id,
                           'Ласкаво прошу до книги-гри під назвою "Rebel Planet" авторства Robin Waterfield. Деталі можете дізнатися, натиснувши в Меню "довідка".',
                           reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі


@dp.message_handler(commands=['character_data'])
async def character_data(message: types.Message):
    # Retrieve character data for the user
    character_data = Functions.DB.retrieve_character_data(message.chat.id)
    money = Functions.DB.select_one_value(message.chat.id, 'money', 'user_id')

    if character_data:
        mastery, endurance, luck = character_data
        text_message = f"Характеристики вашого персонажа:\nМайстерність: {mastery}\nВитривалість: {endurance}\nУдача: {luck}\nГроші: {money}"
    await bot.send_message(message.chat.id, text_message)


@dp.message_handler(commands=['help'])
async def help(message: types.Message):
    """
        Handle the '/help' command and provide assistance to the user.

        Parameters:
        - message (types.Message): The incoming message object.

        Returns:
        None
        """
    # Create an inline keyboard with a "Продовжити" button
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Продовжити", callback_data="help_continue"))

    # Send a message with information and the inline keyboard
    await bot.send_message(message.chat.id, 'Попереджаю, це може зайняти деякий час. Зате потім буде цікавіше грати 😉',
                           reply_markup=markup)


@dp.callback_query_handler(lambda c: c.data == 'help_continue')
async def process_callback(callback_query: types.CallbackQuery):
    global indx
    user_id = callback_query.from_user.id
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Go on", callback_data="help_continue"))

    texts = [
        text.intro, text.story_1, text.story_2, text.story_3, text.prehistory,
        text.contacts_with_strangers, text.mastery_endurance_luck, text.mastery,
        text.stamina_recovery, text.luck, text.battles, text.fight_without_weapons,
        text.fight_with_multiple_opponents, text.using_luck_in_battles,
        text.equipment_and_money, 'Ось і кінець! Щоб почати гру натисніть в Меню "старт".'
    ]
    print('довжина = ', len(texts), 'індекс', indx)

    if indx < len(texts):
        if indx < 15:
            await bot.send_message(user_id, texts[indx], reply_markup=markup, parse_mode='Markdown')

        elif indx == 15:
            await bot.send_message(user_id, texts[indx])  # 'Ось і кінець! Щоб почати гру натисніть в Меню "старт".')

        indx += 1
        await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == 'character_data')
async def character_data(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    # Call the function to create a character and insert data into the database
    Functions.Functions.create_character_and_insert(user_id, 1)
    Functions.DB.update_one_value(user_id, 'money', 2000)

    # Retrieve character data for the user
    character_data = Functions.DB.retrieve_character_data(user_id)

    if character_data:
        mastery, endurance, luck = character_data
        Functions.DB.update_one_value(user_id, 'max_mastery', mastery)
        Functions.DB.update_one_value(user_id, 'max_endurance', endurance)
        Functions.DB.update_one_value(user_id, 'max_luck', luck)
        response_message = f"Характеристики вашого персонажа:\nМайстерність: {mastery}\nВитривалість: {endurance}\nУдача: {luck}"
        markup = types.InlineKeyboardMarkup(row_width=2)
        item1 = [types.InlineKeyboardButton("Продовжити", callback_data="go_on"),
                 types.InlineKeyboardButton('Змінити', callback_data='change_data')]
        markup.add(*item1)
        await bot.send_message(callback_query.from_user.id, response_message, reply_markup=markup,
                               parse_mode='Markdown', )
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == 'change_data')
async def process_change_data(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.Functions.update_character(user_id)

    # Retrieve character data for the user
    character_data = Functions.DB.retrieve_character_data(user_id)

    markup = types.InlineKeyboardMarkup(row_width=2)
    item1 = [types.InlineKeyboardButton("Продовжити", callback_data="go_on"),
             types.InlineKeyboardButton('Змінити', callback_data='change_data')]
    markup.add(*item1)

    if character_data:
        mastery, endurance, luck = character_data
        Functions.DB.update_one_value(user_id, 'max_mastery', mastery)
        Functions.DB.update_one_value(user_id, 'max_endurance', endurance)
        Functions.DB.update_one_value(user_id, 'max_luck', luck)
        response_message = f"Характеристики вашого персонажа:\nМайстерність: {mastery}\nВитривалість: {endurance}\nУдача: {luck}"
        await bot.send_message(user_id, response_message, reply_markup=markup, parse_mode='Markdown', )
    else:
        await bot.send_message(user_id, "No character data found for you.", reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == 'go_on')
async def go_on(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = [types.InlineKeyboardButton("Наказати комп'ютеру виконати маневр ухилу", callback_data="48"),
             types.InlineKeyboardButton('Продовжити політ', callback_data='398')]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_1, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '2')
async def text_2(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_1_fight(callback_query, 2, 6, 8, "4 rounds", text.text_2)
    # Functions.DB.update_one_value(callback_query.from_user.id, 'text_number', 2)
    # Functions.DB.update_add_enemy(callback_query.from_user.id, 6, 8, 'e_mastery_2', 'e_endurance_2')
    # markup = types.InlineKeyboardMarkup()
    # item1 = [types.InlineKeyboardButton("Почати бійку", callback_data="4 rounds")]
    # markup.add(*item1)
    # await bot.send_message(callback_query.from_user.id, text.text_2, reply_markup=markup, parse_mode='Markdown')
    # await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '4 rounds')
async def text_2_2(callback_query: types.CallbackQuery):
    global count_rounds
    user_id = callback_query.from_user.id
    text_number = Functions.DB.select_one_value(user_id, 'text_number', 'user_id')
    flag24 = Functions.DB.select_one_value(user_id, 'flag24', 'user_id')
    flag113 = Functions.DB.select_one_value(user_id, 'flag113', 'user_id')
    flag172 = Functions.DB.select_one_value(user_id, 'flag172', 'user_id')
    flag234 = Functions.DB.select_one_value(user_id, 'flag234', 'user_id')
    flag244 = Functions.DB.select_one_value(user_id, 'flag244', 'user_id')
    character_data = Functions.DB.retrieve_character_data(user_id)
    character = Functions.Functions.Character(mastery=character_data[0], endurance=character_data[1],
                                              luck=character_data[2])
    if text_number == 2:
        count_rounds += 1
        creature_data = Functions.DB.retrieve_creature_data(user_id, 'e_mastery_2', 'e_endurance_2')
        creature = Functions.Functions.Character(mastery=creature_data[0], endurance=creature_data[1],
                                                 luck=creature_data[2])
        if count_rounds < 5 and creature.endurance > 0:
            print("Initiating battle...")
            await Functions.Functions.battle_for_2(bot, user_id, character, creature)
        elif count_rounds == 5:
            print("Sending victory message...")
            markup = types.InlineKeyboardMarkup()
            item1 = [types.InlineKeyboardButton("34", callback_data="34")]
            markup.add(*item1)
            await bot.send_message(user_id, 'Після чотирьох раундів бою охоронець ще живий — 34.', reply_markup=markup,
                                   parse_mode='Markdown')
    elif text_number in [3, 4, 17, 35, 55, 82, 84, 104, 106, 107, 124, 133, 136, 150, 157, 161, 165, 190, 206, 215,
                         224, 243, 289, 295, 298, 313, 341, 351, 366, 367, 373, 375, 391]:
        text_to_creature_data_mapping = {
            3: ('e_mastery_3', 'e_endurance_3'),
            4: ('e_mastery_4', 'e_endurance_4'),
            17: ('e_mastery_17', 'e_endurance_17'),
            35: ('e_mastery_35', 'e_endurance_35'),
            55: ('e_mastery_55', 'e_endurance_55'),
            82: ('e_mastery_82', 'e_endurance_82'),
            84: ('e_mastery_84', 'e_endurance_84'),
            104: ('e_mastery_104', 'e_endurance_104'),
            106: ('e_mastery_106', 'e_endurance_106'),
            107: ('e_mastery_107', 'e_endurance_107'),
            124: ('e_mastery_124', 'e_endurance_124'),
            133: ('e_mastery_133', 'e_endurance_133'),
            136: ('e_mastery_136', 'e_endurance_136'),
            150: ('e_mastery_150', 'e_endurance_150'),
            157: ('e_mastery_157', 'e_endurance_157'),
            161: ('e_mastery_161', 'e_endurance_161'),
            165: ('e_mastery_165', 'e_endurance_165'),
            190: ('e_mastery_190', 'e_endurance_190'),
            206: ('e_mastery_206', 'e_endurance_206'),
            215: ('e_mastery_215', 'e_endurance_215'),
            224: ('e_mastery_224', 'e_endurance_224'),
            243: ('e_mastery_243', 'e_endurance_243'),
            289: ('e_mastery_289', 'e_endurance_289'),
            295: ('e_mastery_295', 'e_endurance_295'),
            298: ('e_mastery_298', 'e_endurance_298'),
            313: ('e_mastery_313', 'e_endurance_313'),
            341: ('e_mastery_341', 'e_endurance_341'),
            351: ('e_mastery_351', 'e_endurance_351'),
            366: ('e_mastery_366', 'e_endurance_366'),
            367: ('e_mastery_367', 'e_endurance_367'),
            373: ('e_mastery_373', 'e_endurance_373'),
            375: ('e_mastery_375', 'e_endurance_375'),
            391: ('e_mastery_391', 'e_endurance_391'),
        }
        creature_data = Functions.DB.retrieve_creature_data(user_id,
                                                            *text_to_creature_data_mapping.get(text_number, ('', '')))
        creature = Functions.Functions.Character(mastery=creature_data[0], endurance=creature_data[1],
                                                 luck=creature_data[2])
        await Functions.Functions.battle_for_2(bot, user_id, character, creature)

    elif text_number in [24, 113, 172, 234, 244]:
        creature_data = ''
        if text_number == 24 and flag24 in [1, 2]:
            creature_data = Functions.DB.retrieve_creature_data(user_id, f'e_mastery_{text_number}_flag{text_number}',
                                                                f'e_endurance_{text_number}_flag{text_number}')

        elif text_number == 113 and flag113 in [1, 2]:
            creature_data = Functions.DB.retrieve_creature_data(user_id, f'e_mastery_{text_number}_flag{text_number}',
                                                                f'e_endurance_{text_number}_flag{text_number}')

        elif text_number == 172 and flag172 in [1, 2]:
            creature_data = Functions.DB.retrieve_creature_data(user_id, f'e_mastery_{text_number}_flag{text_number}',
                                                                f'e_endurance_{text_number}_flag{text_number}')

        elif text_number == 234 and flag234 in [1, 2]:
            creature_data = Functions.DB.retrieve_creature_data(user_id, f'e_mastery_{text_number}_flag{text_number}',
                                                                f'e_endurance_{text_number}_flag{text_number}')

        elif text_number == 244 and flag244 in [1, 2]:
            creature_data = Functions.DB.retrieve_creature_data(user_id, f'e_mastery_{text_number}_flag{text_number}',
                                                                f'e_endurance_{text_number}_flag{text_number}')
        creature = Functions.Functions.Character(mastery=creature_data[0], endurance=creature_data[1],
                                                 luck=creature_data[2])
        await Functions.Functions.battle_for_2(bot, user_id, character, creature)

    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '3')
async def text_3(callback_query: types.CallbackQuery):
    Functions.DB.update_one_value(callback_query.from_user.id, 'text_number', 3)
    Functions.DB.update_add_enemy(callback_query.from_user.id, 6, 10, 'e_mastery_3', 'e_endurance_3')
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = [types.InlineKeyboardButton("Запропонувати персонального робота-масажиста", callback_data="robot"),
             types.InlineKeyboardButton("Запропонувати 400 кредитів", callback_data="400 credits"),
             types.InlineKeyboardButton("Рукопашний бій", callback_data="fight")]
    markup.add(*item1)
    await bot.send_message(callback_query.from_user.id, text.text_3, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == 'robot')
async def text_3_1(callback_query: types.CallbackQuery):
    markup = types.InlineKeyboardMarkup(row_width=1)
    if Functions.DB.check_column_existence('personal_robot_382'):
        if_is_robot_massage = Functions.DB.select_one_value(callback_query.from_user.id, 'personal_robot_382',
                                                            'user_id')
        if if_is_robot_massage == 1:
            item1 = [types.InlineKeyboardButton("Go on", callback_data="119")]
            markup.add(*item1)
            await bot.send_message(callback_query.from_user.id, "Жирдяй приймає робота-масажиста", reply_markup=markup,
                                   parse_mode='Markdown')
        else:
            item1 = [types.InlineKeyboardButton("Запропонувати 400 кредитів", callback_data="400 credits"),
                     types.InlineKeyboardButton("Рукопашний бій", callback_data="fight")]
            markup.add(*item1)
            await bot.send_message(callback_query.from_user.id, "Схоже, у вас нема робота-масажиста",
                                   reply_markup=markup,
                                   parse_mode='Markdown')
    else:
        item1 = [types.InlineKeyboardButton("Запропонувати 400 кредитів", callback_data="400 credits"),
                 types.InlineKeyboardButton("Рукопашний бій", callback_data="fight")]
        markup.add(*item1)
        await bot.send_message(callback_query.from_user.id, "Схоже, у вас нема робота-масажиста", reply_markup=markup,
                               parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '400 credits')
async def text_3_2(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    money = Functions.DB.select_one_value(user_id, 'money', 'user_id')
    markup = types.InlineKeyboardMarkup()
    if money >= 400:
        money -= 400
        Functions.DB.update_one_value(user_id, 'money', money)
        item1 = [types.InlineKeyboardButton("Продовжити", callback_data="119")]
        markup.add(*item1)
        await bot.send_message(user_id, "Жирдяй приймає гроші і дозволяє скористатися комп'ютером", reply_markup=markup,
                               parse_mode='Markdown')
    else:
        item1 = [types.InlineKeyboardButton("Запропонувати персонального робота-масажиста", callback_data="robot"),
                 types.InlineKeyboardButton("Рукопашний бій", callback_data="fight")]
        markup.add(*item1)
        await bot.send_message(callback_query.from_user.id, "Схоже, у вас нема робота-масажиста", reply_markup=markup,
                               parse_mode='Markdown')
        if Functions.DB.check_column_existence('personal_robot_382'):
            if_is_robot_massage = Functions.DB.select_one_value(callback_query.from_user.id, 'robot_massage_382',
                                                                'user_id')
            if if_is_robot_massage == 1:  # якщо робот є в наявності
                item1 = [
                    types.InlineKeyboardButton("Запропонувати персонального робота-масажиста", callback_data="robot"),
                    types.InlineKeyboardButton("Рукопашний бій", callback_data="fight")]
                markup.add(*item1)
                await bot.send_message(callback_query.from_user.id, "У вас недостатньо коштів",
                                       reply_markup=markup,
                                       parse_mode='Markdown')
            else:
                item1 = [types.InlineKeyboardButton("Рукопашний бій", callback_data="fight")]
                markup.add(*item1)
                await bot.send_message(callback_query.from_user.id, "У вас недостатньо коштів", reply_markup=markup,
                                       parse_mode='Markdown')
        else:
            item1 = [types.InlineKeyboardButton("Рукопашний бій", callback_data="fight")]
            markup.add(*item1)
            await bot.send_message(callback_query.from_user.id, "У вас недостатньо коштів", reply_markup=markup,
                                   parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == 'fight')
async def text_3_3(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id

    # Retrieve necessary data
    text_number = Functions.Functions.select_one_value(user_id, 'text_number', 'user_id')
    flag24 = Functions.Functions.select_one_value(user_id, 'flag24', 'user_id')
    flag113 = Functions.Functions.select_one_value(user_id, 'flag113', 'user_id')
    flag172 = Functions.Functions.select_one_value(user_id, 'flag172', 'user_id')
    flag234 = Functions.Functions.select_one_value(user_id, 'flag234', 'user_id')
    flag244 = Functions.Functions.select_one_value(user_id, 'flag244', 'user_id')
    character_data_outer = Functions.DB.retrieve_character_data(user_id)
    creature_data = None
    valid_text_numbers = {24, 113, 172, 234, 244}

    if text_number in [3, 4, 17, 35, 55, 82, 84, 104, 106, 107, 124, 133, 136, 150, 157, 161, 165, 190, 206, 215, 224,
                       243, 289, 295, 298, 313, 341, 351, 366, 367, 373, 375, 391]:
        # Map text_number to the corresponding creature data
        text_to_creature_data_mapping = {
            3: ('e_mastery_3', 'e_endurance_3'),
            4: ('e_mastery_4', 'e_endurance_4'),
            17: ('e_mastery_17', 'e_endurance_17'),
            35: ('e_mastery_35', 'e_endurance_35'),
            55: ('e_mastery_55', 'e_endurance_55'),
            82: ('e_mastery_82', 'e_endurance_82'),
            84: ('e_mastery_84', 'e_endurance_84'),
            104: ('e_mastery_104', 'e_endurance_104'),
            106: ('e_mastery_106', 'e_endurance_106'),
            107: ('e_mastery_107', 'e_endurance_107'),
            124: ('e_mastery_124', 'e_endurance_124'),
            133: ('e_mastery_133', 'e_endurance_133'),
            136: ('e_mastery_136', 'e_endurance_136'),
            150: ('e_mastery_150', 'e_endurance_150'),
            157: ('e_mastery_157', 'e_endurance_157'),
            161: ('e_mastery_161', 'e_endurance_161'),
            165: ('e_mastery_165', 'e_endurance_165'),
            190: ('e_mastery_190', 'e_endurance_190'),
            206: ('e_mastery_206', 'e_endurance_206'),
            215: ('e_mastery_215', 'e_endurance_215'),
            224: ('e_mastery_224', 'e_endurance_224'),
            243: ('e_mastery_243', 'e_endurance_243'),
            289: ('e_mastery_289', 'e_endurance_289'),
            295: ('e_mastery_295', 'e_endurance_295'),
            298: ('e_mastery_298', 'e_endurance_298'),
            313: ('e_mastery_313', 'e_endurance_313'),
            341: ('e_mastery_341', 'e_endurance_341'),
            351: ('e_mastery_351', 'e_endurance_351'),
            366: ('e_mastery_366', 'e_endurance_366'),
            367: ('e_mastery_367', 'e_endurance_367'),
            373: ('e_mastery_373', 'e_endurance_373'),
            375: ('e_mastery_375', 'e_endurance_375'),
            391: ('e_mastery_391', 'e_endurance_391'),
        }

        creature_data = Functions.DB.retrieve_creature_data(user_id,
                                                            *text_to_creature_data_mapping.get(text_number, ('', '')))

    # elif text_number in valid_text_numbers and f'flag{text_number}' in {1, 2}:
    #     print(234)
    #     creature_data = Functions.Functions.retrieve_creature_data_by_flag(user_id, text_number, f'flag{text_number}')

    elif text_number == 24 and flag24 in {1, 2}:
        creature_data = Functions.Functions.retrieve_creature_data_by_flag(user_id, text_number, flag24)
    elif text_number == 113 and flag113 in {1, 2}:
        creature_data = Functions.Functions.retrieve_creature_data_by_flag(user_id, text_number, flag113)
    elif text_number == 172 and flag172 in {1, 2}:
        creature_data = Functions.Functions.retrieve_creature_data_by_flag(user_id, text_number, flag172)
    elif text_number == 234 and flag234 in {1, 2}:
        creature_data = Functions.Functions.retrieve_creature_data_by_flag(user_id, text_number, flag234)
    elif text_number == 244 and flag244 in {1, 2}:
        creature_data = Functions.Functions.retrieve_creature_data_by_flag(user_id, text_number, flag244)

    if creature_data is not None:
        # Create character and creature objects
        character = Functions.Functions.Character(mastery=character_data_outer[0], endurance=character_data_outer[1],
                                                  luck=character_data_outer[2])
        creature = Functions.Functions.Character(mastery=creature_data[0], endurance=creature_data[1],
                                                 luck=creature_data[2])

        # Perform the battle
        await Functions.Functions.battle_for_2(bot, user_id, character, creature)

    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '4')
async def text_4(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 4)
    endurance = Functions.DB.select_one_value(user_id, 'Endurance', 'user_id')
    max_endurance = Functions.DB.select_one_value(user_id, 'max_endurance', 'user_id')
    if endurance < max_endurance:
        Functions.Functions.change_1_data(user_id, 'Endurance', 'user_id', 1)
    Functions.DB.update_add_enemy(user_id, 5, 6, 'e_mastery_4', 'e_endurance_4')
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("Почати бійку", callback_data="fight")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_4, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '5')
async def text_5(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 5)
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("Зайти в магазин бакалійника", callback_data="grocery"),
             types.InlineKeyboardButton("Рухатися далі", callback_data="204")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_5, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == 'grocery')
async def text_5_1(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.Functions.change_1_data(user_id, 'money', 'user_id', 20, multiplier=-1)
    Functions.Functions.change_1_data(user_id, 'Endurance', 'user_id', 4)
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("Рухатися далі", callback_data="204")]
    markup.add(*item1)
    await bot.send_message(user_id,
                           "Ви витратили 20 кредитів на їжу, за рахунок чого поповнили вашу Витривалість на 4 бали",
                           reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '6')
async def text_6(callback_query: types.CallbackQuery):
    Functions.DB.update_one_value(callback_query.from_user.id, 'text_number', 6)
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = [types.InlineKeyboardButton("Лівий комп'ютер", callback_data="203"),
             types.InlineKeyboardButton("Правий комп'ютер", callback_data="51"),
             types.InlineKeyboardButton("Комп'ютер навпроти дверей", callback_data="139"),
             types.InlineKeyboardButton("Повернутися на 381 для здійснення вибору", callback_data="381")]
    markup.add(*item1)
    await bot.send_message(callback_query.from_user.id, text.text_6, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '7')
async def text_7(callback_query: types.CallbackQuery):
    Functions.DB.update_one_value(callback_query.from_user.id, 'text_number', 7)
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = [types.InlineKeyboardButton("Піти головними вулицями", callback_data="132"),
             types.InlineKeyboardButton("Побігти назад вздовж провулка", callback_data="303")]
    markup.add(*item1)
    await bot.send_message(callback_query.from_user.id, text.text_7, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '8')
async def text_8(callback_query: types.CallbackQuery):
    Functions.DB.update_one_value(callback_query.from_user.id, 'text_number', 8)
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("Повернутись", callback_data="384"),
             types.InlineKeyboardButton("Продовжити йти прямо", callback_data="23")]
    markup.add(*item1)
    await bot.send_message(callback_query.from_user.id, text.text_8, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '9')
async def text_9(callback_query: types.CallbackQuery):
    Functions.DB.update_one_value(callback_query.from_user.id, 'text_number', 9)
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = [types.InlineKeyboardButton("Залишитись та обшукати будинок", callback_data="117"),
             types.InlineKeyboardButton('Вийти, щоб знайти "Вщент"', callback_data="132")]
    markup.add(*item1)
    await bot.send_message(callback_query.from_user.id, text.text_9, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '10')
async def text_10(callback_query: types.CallbackQuery):
    Functions.DB.update_one_value(callback_query.from_user.id, 'text_number', 10)
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("Винести з собою посох", callback_data="49"),
             types.InlineKeyboardButton('147', callback_data="147")]
    markup.add(*item1)
    await bot.send_message(callback_query.from_user.id, text.text_10, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '11')
async def text_11(callback_query: types.CallbackQuery):
    Functions.DB.update_one_value(callback_query.from_user.id, 'text_number', 11)
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("Довіритися Мехіті", callback_data="97"),
             types.InlineKeyboardButton('Не довіритися Мехіті', callback_data="202")]
    markup.add(*item1)
    await bot.send_message(callback_query.from_user.id, text.text_11, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '12')
async def text_12(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 12)
    Functions.Functions.change_1_data(user_id, 'money', 'user_id', 55)
    Functions.DB.update_one_value(user_id, 'food_briquette_12', 1)
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = [types.InlineKeyboardButton("Битися з ними", callback_data="80"),
             types.InlineKeyboardButton('Дозволити їм супроводжувати вас всередину', callback_data="145")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_12, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '13')
async def text_13(callback_query: types.CallbackQuery):
    Functions.DB.update_one_value(callback_query.from_user.id, 'text_number', 13)
    markup = types.InlineKeyboardMarkup()
    result = random.randint(1, 6)

    # Check if the result is even or odd
    if result % 2 == 0:
        item1 = [types.InlineKeyboardButton('Go on', callback_data="140")]  # Even number
    else:
        item1 = [types.InlineKeyboardButton('Go on', callback_data="67")]  # Odd number

    markup.add(*item1)
    await bot.send_message(callback_query.from_user.id, text.text_13, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '14')
async def text_14(callback_query: types.CallbackQuery):
    Functions.DB.update_one_value(callback_query.from_user.id, 'text_number', 14)
    Functions.DB.update_one_value(callback_query.from_user.id, 'rat_bite', 1)
    markup = types.InlineKeyboardMarkup()
    result = random.randint(1, 6)

    # Check if the result is even or odd
    if result % 2 == 0:
        item1 = [types.InlineKeyboardButton('Go on', callback_data="92")]  # Even number
    else:
        item1 = [types.InlineKeyboardButton('Go on', callback_data="331")]  # Odd number

    markup.add(*item1)
    await bot.send_message(callback_query.from_user.id, text.text_14, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '15')
async def text_15(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_move(callback_query, 15, "66", text.text_15)
    # user_id = callback_query.from_user.id
    # Functions.DB.update_one_value(user_id, 'text_number', 15)
    # markup = types.InlineKeyboardMarkup()
    # item1 = [types.InlineKeyboardButton('Go on', callback_data="66")]
    # markup.add(*item1)
    # await bot.send_message(user_id, text.text_15, reply_markup=markup, parse_mode='Markdown')
    # await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '16')
async def text_16(callback_query: types.CallbackQuery):
    Functions.DB.update_one_value(callback_query.from_user.id, 'text_number', 16)

    character_data = Functions.DB.retrieve_character_data(callback_query.from_user.id)
    character = Functions.Functions.Character(mastery=character_data[0], endurance=character_data[1],
                                              luck=character_data[2])
    result = Functions.Functions.roll_dice_2()
    print(result)
    markup = types.InlineKeyboardMarkup()
    if result <= character.luck:
        item1 = [types.InlineKeyboardButton('Go on', callback_data="367")]
    else:
        item1 = [types.InlineKeyboardButton('Go on', callback_data="224")]
    character.luck -= 1
    Functions.DB.update_one_value(callback_query.from_user.id, 'Luck', character.luck)
    markup.add(*item1)
    await bot.send_message(callback_query.from_user.id, text.text_16, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '17')
async def text_17(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_1_fight(callback_query, 17, 7, 10, "fight", text.text_17)
    # user_id = callback_query.from_user.id
    # Functions.DB.update_one_value(user_id, 'text_number', 17)
    # Functions.DB.update_add_enemy(user_id, 7, 10, 'e_mastery_17', 'e_endurance_17')
    # markup = types.InlineKeyboardMarkup()
    # item1 = [types.InlineKeyboardButton("Почати бійку", callback_data="fight")]
    # markup.add(*item1)
    # await bot.send_message(user_id, text.text_17, reply_markup=markup, parse_mode='Markdown')
    # await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '18')
async def text_18(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 18)
    character_endurance = Functions.DB.select_one_value(callback_query.from_user.id, 'Endurance', 'user_id')
    character_endurance += 1
    Functions.DB.update_one_value(callback_query.from_user.id, 'Endurance', character_endurance)
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("Піти направо", callback_data="296"),
             types.InlineKeyboardButton("Піти наліво", callback_data="171")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_18, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '19')
async def text_19(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 19)
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("Запитати у сторожа, що знаходиться за іншими дверима", callback_data="380"),
             types.InlineKeyboardButton("Піти в університет", callback_data="146")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_19, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '20')
async def text_20(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_move(callback_query, 20, "247", text.text_20)
    # user_id = callback_query.from_user.id
    # Functions.DB.update_one_value(user_id, 'text_number', 20)
    # markup = types.InlineKeyboardMarkup()
    # item1 = [types.InlineKeyboardButton("Go on", callback_data="247")]
    # markup.add(*item1)
    # await bot.send_message(user_id, text.text_20, reply_markup=markup, parse_mode='Markdown')
    # await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '21')
async def text_21(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(callback_query.from_user.id, 'text_number', 21)

    # markup = types.InlineKeyboardMarkup()
    # if Functions.DB.check_column_existence('klaxon'):
    #     if_is_klaxon = Functions.DB.select_one_value(callback_query.from_user.id, 'klaxon', 'user_id')
    #     if if_is_klaxon == 1:
    #         item1 = [types.InlineKeyboardButton("Go on", callback_data="366"),
    #                  types.InlineKeyboardButton("Go on", callback_data="295")]
    #         markup.add(*item1)
    #         await bot.send_message(callback_query.from_user.id, text.text_21, reply_markup=markup,
    #                                parse_mode='Markdown')
    #         Functions.DB.update_one_value(callback_query.from_user.id, 'klaxon', 0)
    #     else:
    #         item1 = [types.InlineKeyboardButton("Go on", callback_data="366"),
    #                  types.InlineKeyboardButton("Go on", callback_data="295")]
    #         markup.add(*item1)
    #         await bot.send_message(callback_query.from_user.id, "Схоже, у вас нема ручного клаксона.",
    #                                reply_markup=markup, parse_mode='Markdown')
    # else:
    #     item1 = [types.InlineKeyboardButton("Go on", callback_data="366"),
    #              types.InlineKeyboardButton("Go on", callback_data="295")]
    #     markup.add(*item1)
    #     await bot.send_message(callback_query.from_user.id, "Схоже, у вас нема ручного клаксона.", reply_markup=markup,
    #                            parse_mode='Markdown')
    # await callback_query.answer()

    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("366", callback_data="366"),
             types.InlineKeyboardButton("295", callback_data="295")]
    markup.add(*item1)
    await bot.send_message(callback_query.from_user.id, text.text_21, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '22')
async def text_22(callback_query: types.CallbackQuery):
    Functions.DB.update_one_value(callback_query.from_user.id, 'text_number', 22)
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("Залишитися на місці", callback_data="53"),
             types.InlineKeyboardButton("Спробувати прорватися", callback_data="216")]
    markup.add(*item1)
    await bot.send_message(callback_query.from_user.id, text.text_22, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '23')
async def text_23(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_game_over(callback_query, 23, text.text_23)


@dp.callback_query_handler(lambda c: c.data == '24')
async def text_24(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 24)
    Functions.DB.update_add_enemy(user_id, 7, 8, 'e_mastery_24_1', 'e_endurance_24_1')
    Functions.DB.update_add_enemy(user_id, 6, 6, 'e_mastery_24_2', 'e_endurance_24_2')
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("Перший аркадіанець", callback_data="first_a"),
             types.InlineKeyboardButton("Другий аркадіанець", callback_data="second_a")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_24, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == 'first_a')
async def text_24_1(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'flag24', 1)
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("До бою", callback_data="fight")]
    markup.add(*item1)
    await bot.send_message(user_id, "Ти обираєш битися з першим аркадіанцем", reply_markup=markup,
                           parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == 'second_a')
async def text_24_2(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'flag24', 2)
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("До бою", callback_data="fight")]
    markup.add(*item1)
    await bot.send_message(user_id, "Ти обираєш битися з другим аркадіанцем", reply_markup=markup,
                           parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '25')
async def text_25(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 25)
    Functions.Functions.change_1_data(user_id, 'Endurance', 'user_id', 2)
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("Go on", callback_data="213")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_25, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '26')
async def text_26(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_game_over(callback_query, 26, text.text_26)


@dp.callback_query_handler(lambda c: c.data == '27')
async def text_27(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_game_over(callback_query, 27, text.text_27)


@dp.callback_query_handler(lambda c: c.data == '28')
async def text_28(callback_query: types.CallbackQuery):
    Functions.DB.update_one_value(callback_query.from_user.id, 'text_number', 28)
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("Запитати, що відбувається", callback_data="353"),
             types.InlineKeyboardButton("Промовчати", callback_data="321")]
    markup.add(*item1)
    await bot.send_message(callback_query.from_user.id, text.text_28, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '29')
async def text_29(callback_query: types.CallbackQuery):
    Functions.DB.update_one_value(callback_query.from_user.id, 'text_number', 29)
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = [types.InlineKeyboardButton("Постаратися зав'язати розмову", callback_data="354"),
             types.InlineKeyboardButton("Влаштуватися подалі від нього", callback_data="60")]
    markup.add(*item1)
    await bot.send_message(callback_query.from_user.id, text.text_29, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '30')
async def text_30(callback_query: types.CallbackQuery):
    Functions.DB.update_one_value(callback_query.from_user.id, 'text_number', 30)
    markup = types.InlineKeyboardMarkup(row_width=3)
    item1 = [types.InlineKeyboardButton("На схід", callback_data="245"),
             types.InlineKeyboardButton("На північ", callback_data="342"),
             types.InlineKeyboardButton("На південь", callback_data="181")]
    markup.add(*item1)
    await bot.send_message(callback_query.from_user.id, text.text_30, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '31')
async def text_31(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_move(callback_query, 31, "119", text.text_31)
    # user_id = callback_query.from_user.id
    # Functions.DB.update_one_value(user_id, 'text_number', 31)
    # markup = types.InlineKeyboardMarkup()
    # item1 = [types.InlineKeyboardButton("Go on", callback_data="119")]
    # markup.add(*item1)
    # await bot.send_message(user_id, text.text_31, reply_markup=markup, parse_mode='Markdown')
    # await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '32')
async def text_32(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 32)
    Functions.Functions.change_1_data(user_id, 'Endurance', 'user_id', 4)
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("Go on", callback_data="292")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_32, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '33')
async def text_33(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 33)
    rope = Functions.DB.select_one_value(user_id, 'skein_of_nylon_rope_382', 'user_id')
    # scaner = Functions.DB.select_one_value(user_id, 'scaner110_117_381', 'user_id')
    scaner = Functions.DB.select_one_value(user_id, 'scanner_110_117', 'user_id')
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("Продовжити", callback_data="210")]
    if rope == 1 or scaner == 1:
        item1 = [types.InlineKeyboardButton("Продовжити", callback_data="339")]
    elif rope != 1 and scaner != 1:
        item1 = [types.InlineKeyboardButton("Продовжити", callback_data="374")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_33, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '34')
async def text_34(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_game_over(callback_query, 34, text.text_34)


@dp.callback_query_handler(lambda c: c.data == '35')
async def text_35(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 35)
    Functions.DB.update_add_enemy(user_id, 7, 12, 'e_mastery_35', 'e_endurance_35')
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("Випробувати Удачу", callback_data="luck_35")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_35, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == 'luck_35')
async def text_35_1(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    luck = Functions.DB.select_one_value(user_id, 'Luck', 'user_id')
    mastery_creature = Functions.DB.select_one_value(user_id, 'e_mastery_35', 'user_id')
    text_35_1 = 'Не пощастило. В будь-якому випадку до бою!'

    if luck > 0:
        result = Functions.Functions.roll_dice_2()
        if result <= luck:  # якщо пощастило
            mastery_creature -= 1
            Functions.DB.update_one_value(user_id, 'e_mastery_35', mastery_creature)
            text_35_1 = 'Вам пощастило, частина наркотику, який був у напої, потрапила до рота вашого опонента, і в результаті його Майстерність зменшується на 1 пункт'
        Functions.Functions.change_1_data(user_id, 'Luck', 'user_id', 1, multiplier=-1)
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("Почати бійку", callback_data="fight")]
    markup.add(*item1)
    await bot.send_message(user_id, text_35_1, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '36')
async def text_36(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_game_over(callback_query, 36, text.text_36)


@dp.callback_query_handler(lambda c: c.data == '37')
async def text_37(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 37)
    Functions.Functions.change_1_data(user_id, 'money', 'user_id', 10, multiplier=-1)
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("Піти за нею", callback_data="75"),
             types.InlineKeyboardButton("Побути тут ще трохи", callback_data="81")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_37, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '38')
async def text_38(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 38)
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = [types.InlineKeyboardButton("Піти з ним", callback_data="399"),
             types.InlineKeyboardButton("Залишити його і спробувати знайти меч", callback_data="137")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_38, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '39')
async def text_39(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 39)
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("Повернути на північ", callback_data="277"),
             types.InlineKeyboardButton("Йти прямо", callback_data="23")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_39, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '40')
async def text_40(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 40)
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = [types.InlineKeyboardButton("Спробувати пролізти в ліву ущелину", callback_data="14"),
             types.InlineKeyboardButton("Спробувати пролізти в праву ущелину", callback_data="355"),
             types.InlineKeyboardButton("Не ризикувати більше і повернутися на стежку", callback_data="147")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_40, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '41')
async def text_41(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_move(callback_query, 41, "207", text.text_41)
    # user_id = callback_query.from_user.id
    # Functions.DB.update_one_value(user_id, 'text_number', 41)
    # markup = types.InlineKeyboardMarkup()
    # item1 = [types.InlineKeyboardButton("Go on", callback_data="207")]
    # markup.add(*item1)
    # await bot.send_message(user_id, text.text_41, reply_markup=markup, parse_mode='Markdown')
    # await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '42')
async def text_42(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_game_over(callback_query, 42, text.text_42)


@dp.callback_query_handler(lambda c: c.data == '43')
async def text_43(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(callback_query.from_user.id, 'text_number', 43)
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("Дати інформацію", callback_data="345"),
             types.InlineKeyboardButton("Не давати інформацію", callback_data="368")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_43, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '44')
async def text_44(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id

    # Update text_number to 44
    Functions.DB.update_one_value(user_id, 'text_number', 44)

    # Update Luck
    Functions.Functions.change_1_data(user_id, 'Luck', 'user_id', 1, multiplier=-1)

    # Check if money382 is not empty
    if Functions.DB.is_cell_not_empty(user_id, 'money382'):
        money = Functions.DB.select_one_value(user_id, 'money', 'user_id')
        money382 = Functions.DB.select_one_value(user_id, 'money382', 'user_id')

        # Deduct money382 * 0.5 from money
        Functions.DB.update_one_value(user_id, 'money', money - money382 * 0.5)

    check_152 = Functions.DB.select_one_value(user_id, 'check_152', 'user_id')
    if check_152:  # якщо був раніше в бакалійника
        text_message = text.text_44_1
    else:
        text_message = text.text_44_2
        Functions.Functions.change_1_data(user_id, 'money', 'user_id', 20, multiplier=-1)
        Functions.Functions.change_1_data(user_id, 'Endurance', 'user_id', 4)

    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("Go on", callback_data="204")]
    markup.add(*item1)
    await bot.send_message(user_id, text_message, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '45')
async def text_45(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 45)
    sword = Functions.DB.select_one_value(user_id, 'sword', 'user_id')
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("Відійти від клубу", callback_data="390")]
    if sword == 1:
        item1 = [types.InlineKeyboardButton("Відійти від клубу", callback_data="390"),
                 types.InlineKeyboardButton("Спробувати розрубати замок на дверях своїм мечем", callback_data="366")]
        markup.add(*item1)
        await bot.send_message(user_id, text.text_45, reply_markup=markup, parse_mode='Markdown')
    else:
        markup.add(*item1)
        await bot.send_message(user_id,
                               '"Я не знаю, в які ігри ви граєте, — каже брамник крізь отвір, — але вам тут не раді". Він закриває віконце.',
                               reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '46')
async def text_46(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 46)
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("Відправити в бій Дорадо", callback_data="175"),
             types.InlineKeyboardButton("Відправити в бій Мізара", callback_data="255")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_46, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '47')
async def text_47(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 47)
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = [types.InlineKeyboardButton("Зупинитись в Зодіаку", callback_data="89"),
             types.InlineKeyboardButton("Зупинитись у Палаці Жирдяя", callback_data="101")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_47, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '48')
async def text_48(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_move(callback_query, 48, "164", text.text_48)
    # user_id = callback_query.from_user.id
    # Functions.DB.update_one_value(user_id, 'text_number', 48)
    # markup = types.InlineKeyboardMarkup()
    # item1 = [types.InlineKeyboardButton("Продовжити", callback_data="164")]
    # markup.add(*item1)
    # await bot.send_message(user_id, text.text_48, reply_markup=markup, parse_mode='Markdown')
    # await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '49')
async def text_49(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id

    # Update text_number to 49
    Functions.DB.update_one_value(user_id, 'text_number', 49)

    # Create InlineKeyboardMarkup
    markup = types.InlineKeyboardMarkup()

    if Functions.DB.is_cell_not_empty(user_id, 'rat_bite'):
        item1 = [types.InlineKeyboardButton("Go on", callback_data="98")]
    else:
        item1 = [types.InlineKeyboardButton("Go on", callback_data="232")]

    markup.add(*item1)

    # Send the message
    await bot.send_message(callback_query.from_user.id, text.text_49, reply_markup=markup, parse_mode='Markdown')

    # Answer the callback query
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '50')
async def text_50(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 50)
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("Відправитися в університет", callback_data="146")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_50, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '51')
async def text_51(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_move(callback_query, 51, "177", text.text_51)
    # user_id = callback_query.from_user.id
    # Functions.DB.update_one_value(user_id, 'text_number', 51)
    # markup = types.InlineKeyboardMarkup()
    # item1 = [types.InlineKeyboardButton("Перейти до 177", callback_data="177")]
    # markup.add(*item1)
    # await bot.send_message(user_id, text.text_51, reply_markup=markup, parse_mode='Markdown')
    # await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '52')
async def text_52(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_game_over(callback_query, 52, text.text_52)


@dp.callback_query_handler(lambda c: c.data == '53')
async def text_53(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_game_over(callback_query, 53, text.text_53)


@dp.callback_query_handler(lambda c: c.data == '54')
async def text_54(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 54)
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("Повернутися на свій корабель", callback_data="191")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_54, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '55')
async def text_55(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_1_fight(callback_query, 55, 8, 8, "fight", text.text_55)
    # user_id = callback_query.from_user.id
    # Functions.DB.update_one_value(user_id, 'text_number', 55)
    # Functions.DB.update_add_enemy(user_id, 8, 8, 'e_mastery_55', 'e_endurance_55')
    # markup = types.InlineKeyboardMarkup()
    # item1 = [types.InlineKeyboardButton("Почати бійку", callback_data="fight")]
    # markup.add(*item1)
    # await bot.send_message(user_id, text.text_55, reply_markup=markup, parse_mode='Markdown')
    # await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '56')
async def text_56(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 56)
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = [types.InlineKeyboardButton("Прийняти безнадійний бій", callback_data="264"),
             types.InlineKeyboardButton("Стукати у двері", callback_data="364"),
             types.InlineKeyboardButton("Спробувати увійти в дім навпроти", callback_data="121")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_56, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '57')
async def text_57(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 57)
    character_data = Functions.DB.retrieve_character_data(user_id)
    character = Functions.Functions.Character(mastery=character_data[0], endurance=character_data[1],
                                              luck=character_data[2])
    if character.luck > 0:
        markup = types.InlineKeyboardMarkup()
        item1 = [types.InlineKeyboardButton('Перевірити Удачу', callback_data='359')]
        if not Functions.Functions.if_luck(character.luck):  # якщо не пощастило
            item1 = [types.InlineKeyboardButton('Перевірити Удачу', callback_data='304')]
        markup.add(*item1)
        Functions.Functions.change_1_data(user_id, 'Luck', 'user_id', 1, multiplier=-1)
    await bot.send_message(user_id, text.text_57, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '58')
async def text_58(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 58)
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton('Піти на Науковий поверх', callback_data='266'),
             types.InlineKeyboardButton('Покинути університет', callback_data='235')]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_58, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '59')
async def text_59(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_move(callback_query, 59, "118", text.text_59)
    # user_id = callback_query.from_user.id
    # Functions.DB.update_one_value(user_id, 'text_number', 59)
    # markup = types.InlineKeyboardMarkup()
    # item1 = [types.InlineKeyboardButton('Go on', callback_data='118')]
    # markup.add(*item1)
    # await bot.send_message(user_id, text.text_59, reply_markup=markup, parse_mode='Markdown')
    # await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '60')
async def text_60(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(callback_query.from_user.id, 'text_number', 60)
    Functions.Functions.change_1_data(user_id, 'Luck', 'user_id', 1, multiplier=-1)
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("Go on", callback_data="99")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_60, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '61')
async def text_61(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 61)
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = [types.InlineKeyboardButton("Видалити кожух комп'ютера", callback_data='325'),
             types.InlineKeyboardButton('Повернутися і зробити інший вибір', callback_data='381')]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_61, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '62')
async def text_62(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 62)
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("Відправитися на південь", callback_data='154'),
             types.InlineKeyboardButton('Відправитися на північ', callback_data='23')]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_62, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '63')
async def text_63(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 63)
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("Повернутися до свого готелю", callback_data='309')]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_63, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '64')
async def text_64(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 64)
    Functions.Functions.change_1_data(user_id, 'money', 'user_id', 10, multiplier=-1)
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("Приєднатися до групи людей", callback_data='305')]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_64, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '65')
async def text_65(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 65)
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("Сказати, щоб поквапився", callback_data='241'),
             types.InlineKeyboardButton('Бути терплячим', callback_data='32')]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_65, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '66')
async def text_66(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 66)
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("Переглянути їх тут", callback_data='174'),
             types.InlineKeyboardButton('Забрати із собою', callback_data='316')]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_66, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '67')
async def text_67(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_move(callback_query, 67, "156", text.text_67)
    # user_id = callback_query.from_user.id
    # Functions.DB.update_one_value(user_id, 'text_number', 67)
    # markup = types.InlineKeyboardMarkup()
    # item1 = [types.InlineKeyboardButton("Go on", callback_data='156')]
    # markup.add(*item1)
    # await bot.send_message(user_id, text.text_67, reply_markup=markup, parse_mode='Markdown')
    # await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '68')
async def text_68(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_game_over(callback_query, 68, text.text_68)


@dp.callback_query_handler(lambda c: c.data == '69')
async def text_69(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 69)
    Functions.Functions.change_1_data(user_id, 'Endurance', 'user_id', 2, multiplier=-1)
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("Go on", callback_data='116')]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_69, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '70')
async def text_70(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 70)
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = [types.InlineKeyboardButton("Одразу увійти всередину", callback_data='146'),
             types.InlineKeyboardButton('Зачекати деякий час зовні', callback_data='178')]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_70, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '71')
async def text_71(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 71)
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = [types.InlineKeyboardButton("Спробувати зламати двері", callback_data='360'),
             types.InlineKeyboardButton('Зачекати, чи не станеться чогось', callback_data='301')]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_71, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '72')
async def text_72(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 72)
    Functions.DB.update_one_value(user_id, 'sword', 0)
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = [types.InlineKeyboardButton("Спробувати зламати двері", callback_data='360')]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_72, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '73')
async def text_73(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 73)
    Functions.Functions.change_1_data(user_id, 'Endurance', 'user_id', 4)
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("Вирушити праворуч", callback_data='296'),
             types.InlineKeyboardButton('Вирушити ліворуч', callback_data='171')]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_73, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '74')
async def text_74(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 74)
    Functions.Functions.change_1_data(user_id, 'Luck', 'user_id', 1)
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = [types.InlineKeyboardButton("Go on", callback_data='134')]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_74, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '75')
async def text_75(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 75)
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("Повернутися в клуб", callback_data='45'),
             types.InlineKeyboardButton('Продовжити пошуки', callback_data='13')]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_75, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '76')
async def text_76(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 76)
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = [types.InlineKeyboardButton("Трохи зачекати", callback_data='244'),
             types.InlineKeyboardButton("Зійти на Науковий поверх", callback_data='266'),
             types.InlineKeyboardButton('Покинути університет', callback_data='235')]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_76, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '77')
async def text_77(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 77)
    Functions.Functions.change_1_data(user_id, 'Luck', 'user_id', 1)
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("Відразу увійти", callback_data='146'),
             types.InlineKeyboardButton('Зачекати деякий час зовні', callback_data='178')]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_77, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '78')
async def text_78(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 78)
    endurance = Functions.DB.select_one_value(user_id, 'Endurance', 'user_id')
    Functions.DB.update_one_value(user_id, 'Endurance', endurance + math.ceil(endurance / 2))
    Functions.Functions.change_1_data(user_id, 'Mastery', 'user_id', 1)
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("Запитати, хто це", callback_data='20'),
             types.InlineKeyboardButton('Одразу відчинити двері', callback_data='350')]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_78, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '79')
async def text_79(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 79)
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("Повернутися до місця битви", callback_data='295'),
             types.InlineKeyboardButton('366', callback_data='366')]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_79, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '80')
async def text_80(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_game_over(callback_query, 80, text.text_80)


@dp.callback_query_handler(lambda c: c.data == '81')
async def text_81(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 81)
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("Так", callback_data='362'),
             types.InlineKeyboardButton('Ні', callback_data='311')]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_81, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '82')
async def text_82(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_1_fight(callback_query, 82, 7, 8, "fight", text.text_82)
    # user_id = callback_query.from_user.id
    # Functions.DB.update_one_value(user_id, 'text_number', 82)
    # Functions.DB.update_add_enemy(user_id, 7, 8, 'e_mastery_82', 'e_endurance_82')
    # markup = types.InlineKeyboardMarkup()
    # item1 = [types.InlineKeyboardButton("Почати бійку", callback_data="fight")]
    # markup.add(*item1)
    # await bot.send_message(callback_query.from_user.id, text.text_82, reply_markup=markup, parse_mode='Markdown')
    # await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '83')
async def text_83(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_game_over(callback_query, 83, text.text_83)


@dp.callback_query_handler(lambda c: c.data == '84')
async def text_84(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_1_fight(callback_query, 84, 6, 10, "fight", text.text_84)
    # user_id = callback_query.from_user.id
    # Functions.DB.update_one_value(user_id, 'text_number', 84)
    # Functions.DB.update_add_enemy(user_id, 6, 10, 'e_mastery_84', 'e_endurance_84')
    # markup = types.InlineKeyboardMarkup()
    # item1 = [types.InlineKeyboardButton("Почати бійку", callback_data="fight")]
    # markup.add(*item1)
    # await bot.send_message(callback_query.from_user.id, text.text_84, reply_markup=markup, parse_mode='Markdown')
    # await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '85')
async def text_85(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 85)
    Functions.Functions.change_1_data(user_id, 'Endurance', 'user_id', 2, multiplier=-1)
    Functions.Functions.change_1_data(user_id, 'Mastery', 'user_id', 1, multiplier=-1)
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("Go on", callback_data='215')]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_85, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '86')
async def text_86(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_move(callback_query, 86, "381", text.text_86)
    # user_id = callback_query.from_user.id
    # Functions.DB.update_one_value(user_id, 'text_number', 86)
    # markup = types.InlineKeyboardMarkup()
    # item1 = [types.InlineKeyboardButton("Go on", callback_data='381')]
    # markup.add(*item1)
    # await bot.send_message(user_id, text.text_86, reply_markup=markup, parse_mode='Markdown')
    # await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '87')
async def text_87(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_move(callback_query, 87, "276", text.text_87)
    # user_id = callback_query.from_user.id
    # Functions.DB.update_one_value(user_id, 'text_number', 87)
    # markup = types.InlineKeyboardMarkup()
    # item1 = [types.InlineKeyboardButton("Go on", callback_data='276')]
    # markup.add(*item1)
    # await bot.send_message(user_id, text.text_87, reply_markup=markup, parse_mode='Markdown')
    # await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '88')
async def text_88(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_game_over(callback_query, 88, text.text_88)


@dp.callback_query_handler(lambda c: c.data == '89')
async def text_89(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 89)
    Functions.Functions.change_1_data(user_id, 'Endurance', 'user_id', 1)
    Functions.Functions.change_1_data(user_id, 'money', 'user_id', 375, multiplier=-1)
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("Поїсти або в барі", callback_data='115'),
             types.InlineKeyboardButton("Пообідати в ресторані", callback_data='138')]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_89, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '90')
async def text_90(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 90)
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = [types.InlineKeyboardButton("Спробувати відібрати у нього зброю", callback_data='59'),
             types.InlineKeyboardButton('Продовжити вмовляння', callback_data='130')]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_90, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '91')
async def text_91(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 91)
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = [types.InlineKeyboardButton("Сказати, що це все, що у вас є", callback_data='223'),
             types.InlineKeyboardButton('Спробувати ще поторгуватися', callback_data='148')]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_91, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '92')
async def text_92(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 92)
    Functions.Functions.change_1_data(user_id, 'Endurance', 'user_id', 2, multiplier=-1)
    Functions.Functions.change_1_data(user_id, 'Mastery', 'user_id', 1, multiplier=-1)
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = [types.InlineKeyboardButton("Дослідити іншу ущелину", callback_data='355'),
             types.InlineKeyboardButton('Вважаю, що настав час продовжити подорож', callback_data='10')]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_92, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '93')
async def text_93(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 93)
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("Так", callback_data='248'),
             types.InlineKeyboardButton('Ні', callback_data='70')]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_93, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '94')
async def text_94(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 94)
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = [types.InlineKeyboardButton("Наказати йому звільнити вас", callback_data='65'),
             types.InlineKeyboardButton('Дочекатися, щоб повз пройшов робот', callback_data='278')]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_94, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '95')
async def text_95(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 95)
    Functions.Functions.change_1_data(user_id, 'Luck', 'user_id', 1, multiplier=-1)
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = [types.InlineKeyboardButton("Чинити опір", callback_data='156'),
             types.InlineKeyboardButton('Занадто пригнічений, щоб турбуватися через напад', callback_data='272')]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_95, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '96')
async def text_96(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 96)
    Functions.Functions.change_1_data(user_id, 'money', 'user_id', 200, multiplier=-1)
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = [types.InlineKeyboardButton("Go on", callback_data='84')]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_96, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '97')
async def text_97(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 97)
    Functions.Functions.change_1_data(user_id, 'Luck', 'user_id', 1)
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = [types.InlineKeyboardButton("Піти нагору", callback_data='258'),
             types.InlineKeyboardButton('Залишити університет', callback_data='235')]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_97, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '98')
async def text_98(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 98)
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = [types.InlineKeyboardButton("Перевірити Удачу", callback_data='check_luck_98')]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_98, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == 'check_luck_98')
async def text_98_1(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id

    # Retrieve Luck value
    luck = Functions.DB.select_one_value(user_id, 'Luck', 'user_id')

    if luck > 0:
        result = Functions.Functions.roll_dice_2()
        if result <= luck:  # good luck
            Functions.Functions.change_1_data(user_id, 'Endurance', 'user_id', 2, multiplier=-1)
            markup = types.InlineKeyboardMarkup()
            item1 = [types.InlineKeyboardButton('Go on', callback_data='147')]
            markup.add(*item1)
            await bot.send_message(user_id,
                                   f"Ви падаєте на останній ділянці спуску і втрачаєте 2 бали Витривалості, крім того ламається кінець у палиці. Потім ви продовжуєте подорож.",
                                   reply_markup=markup)
        else:
            await bot.send_message(user_id, f"Ви падаєте з великої висоти і розбиваєтеся")
        Functions.DB.update_one_value(user_id, 'Luck', luck - 1)
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '99')
async def text_99(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 99)
    Functions.Functions.change_1_data(user_id, 'Endurance', 'user_id', 2, multiplier=-1)
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = [types.InlineKeyboardButton("Зайти в бакалею", callback_data="152"),
             types.InlineKeyboardButton("Зайти в магазин обладнання", callback_data="382")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_99, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '100')
async def text_100(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(callback_query.from_user.id, 'text_number', 100)
    food_briquette = Functions.DB.select_one_value(user_id, 'food_briquette_12', 'user_id')
    markup = types.InlineKeyboardMarkup()
    if food_briquette == 1:
        item1 = [types.InlineKeyboardButton("У вас є харчовий брикет", callback_data="73")]
    else:
        item1 = [types.InlineKeyboardButton("У вас нема харчового брикету", callback_data="18")]
    markup.add(*item1)
    await bot.send_message(callback_query.from_user.id, text.text_100, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '101')
async def text_101(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 101)
    Functions.Functions.change_1_data(user_id, 'money', 'user_id', 50, multiplier=-1)
    Functions.Functions.change_1_data(user_id, 'Endurance', 'user_id', 2)
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = [types.InlineKeyboardButton("Поставити кілька загальних запитань про Радикс", callback_data="77"),
             types.InlineKeyboardButton("Попросити пояснити феномен зруйнованих будинків", callback_data="306")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_101, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '102')
async def text_102(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 102)
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = [types.InlineKeyboardButton("Запитаєти, як отримати перепустку", callback_data="38"),
             types.InlineKeyboardButton("Залишити його і спробувати роздобути десь меч", callback_data="137")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_102, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '103')
async def text_103(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 103)
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("Піти за нею", callback_data="75"),
             types.InlineKeyboardButton("Залишитися тут", callback_data="280")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_103, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '104')
async def text_104(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_1_fight(callback_query, 104, 7, 8, "fight", text.text_104)
    # user_id = callback_query.from_user.id
    # Functions.DB.update_one_value(user_id, 'text_number', 104)
    # Functions.DB.update_add_enemy(user_id, 7, 8, 'e_mastery_104', 'e_endurance_104')
    # markup = types.InlineKeyboardMarkup()
    # item1 = [types.InlineKeyboardButton("Почати бійку", callback_data="fight")]
    # markup.add(*item1)
    # await bot.send_message(callback_query.from_user.id, text.text_104, reply_markup=markup, parse_mode='Markdown')
    # await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '105')
async def text_105(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_move(callback_query, 105, "168", text.text_105)
    # user_id = callback_query.from_user.id
    # Functions.DB.update_one_value(user_id, 'text_number', 105)
    # markup = types.InlineKeyboardMarkup()
    # item1 = [types.InlineKeyboardButton("Go on", callback_data="168")]
    # markup.add(*item1)
    # await bot.send_message(user_id, text.text_105, reply_markup=markup, parse_mode='Markdown')
    # await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '106')
async def text_106(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 106)
    Functions.DB.update_add_enemy(user_id, 8, 14, 'e_mastery_106', 'e_endurance_106')

    buttons_data = [
        ("Я знаю про його слабкість", "check_106"),
        ("Почати бійку", "fight")
    ]
    markup = types.InlineKeyboardMarkup()
    markup.add(*Functions.Functions.create_inline_buttons(*buttons_data))

    await bot.send_message(user_id, text.text_106, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == 'check_106')
async def text_check_106_callback(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_text = 'Введіть номер параграфу або переходьте до бою, якщо не знаєте номеру параграфу'
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("Не знаю номеру параграфу. Почати бійку", callback_data="fight")]
    markup.add(*item1)
    await bot.send_message(user_id, message_text, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.message_handler(text='262')
async def paragraph_262(message: types.Message, state: FSMContext):
    print('paragraph_262')
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Перевірити Удачу", callback_data="luck_262"))
    await bot.send_message(message.chat.id, text.text_262, reply_markup=markup)


@dp.callback_query_handler(lambda c: c.data == 'luck_262')
async def text_check_106(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id

    # Retrieve Luck value
    luck = Functions.DB.select_one_value(user_id, 'Luck', 'user_id')

    if luck > 0:
        result = Functions.Functions.roll_dice_2()
        markup = types.InlineKeyboardMarkup()
        if result <= luck:  # good luck
            item1 = [types.InlineKeyboardButton('Go on', callback_data='341')]
            markup.add(*item1)
            await bot.send_message(user_id, "Вам пощастило", reply_markup=markup)
        else:
            item1 = [types.InlineKeyboardButton('Go on', callback_data='133')]
            markup.add(*item1)
            await bot.send_message(user_id, "Вам не пощастило", reply_markup=markup)
        Functions.DB.update_one_value(callback_query.from_user.id, 'Luck', luck - 1)
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '107')
async def text_107(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 107)
    Functions.DB.update_one_value(user_id, 'dogfight_107', 2)
    Functions.DB.update_add_enemy(user_id, 7, 8, 'e_mastery_107', 'e_endurance_107')

    buttons_data = [
        ("Почати бійку", "fight_107"),
        ("Рукопашний бій", "fight")
    ]
    markup = types.InlineKeyboardMarkup()
    markup.add(*Functions.Functions.create_inline_buttons(*buttons_data))

    await bot.send_message(callback_query.from_user.id, text.text_107, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == 'fight_107')
async def text_fight_107(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'dogfight_107', 1)
    Functions.Functions.change_1_data(user_id, 'Mastery', 'user_id', 1)
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("Go on", callback_data="fight")]
    markup.add(*item1)
    await bot.send_message(user_id, "До бою!", reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == 'check_luck_107')
async def check_luck_107(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    character_data_outer = Functions.DB.retrieve_character_data(user_id)
    character = Functions.Functions.Character(mastery=character_data_outer[0], endurance=character_data_outer[1],
                                              luck=character_data_outer[2])
    if character.luck > 0:
        result = Functions.Functions.roll_dice_2()
        markup = types.InlineKeyboardMarkup()
        if result <= character.luck:  # good luck
            item1 = [types.InlineKeyboardButton('Go on', callback_data='15')]
            markup.add(*item1)
            await bot.send_message(callback_query.from_user.id, "Вам пощастило!", reply_markup=markup)
        else:
            item1 = [types.InlineKeyboardButton('Go on', callback_data='150')]
            markup.add(*item1)
            await bot.send_message(callback_query.from_user.id, "На жаль, вам не пощастило!", reply_markup=markup)
        Functions.DB.update_one_value(callback_query.from_user.id, 'Luck', character.luck - 1)
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '108')
async def text_108(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 108)
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = [types.InlineKeyboardButton("Постаратися уникнути зустрічі", callback_data="120"),
             types.InlineKeyboardButton("Зачекати і подивитися, що станеться", callback_data="236")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_108, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '109')
async def text_109(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 109)
    Functions.Functions.change_1_data(user_id, 'Endurance', 'user_id', 2, multiplier=-1)
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("Go on", callback_data="204")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_109, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '110')
async def text_110(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 110)
    data_list = ["Запечатана трубка", "Магнітна міна", "Фотонна граната",
                 "Ручний фазер", "Інфрачервоний сканер"]
    Functions.DB.insert_list_data(user_id, data_list, 'buttons_data_110')
    buttons_data = [
        ("Запечатана трубка", "110_1"),
        ("Магнітна міна", "110_2"),
        ("Фотонна граната", "110_3"),
        ("Ручний фазер", "110_4"),
        ("Інфрачервоний сканер", "110_5"),
        ("Продовжити", "348")
    ]
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(*Functions.Functions.create_inline_buttons(*buttons_data))
    await bot.send_message(user_id, text.text_110, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '110_1')
async def text_110_1(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    data_string = Functions.DB.select_one_value(user_id, 'buttons_data_110', 'user_id')
    # Wrap the string with brackets to make it a valid list literal
    formatted_string = f'[{data_string}]'

    # Use ast.literal_eval to safely evaluate the string as a list
    data_list = ast.literal_eval(formatted_string)

    data_list.remove("Запечатана трубка")
    Functions.DB.insert_list_data(user_id, data_list, 'buttons_data_110')
    Functions.DB.update_one_value(user_id, 'sealed_tube_110', 1)

    buttons_data_0 = {
        "Запечатана трубка": ("Запечатана трубка", "110_1"),
        "Магнітна міна": ("Магнітна міна", "110_2"),
        "Фотонна граната": ("Фотонна граната", "110_3"),
        "Ручний фазер": ("Ручний фазер", "110_4"),
        "Інфрачервоний сканер": ("Інфрачервоний сканер", "110_5")
    }
    buttons_data = []
    for key, value in buttons_data_0.items():
        for item in data_list:
            if key == item:
                buttons_data.append(value)
    if len(buttons_data) > 3:  # якщо гравець ще не взяв 2 предмети
        buttons_data.append(("Продовжити", "348"))
        text_message = 'Ви берете запечатану трубку. Бажаєте ще щось взяти?'
    else:
        text_message = "Ви взяли два предмета."
        buttons_data = [
            ("Продовжити", "348")
        ]
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(*Functions.Functions.create_inline_buttons(*buttons_data))
    await bot.send_message(user_id, text_message, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '110_2')
async def text_110_2(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    data_string = Functions.DB.select_one_value(user_id, 'buttons_data_110', 'user_id')
    # Wrap the string with brackets to make it a valid list literal
    formatted_string = f'[{data_string}]'

    # Use ast.literal_eval to safely evaluate the string as a list
    data_list = ast.literal_eval(formatted_string)

    data_list.remove("Магнітна міна")
    Functions.DB.insert_list_data(user_id, data_list, 'buttons_data_110')
    Functions.DB.update_one_value(user_id, 'magnetic_mine_110', 1)

    buttons_data_0 = {
        "Запечатана трубка": ("Запечатана трубка", "110_1"),
        "Магнітна міна": ("Магнітна міна", "110_2"),
        "Фотонна граната": ("Фотонна граната", "110_3"),
        "Ручний фазер": ("Ручний фазер", "110_4"),
        "Інфрачервоний сканер": ("Інфрачервоний сканер", "110_5")
    }
    buttons_data = []
    for key, value in buttons_data_0.items():
        for item in data_list:
            if key == item:
                buttons_data.append(value)
    if len(buttons_data) > 3:  # якщо гравець ще не взяв 2 предмети
        buttons_data.append(("Продовжити", "348"))
        text_message = 'Ви берете магнітну міну. Бажаєте ще щось взяти?'
    else:
        text_message = "Ви взяли два предмета."
        buttons_data = [
            ("Продовжити", "348")
        ]
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(*Functions.Functions.create_inline_buttons(*buttons_data))
    await bot.send_message(user_id, text_message, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '110_3')
async def text_110_3(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    data_string = Functions.DB.select_one_value(user_id, 'buttons_data_110', 'user_id')
    # Wrap the string with brackets to make it a valid list literal
    formatted_string = f'[{data_string}]'

    # Use ast.literal_eval to safely evaluate the string as a list
    data_list = ast.literal_eval(formatted_string)

    data_list.remove("Фотонна граната")
    Functions.DB.insert_list_data(user_id, data_list, 'buttons_data_110')
    Functions.DB.update_one_value(user_id, 'grenade_110_215', 1)

    buttons_data_0 = {
        "Запечатана трубка": ("Запечатана трубка", "110_1"),
        "Магнітна міна": ("Магнітна міна", "110_2"),
        "Фотонна граната": ("Фотонна граната", "110_3"),
        "Ручний фазер": ("Ручний фазер", "110_4"),
        "Інфрачервоний сканер": ("Інфрачервоний сканер", "110_5")
    }
    buttons_data = []
    for key, value in buttons_data_0.items():
        for item in data_list:
            if key == item:
                buttons_data.append(value)
    if len(buttons_data) > 3:  # якщо гравець ще не взяв 2 предмети
        buttons_data.append(("Продовжити", "348"))
        text_message = 'Ви берете фотонну гранату. Бажаєте ще щось взяти?'
    else:
        text_message = "Ви взяли два предмета."
        buttons_data = [
            ("Продовжити", "348")
        ]
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(*Functions.Functions.create_inline_buttons(*buttons_data))
    await bot.send_message(user_id, text_message, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '110_4')
async def text_110_4(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    data_string = Functions.DB.select_one_value(user_id, 'buttons_data_110', 'user_id')
    # Wrap the string with brackets to make it a valid list literal
    formatted_string = f'[{data_string}]'

    # Use ast.literal_eval to safely evaluate the string as a list
    data_list = ast.literal_eval(formatted_string)

    data_list.remove("Ручний фазер")
    Functions.DB.insert_list_data(user_id, data_list, 'buttons_data_110')
    Functions.DB.update_one_value(user_id, 'hand_phaser_110', 1)

    buttons_data_0 = {
        "Запечатана трубка": ("Запечатана трубка", "110_1"),
        "Магнітна міна": ("Магнітна міна", "110_2"),
        "Фотонна граната": ("Фотонна граната", "110_3"),
        "Ручний фазер": ("Ручний фазер", "110_4"),
        "Інфрачервоний сканер": ("Інфрачервоний сканер", "110_5")
    }
    buttons_data = []
    for key, value in buttons_data_0.items():
        for item in data_list:
            if key == item:
                buttons_data.append(value)
    if len(buttons_data) > 3:  # якщо гравець ще не взяв 2 предмети
        buttons_data.append(("Продовжити", "348"))
        text_message = 'Ви берете ручний фазер. Бажаєте ще щось взяти?'
    else:
        text_message = "Ви взяли два предмета."
        buttons_data = [
            ("Продовжити", "348")
        ]
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(*Functions.Functions.create_inline_buttons(*buttons_data))
    await bot.send_message(user_id, text_message, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '110_5')
async def text_110_5(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    data_string = Functions.DB.select_one_value(user_id, 'buttons_data_110', 'user_id')
    # Wrap the string with brackets to make it a valid list literal
    formatted_string = f'[{data_string}]'

    # Use ast.literal_eval to safely evaluate the string as a list
    data_list = ast.literal_eval(formatted_string)

    data_list.remove("Інфрачервоний сканер")
    Functions.DB.insert_list_data(user_id, data_list, 'buttons_data_110')
    Functions.DB.update_one_value(user_id, 'scanner_110_117', 1)

    buttons_data_0 = {
        "Запечатана трубка": ("Запечатана трубка", "110_1"),
        "Магнітна міна": ("Магнітна міна", "110_2"),
        "Фотонна граната": ("Фотонна граната", "110_3"),
        "Ручний фазер": ("Ручний фазер", "110_4"),
        "Інфрачервоний сканер": ("Інфрачервоний сканер", "110_5")
    }
    buttons_data = []
    for key, value in buttons_data_0.items():
        for item in data_list:
            if key == item:
                buttons_data.append(value)
    if len(buttons_data) > 3:  # якщо гравець ще не взяв 2 предмети
        buttons_data.append(("Продовжити", "348"))
        text_message = 'Ви берете інфрачервоний сканер. Бажаєте ще щось взяти?'
    else:
        text_message = "Ви взяли два предмета."
        buttons_data = [
            ("Продовжити", "348")
        ]
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(*Functions.Functions.create_inline_buttons(*buttons_data))
    await bot.send_message(user_id, text_message, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '111')
async def text_111(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 111)
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = [
        types.InlineKeyboardButton("Запитати у сторожа, що знаходиться за іншими дверима", callback_data="356"),
        types.InlineKeyboardButton("Піти до університету", callback_data="146")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_111, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '112')
async def text_112(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 112)
    markup = types.InlineKeyboardMarkup(row_width=1)
    result = random.randint(1, 6)

    # Check if the result is even or odd
    if result % 2 == 0:
        item1 = [types.InlineKeyboardButton('Go on', callback_data="122")]  # Even number
    else:
        item1 = [types.InlineKeyboardButton('Go on', callback_data="253")]  # Odd number

    markup.add(*item1)
    await bot.send_message(user_id, text.text_112, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '113')
async def text_113(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 113)
    Functions.DB.update_add_enemy(user_id, 5, 8, 'e_mastery_113_1', 'e_endurance_113_1')
    Functions.DB.update_add_enemy(user_id, 6, 8, 'e_mastery_113_2', 'e_endurance_113_2')
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("Грус", callback_data="grus"),
             types.InlineKeyboardButton("Індус", callback_data="indus")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_113, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == 'grus')
async def text_113_1(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'flag113', 1)
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("До бою", callback_data="fight")]
    markup.add(*item1)
    await bot.send_message(user_id, "Ти обираєш битися з Грусом", reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == 'indus')
async def text_113_2(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'flag113', 2)
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("До бою", callback_data="fight")]
    markup.add(*item1)
    await bot.send_message(user_id, "Ти обираєш битися з Індусом", reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '114')
async def text_114(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 114)
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = [types.InlineKeyboardButton("Повернутися на скелі і пройти до будівлі", callback_data="88"),
             types.InlineKeyboardButton("Наблизитися до людей у полях", callback_data="22")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_114, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '115')
async def text_115(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 115)
    Functions.Functions.change_1_data(user_id, 'Endurance', 'user_id', 3)

    buttons_data = [
        ("Можливість повстання людей", "289"),
        ("Програма відновлення у місті", "93")
    ]
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(*Functions.Functions.create_inline_buttons(*buttons_data))

    await bot.send_message(user_id, text.text_115, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '116')
async def text_116(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_move(callback_query, 116, "300", text.text_116)
    # user_id = callback_query.from_user.id
    # Functions.DB.update_one_value(user_id, 'text_number', 116)
    # markup = types.InlineKeyboardMarkup()
    # item1 = [types.InlineKeyboardButton("Go on", callback_data="300")]
    # markup.add(*item1)
    # await bot.send_message(user_id, text.text_116, reply_markup=markup, parse_mode='Markdown')
    # await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '117')
async def text_117(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 117)
    Functions.Functions.change_1_data(user_id, 'money', 'user_id', 500)
    Functions.DB.update_one_value(user_id, 'bracelet_ziridium_117', 1)  # браслет із зірідієвим покриттям
    Functions.DB.update_one_value(user_id, 'scanner_110_117', 1)  # інфрачервоний сканер
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("Go on", callback_data="132")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_117, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '118')
async def text_118(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_move(callback_query, 118, "185", text.text_118)
    # user_id = callback_query.from_user.id
    # Functions.DB.update_one_value(user_id, 'text_number', 118)
    # markup = types.InlineKeyboardMarkup()
    # item1 = [types.InlineKeyboardButton("Go on", callback_data="185")]
    # markup.add(*item1)
    # await bot.send_message(user_id, text.text_118, reply_markup=markup, parse_mode='Markdown')
    # await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '119')
async def text_119(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 119)

    buttons_data = [
        ("Вбив Жирдяя, щоб отримати доступ до комп'ютера", "209"),
        ("74", "74")
    ]
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(*Functions.Functions.create_inline_buttons(*buttons_data))

    await bot.send_message(user_id, text.text_119, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '120')
async def text_120(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 120)

    buttons_data = [
        ("Атакувати його", "179"),
        ("Спробувати поговорити з ним", "195")
    ]
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(*Functions.Functions.create_inline_buttons(*buttons_data))

    await bot.send_message(user_id, text.text_120, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '121')
async def text_121(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 121)

    buttons_data = [
        ("Піти з ним", "41"),
        ("Сказати, що ви маєте наздогнати пораненого аркадіанця", "283")
    ]
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(*Functions.Functions.create_inline_buttons(*buttons_data))

    await bot.send_message(user_id, text.text_121, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '122')
async def text_122(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_move(callback_query, 122, "336", text.text_122)
    # user_id = callback_query.from_user.id
    # Functions.DB.update_one_value(user_id, 'text_number', 122)
    # markup = types.InlineKeyboardMarkup()
    # item1 = [types.InlineKeyboardButton("Go on", callback_data="336")]
    # markup.add(*item1)
    # await bot.send_message(user_id, text.text_122, reply_markup=markup, parse_mode='Markdown')
    # await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '123')
async def text_123(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 123)

    buttons_data = [
        ("Вирушити на захід", "8"),
        ("Вирушити на схід", "39")
    ]
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(*Functions.Functions.create_inline_buttons(*buttons_data))

    await bot.send_message(user_id, text.text_123, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '124')
async def text_124(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 124)
    Functions.Functions.change_1_data(user_id, 'Mastery', 'user_id', 1, multiplier=-1)
    Functions.DB.update_add_enemy(user_id, 6, 8, 'e_mastery_124', 'e_endurance_124')
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("Почати бійку", callback_data="fight")]
    markup.add(*item1)
    await bot.send_message(callback_query.from_user.id, text.text_124, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '125')
async def text_125(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 125)

    buttons_data = [
        ("Наполягати на тому, щоб залишитися", "184"),
        ("Піти", "252")
    ]
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(*Functions.Functions.create_inline_buttons(*buttons_data))

    await bot.send_message(user_id, text.text_125, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '126')
async def text_126(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 126)

    buttons_data = [
        ("Спробувати втекти", "340"),
        ("Не пробувати втекти", "387")
    ]
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(*Functions.Functions.create_inline_buttons(*buttons_data))

    await bot.send_message(user_id, text.text_126, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '127')
async def text_127(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 127)
    Functions.Functions.change_1_data(user_id, 'Endurance', 'user_id', 1, multiplier=-1)

    buttons_data = [
        ("Піти вперед", "333"),
        ("Піти на південь", "221")
    ]
    markup = types.InlineKeyboardMarkup()
    markup.add(*Functions.Functions.create_inline_buttons(*buttons_data))

    await bot.send_message(user_id, text.text_127, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '128')
async def text_128(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 128)

    buttons_data = [
        ("Використати ранець", "57"),
        ("Не використовувати ранець", "2")
    ]
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(*Functions.Functions.create_inline_buttons(*buttons_data))

    await bot.send_message(user_id, text.text_128, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '129')
async def text_129(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_game_over(callback_query, 129, text.text_129)


@dp.callback_query_handler(lambda c: c.data == '130')
async def text_130(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 130)
    brain_probe = Functions.DB.select_one_value(user_id, 'brain_probe_355', 'user_id')

    markup = types.InlineKeyboardMarkup(row_width=1)

    if brain_probe == 1:
        item1 = [types.InlineKeyboardButton("Використати мозковий зонд", callback_data="153")]
    else:
        item1 = [types.InlineKeyboardButton("Здатися", callback_data="118")]

    markup.add(*item1)

    await bot.send_message(user_id, text.text_130, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '131')
async def text_131(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_move(callback_query, 131, "313", text.text_131)
    # user_id = callback_query.from_user.id
    # Functions.DB.update_one_value(user_id, 'text_number', 131)
    # markup = types.InlineKeyboardMarkup()
    # item1 = [types.InlineKeyboardButton("Go on", callback_data="313")]
    # markup.add(*item1)
    # await bot.send_message(user_id, text.text_131, reply_markup=markup, parse_mode='Markdown')
    # await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '132')
async def text_132(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 132)
    Functions.Functions.change_1_data(user_id, 'Endurance', 'user_id', 2, multiplier=-1)
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("Go on", callback_data="313")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_132, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '133')
async def text_133(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_1_fight(callback_query, 133, 8, 12, "fight", text.text_133)
    # user_id = callback_query.from_user.id
    # Functions.DB.update_one_value(user_id, 'text_number', 133)
    # Functions.DB.update_add_enemy(user_id, 8, 12, 'e_mastery_133', 'e_endurance_133')
    # markup = types.InlineKeyboardMarkup()
    # item1 = [types.InlineKeyboardButton("Почати бійку", callback_data="fight")]
    # markup.add(*item1)
    # await bot.send_message(callback_query.from_user.id, text.text_133, reply_markup=markup, parse_mode='Markdown')
    # await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '134')
async def text_134(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 134)
    Functions.Functions.change_1_data(user_id, 'Endurance', 'user_id', 4)
    appointment = Functions.DB.select_one_value(user_id, 'appointment_74', 'user_id')

    markup = types.InlineKeyboardMarkup(row_width=1)

    if appointment == 1:
        item1 = [types.InlineKeyboardButton("У мене вранці призначена зустріч", callback_data="376")]
    else:
        item1 = [types.InlineKeyboardButton("Go on", callback_data="317")]

    markup.add(*item1)

    await bot.send_message(user_id, text.text_134, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '135')
async def text_135(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 135)
    food_briquette = Functions.DB.select_one_value(user_id, 'food_briquette_12', 'user_id')

    if food_briquette == 1:
        Functions.Functions.change_1_data(user_id, 'Endurance', 'user_id', 4)
        text_message = text.text_135_1
    else:
        Functions.Functions.change_1_data(user_id, 'Endurance', 'user_id', 2)
        text_message = text.text_135_2

    buttons_data = [
        ("Вирушити праворуч", "171"),
        ("Вирушити праворуч", "108")
    ]
    markup = types.InlineKeyboardMarkup()
    markup.add(*Functions.Functions.create_inline_buttons(*buttons_data))

    await bot.send_message(user_id, text_message, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '136')
async def text_136(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_1_fight(callback_query, 136, 6, 8, "fight", text.text_136)
    # user_id = callback_query.from_user.id
    # Functions.DB.update_one_value(user_id, 'text_number', 136)
    # Functions.DB.update_add_enemy(user_id, 6, 8, 'e_mastery_136', 'e_endurance_136')
    # markup = types.InlineKeyboardMarkup()
    # item1 = [types.InlineKeyboardButton("Почати бійку", callback_data="fight")]
    # markup.add(*item1)
    # await bot.send_message(callback_query.from_user.id, text.text_136, reply_markup=markup, parse_mode='Markdown')
    # await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '137')
async def text_137(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_move(callback_query, 137, "16", text.text_137)
    # user_id = callback_query.from_user.id
    # Functions.DB.update_one_value(user_id, 'text_number', 137)
    # markup = types.InlineKeyboardMarkup()
    # item1 = [types.InlineKeyboardButton("Go on", callback_data="16")]
    # markup.add(*item1)
    # await bot.send_message(user_id, text.text_137, reply_markup=markup, parse_mode='Markdown')
    # await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '138')
async def text_138(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 138)
    Functions.Functions.change_1_data(user_id, 'money', 'user_id', 40, multiplier=-1)
    Functions.Functions.change_1_data(user_id, 'Endurance', 'user_id', 3)

    buttons_data = [
        ("Піти в бар", "115"),
        ("Піти на зустріч з ним", "194")
    ]
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(*Functions.Functions.create_inline_buttons(*buttons_data))

    await bot.send_message(user_id, text.text_138, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '139')
async def text_139(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_move(callback_query, 139, "177", text.text_139)
    # user_id = callback_query.from_user.id
    # Functions.DB.update_one_value(user_id, 'text_number', 139)
    # markup = types.InlineKeyboardMarkup()
    # item1 = [types.InlineKeyboardButton("Go on", callback_data="177")]
    # markup.add(*item1)
    # await bot.send_message(user_id, text.text_139, reply_markup=markup, parse_mode='Markdown')
    # await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '140')
async def text_140(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 140)

    character_data = Functions.DB.retrieve_character_data(user_id)
    character = Functions.Functions.Character(mastery=character_data[0], endurance=character_data[1],
                                              luck=character_data[2])
    result = Functions.Functions.roll_dice_2()

    print(result)
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton('Go on', callback_data="330")]
    if result <= character.luck:
        item1 = [types.InlineKeyboardButton('Go on', callback_data="233")]
    character.luck -= 1
    Functions.DB.update_one_value(callback_query.from_user.id, 'Luck', character.luck)
    markup.add(*item1)

    await bot.send_message(user_id, text.text_140, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '141')
async def text_141(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 141)
    Functions.Functions.change_1_data(user_id, 'Mastery', 'user_id', 1)
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("Go on", callback_data="55")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_141, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '142')
async def text_142(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 142)

    buttons_data = [
        ("Повернутися назад", "221"),
        ("Повернути на захід", "324"),
        ("Повернути на схід", "333")
    ]
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(*Functions.Functions.create_inline_buttons(*buttons_data))

    await bot.send_message(user_id, text.text_142, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '143')
async def text_143(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 143)
    Functions.Functions.change_1_data(user_id, 'Endurance', 'user_id', 2, multiplier=-1)
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("Go on", callback_data="100")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_143, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '144')
async def text_144(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_move(callback_query, 144, "370", text.text_144)
    # user_id = callback_query.from_user.id
    # Functions.DB.update_one_value(user_id, 'text_number', 144)
    # markup = types.InlineKeyboardMarkup()
    # item1 = [types.InlineKeyboardButton("Продовжити", callback_data="370")]
    # markup.add(*item1)
    # await bot.send_message(user_id, text.text_144, reply_markup=markup, parse_mode='Markdown')
    # await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '145')
async def text_145(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 145)
    killed = Functions.DB.select_one_value(user_id, 'killed_145', 'user_id')
    markup = types.InlineKeyboardMarkup()

    if killed == 1:
        item1 = [types.InlineKeyboardButton("Go on", callback_data="28")]
    else:
        item1 = [types.InlineKeyboardButton("Go on", callback_data="187")]

    markup.add(*item1)

    await bot.send_message(user_id, text.text_145, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '146')
async def text_146(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 146)

    buttons_data = [
        ("Пройти на Науковий поверх", "266"),
        ("Пройти на Художній поверх", "258")
    ]
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(*Functions.Functions.create_inline_buttons(*buttons_data))

    await bot.send_message(user_id, text.text_146, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '147')
async def text_147(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 147)

    buttons_data = [
        ("Продовжити йти прямо", "114"),
        ("Повернути", "108")
    ]
    markup = types.InlineKeyboardMarkup()
    markup.add(*Functions.Functions.create_inline_buttons(*buttons_data))

    await bot.send_message(user_id, text.text_147, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '148')
async def text_148(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_game_over(callback_query, 148, text.text_148)


@dp.callback_query_handler(lambda c: c.data == '149')
async def text_149(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_move(callback_query, 149, "381", text.text_149)
    # user_id = callback_query.from_user.id
    # Functions.DB.update_one_value(user_id, 'text_number', 149)
    # markup = types.InlineKeyboardMarkup()
    # item1 = [types.InlineKeyboardButton("Go on", callback_data="381")]
    # markup.add(*item1)
    # await bot.send_message(user_id, text.text_149, reply_markup=markup, parse_mode='Markdown')
    # await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '150')
async def text_150(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_1_fight(callback_query, 150, 8, 10, "fight", text.text_150)
    # user_id = callback_query.from_user.id
    # Functions.DB.update_one_value(user_id, 'text_number', 150)
    # Functions.DB.update_add_enemy(user_id, 8, 10, 'e_mastery_150', 'e_endurance_150')
    # markup = types.InlineKeyboardMarkup()
    # item1 = [types.InlineKeyboardButton("Почати бійку", callback_data="fight")]
    # markup.add(*item1)
    # await bot.send_message(callback_query.from_user.id, text.text_150, reply_markup=markup, parse_mode='Markdown')
    # await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '151')
async def text_151(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 151)

    character_data = Functions.DB.retrieve_character_data(user_id)
    character = Functions.Functions.Character(mastery=character_data[0], endurance=character_data[1],
                                              luck=character_data[2])
    result = Functions.Functions.roll_dice_2()

    print(result)
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton('Go on', callback_data="249")]
    if result <= character.luck:
        item1 = [types.InlineKeyboardButton('Go on', callback_data="336")]
    character.luck -= 1
    Functions.DB.update_one_value(user_id, 'Luck', character.luck)
    markup.add(*item1)

    await bot.send_message(user_id, text.text_151, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '152')
async def text_152(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 152)
    Functions.DB.update_one_value(user_id, 'check_152', 152)
    Functions.Functions.change_1_data(user_id, 'money', 'user_id', 20, multiplier=-1)
    Functions.Functions.change_1_data(user_id, 'Endurance', 'user_id', 4)

    buttons_data = [
        ('Запитати, як пройти до "Вщент"', "335"),
        ('Запитати, як пройти до відеорами "Адольфо"', "260")
    ]
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(*Functions.Functions.create_inline_buttons(*buttons_data))

    await bot.send_message(user_id, text.text_152, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '153')
async def text_153(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 153)
    Functions.Functions.change_1_data(user_id, 'Luck', 'user_id', 1)
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("118", callback_data="118")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_153, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '154')
async def text_154(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 154)
    markup = types.InlineKeyboardMarkup()
    result = random.randint(1, 6)

    # Check if the result is even or odd
    if result % 2 == 0:
        item1 = [types.InlineKeyboardButton('Go on', callback_data="166")]  # Even number
    else:
        item1 = [types.InlineKeyboardButton('Go on', callback_data="50")]  # Odd number

    markup.add(*item1)
    await bot.send_message(user_id, text.text_154, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '155')
async def text_155(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 155)
    Functions.Functions.change_1_data(user_id, 'Luck', 'user_id', 1)
    Functions.DB.update_one_value(user_id, 'uniform_155', 1)
    Functions.Functions.change_1_data(user_id, 'Endurance', 'user_id', 4)
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("Go on", callback_data="163")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_155, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '156')
async def text_156(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 156)
    Functions.Functions.change_1_data(user_id, 'Endurance', 'user_id', 2, multiplier=-1)
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("207", callback_data="207")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_156, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '157')
async def text_157(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_1_fight(callback_query, 157, 6, 8, "fight", text.text_157)
    # user_id = callback_query.from_user.id
    # Functions.DB.update_one_value(user_id, 'text_number', 157)
    # Functions.DB.update_add_enemy(user_id, 6, 8, 'e_mastery_157', 'e_endurance_157')
    # markup = types.InlineKeyboardMarkup()
    # item1 = [types.InlineKeyboardButton("Почати бійку", callback_data="fight")]
    # markup.add(*item1)
    # await bot.send_message(callback_query.from_user.id, text.text_157, reply_markup=markup, parse_mode='Markdown')
    # await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '158')
async def text_158(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 158)
    markup = types.InlineKeyboardMarkup()
    # zodiac = Functions.DB.select_one_value(user_id, 'zodiac_47', 'user_id')
    #
    # item1 = [types.InlineKeyboardButton('Go on', callback_data="3")]
    # if zodiac == 1:
    #     item1 = [types.InlineKeyboardButton('Go on', callback_data="31")]
    item1 = [types.InlineKeyboardButton('Палац Жирдяя', callback_data="3"),
             types.InlineKeyboardButton('Зодіак', callback_data="31")]

    markup.add(*item1)
    await bot.send_message(user_id, text.text_158, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '159')
async def text_159(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 159)

    buttons_data = [
        ('Взяти щось', "42"),
        ('Нічого не брати', "391")
    ]
    markup = types.InlineKeyboardMarkup()
    markup.add(*Functions.Functions.create_inline_buttons(*buttons_data))

    await bot.send_message(user_id, text.text_159, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '160')
async def text_160(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id

    # Update text_number to 160
    Functions.DB.update_one_value(user_id, 'text_number', 160)

    character_data = Functions.DB.retrieve_character_data(user_id)
    character = Functions.Functions.Character(mastery=character_data[0], endurance=character_data[1],
                                              luck=character_data[2])
    result = Functions.Functions.roll_dice_2()
    print(result)

    if result <= character.luck:
        markup = types.InlineKeyboardMarkup()
        item1 = [types.InlineKeyboardButton('Go on', callback_data="374")]
        markup.add(*item1)
        await bot.send_message(user_id, text.text_160_1, reply_markup=markup, parse_mode='Markdown')
    else:
        await bot.send_message(user_id, text.text_160_2)
    character.luck -= 1
    Functions.DB.update_one_value(user_id, 'Luck', character.luck)

    # Answer the callback query
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '161')
async def text_161(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_1_fight(callback_query, 161, 0, 14, "fight", text.text_161)
    # user_id = callback_query.from_user.id
    # Functions.DB.update_one_value(user_id, 'text_number', 161)
    # Functions.DB.update_add_enemy(user_id, 0, 14, 'e_mastery_161', 'e_endurance_161')
    # markup = types.InlineKeyboardMarkup()
    # item1 = [types.InlineKeyboardButton("Почати бійку", callback_data="fight")]
    # markup.add(*item1)
    # await bot.send_message(callback_query.from_user.id, text.text_161, reply_markup=markup, parse_mode='Markdown')
    # await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '162')
async def text_162(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id

    # Update text_number to 162
    Functions.DB.update_one_value(user_id, 'text_number', 162)

    character_data = Functions.DB.retrieve_character_data(user_id)
    character = Functions.Functions.Character(mastery=character_data[0], endurance=character_data[1],
                                              luck=character_data[2])
    result = Functions.Functions.roll_dice_2()
    print(result)

    markup = types.InlineKeyboardMarkup()
    if result <= character.luck:
        item1 = [types.InlineKeyboardButton('Go on', callback_data="183")]
        markup.add(*item1)
        await bot.send_message(user_id, text.text_162, reply_markup=markup, parse_mode='Markdown')
    else:
        item1 = [types.InlineKeyboardButton('Go on', callback_data="373")]
        markup.add(*item1)
        await bot.send_message(user_id, text.text_162, reply_markup=markup, parse_mode='Markdown')
    character.luck -= 1
    Functions.DB.update_one_value(user_id, 'Luck', character.luck)

    # Answer the callback query
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '163')
async def text_163(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 163)
    cutter = Functions.DB.select_one_value(user_id, 'cutter393', 'user_id')
    markup = types.InlineKeyboardMarkup(row_width=1)
    if cutter == 1:  # різак є
        item1 = [types.InlineKeyboardButton('Використати сіру уніформу як маскування', callback_data="344"),
                 types.InlineKeyboardButton('Віддати перевагу використанню різака для дроту', callback_data="302")]
        markup.add(*item1)
        await bot.send_message(user_id, text.text_163_1, reply_markup=markup, parse_mode='Markdown')
    else:
        item1 = [types.InlineKeyboardButton('Go on', callback_data="344")]
        markup.add(*item1)
        await bot.send_message(user_id, text.text_163_2, reply_markup=markup, parse_mode='Markdown')

    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '164')
async def text_164(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = [types.InlineKeyboardButton("Спробувати обдурити його", callback_data="246"),
             types.InlineKeyboardButton("Витягнути свій меч і битися з ним", callback_data="17")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_164, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '165')
async def text_165(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 165)
    Functions.Functions.change_1_data(user_id, 'Mastery', 'user_id', 1, multiplier=-1)
    Functions.DB.update_add_enemy(user_id, 6, 8, 'e_mastery_165', 'e_endurance_165')
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("Почати бійку", callback_data="fight")]
    markup.add(*item1)
    await bot.send_message(callback_query.from_user.id, text.text_165, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == 'take_sword_165')
async def text_165_1(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'sword', 1)
    Functions.DB.update_one_value(user_id, 'without_weapons', 1)
    Functions.Functions.change_1_data(user_id, 'Mastery', 'user_id', 1)
    text_message = 'Тепер у вас є меч.'
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("Go on", callback_data="336")]
    markup.add(*item1)
    await bot.send_message(callback_query.from_user.id, text_message, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '166')
async def text_166(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_game_over(callback_query, 166, text.text_166)


@dp.callback_query_handler(lambda c: c.data == '167')
async def text_167(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_move(callback_query, 167, "126", text.text_167)
    # user_id = callback_query.from_user.id
    # Functions.DB.update_one_value(user_id, 'text_number', 167)
    # markup = types.InlineKeyboardMarkup()
    # item1 = [types.InlineKeyboardButton("Go on", callback_data="126")]
    # markup.add(*item1)
    # await bot.send_message(user_id, text.text_167, reply_markup=markup, parse_mode='Markdown')
    # await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '168')
async def text_168(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 168)

    buttons_data = [
        ('Так', "68"),
        ('Ні', "274")
    ]
    markup = types.InlineKeyboardMarkup()
    markup.add(*Functions.Functions.create_inline_buttons(*buttons_data))

    await bot.send_message(user_id, text.text_168, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '169')
async def text_169(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 169)

    buttons_data = [
        ("Я знаю код", "check_169"),
        ("Повернутися до комп'ютерної зали", "381")
    ]
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(*Functions.Functions.create_inline_buttons(*buttons_data))

    await bot.send_message(user_id, text.text_169, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == 'check_169')
async def text_check_106_callback(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_text = "Введіть код або повертайтеся до комп'ютерної зали, якщо не знаєте код"
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("Не знаю код. Повернутися до комп'ютерної зали", callback_data="381")]
    markup.add(*item1)
    await bot.send_message(user_id, message_text, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.message_handler(text='110')
async def paragraph_110(message: types.Message, state: FSMContext):
    print('paragraph_110')
    user_id = message.chat.id
    Functions.DB.update_one_value(user_id, 'text_number', 110)
    data_list = ["Запечатана трубка", "Магнітна міна", "Фотонна граната",
                 "Ручний фазер", "Інфрачервоний сканер"]
    Functions.DB.insert_list_data(user_id, data_list, 'buttons_data_110')
    buttons_data = [
        ("Запечатана трубка", "110_1"),
        ("Магнітна міна", "110_2"),
        ("Фотонна граната", "110_3"),
        ("Ручний фазер", "110_4"),
        ("Інфрачервоний сканер", "110_5"),
        ("Продовжити", "348")
    ]
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(*Functions.Functions.create_inline_buttons(*buttons_data))
    await bot.send_message(message.chat.id, text.text_110, reply_markup=markup)

    # item1 = [types.InlineKeyboardButton("Go on", callback_data="348")]
    # markup.add(*item1)


@dp.callback_query_handler(lambda c: c.data == '170')
async def text_170(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_move(callback_query, 170, "235", text.text_170)
    # user_id = callback_query.from_user.id
    # Functions.DB.update_one_value(user_id, 'text_number', 170)
    # markup = types.InlineKeyboardMarkup()
    # item1 = [types.InlineKeyboardButton("Go on", callback_data="235")]
    # markup.add(*item1)
    # await bot.send_message(user_id, text.text_170, reply_markup=markup, parse_mode='Markdown')
    # await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '171')
async def text_171(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 171)
    Functions.Functions.change_1_data(user_id, 'Endurance', 'user_id', 1)

    buttons_data = [
        ('Дізнатися, що це за предмет', "383"),
        ('Продовжити подорож', "147")
    ]
    markup = types.InlineKeyboardMarkup()
    markup.add(*Functions.Functions.create_inline_buttons(*buttons_data))

    await bot.send_message(user_id, text.text_171, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '172')
async def text_172(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 172)
    Functions.DB.update_one_value(user_id, 'button_172', 1)
    Functions.DB.update_add_enemy(user_id, 6, 8, 'e_mastery_172_1', 'e_endurance_172_1')
    Functions.DB.update_add_enemy(user_id, 7, 8, 'e_mastery_172_2', 'e_endurance_172_2')
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("Перший стражник", callback_data="first_g"),
             types.InlineKeyboardButton("Другий стражник", callback_data="second_g")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_172, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == 'first_g')
async def text_172_1(callback_query: types.CallbackQuery):
    Functions.DB.update_one_value(callback_query.from_user.id, 'flag172', 1)
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("До бою", callback_data="fight")]
    markup.add(*item1)
    await bot.send_message(callback_query.from_user.id, "Ти обираєш битися з першим стражником", reply_markup=markup,
                           parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == 'second_g')
async def text_172_2(callback_query: types.CallbackQuery):
    Functions.DB.update_one_value(callback_query.from_user.id, 'flag172', 2)
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("До бою", callback_data="fight")]
    markup.add(*item1)
    await bot.send_message(callback_query.from_user.id, "Ти обираєш битися з другим стражником", reply_markup=markup,
                           parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '173')
async def text_173(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 173)

    buttons_data = [
        ('Запитати в когось у сірому', "310"),
        ('Запитати в когось у синьому', "102")
    ]
    markup = types.InlineKeyboardMarkup()
    markup.add(*Functions.Functions.create_inline_buttons(*buttons_data))

    await bot.send_message(user_id, text.text_173, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '174')
async def text_174(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_game_over(callback_query, 174, text.text_174)


@dp.callback_query_handler(lambda c: c.data == '175')
async def text_175(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_game_over(callback_query, 175, text.text_175)


@dp.callback_query_handler(lambda c: c.data == '176')
async def text_176(callback_query: types.CallbackQuery):
    Functions.DB.update_one_value(callback_query.from_user.id, 'text_number', 176)
    luck = Functions.DB.select_one_value(callback_query.from_user.id, 'Luck', 'user_id')
    Functions.DB.update_one_value(callback_query.from_user.id, 'Luck', luck - 1)
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = [types.InlineKeyboardButton('Go on', callback_data="196")]
    markup.add(*item1)
    await bot.send_message(callback_query.from_user.id, text.text_176, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '177')
async def text_177(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_game_over(callback_query, 177, text.text_177)


@dp.callback_query_handler(lambda c: c.data == '178')
async def text_178(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 178)

    buttons_data = [
        ('Ні, дякую, я огляну виставку сам', "111"),
        ('Приємно бачити, що хтось серйозно ставиться до своєї роботи', "19")
    ]
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(*Functions.Functions.create_inline_buttons(*buttons_data))

    await bot.send_message(user_id, text.text_178, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '179')
async def text_179(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_1_fight(callback_query, 179, 10, 14, "fight", text.text_179)
    # user_id = callback_query.from_user.id
    # Functions.DB.update_one_value(user_id, 'text_number', 179)
    # Functions.DB.update_add_enemy(user_id, 10, 14, 'e_mastery_179', 'e_endurance_179')
    # markup = types.InlineKeyboardMarkup()
    # item1 = [types.InlineKeyboardButton("Почати бійку", callback_data="fight")]
    # markup.add(*item1)
    # await bot.send_message(callback_query.from_user.id, text.text_179, reply_markup=markup, parse_mode='Markdown')
    # await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '180')
async def text_180(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_game_over(callback_query, 180, text.text_180)


@dp.callback_query_handler(lambda c: c.data == '181')
async def text_181(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_game_over(callback_query, 181, text.text_181)


@dp.callback_query_handler(lambda c: c.data == '182')
async def text_182(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 182)
    Functions.Functions.change_1_data(user_id, 'money', 'user_id', 20, multiplier=-1)
    Functions.Functions.change_1_data(user_id, 'Endurance', 'user_id', 2)
    Functions.Functions.change_1_data(user_id, 'Luck', 'user_id', 1, multiplier=-1)
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("Go on", callback_data="235")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_182, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '183')
async def text_183(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_move(callback_query, 183, "285", text.text_183)
    # user_id = callback_query.from_user.id
    # Functions.DB.update_one_value(user_id, 'text_number', 183)
    # markup = types.InlineKeyboardMarkup()
    # item1 = [types.InlineKeyboardButton("Go on", callback_data="285")]
    # markup.add(*item1)
    # await bot.send_message(user_id, text.text_183, reply_markup=markup, parse_mode='Markdown')
    # await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '184')
async def text_184(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_game_over(callback_query, 184, text.text_184)


@dp.callback_query_handler(lambda c: c.data == '185')
async def text_185(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 185)

    buttons_data = [
        ("Піти прямо до комп'ютерної будівлі", "219"),
        ('Дізнатися, де знаходиться арсенал', "284")
    ]
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(*Functions.Functions.create_inline_buttons(*buttons_data))

    await bot.send_message(user_id, text.text_185, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '186')
async def text_186(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 186)
    Functions.Functions.change_1_data(user_id, 'Luck', 'user_id', 1, multiplier=-1)

    buttons_data = [
        ("Повернути на південь", "384"),
        ('Продовжити йти прямо', "254")
    ]
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(*Functions.Functions.create_inline_buttons(*buttons_data))

    await bot.send_message(user_id, text.text_186, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '187')
async def text_187(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 187)

    buttons_data = [
        ("Запитати, чи може він роздобути вам пропуск", "385"),
        ('Запитати, чи може він дістати вам меч', "286")
    ]
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(*Functions.Functions.create_inline_buttons(*buttons_data))

    await bot.send_message(user_id, text.text_187, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '188')
async def text_188(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 188)

    buttons_data = [
        ("Просто чекати", "29"),
        ('Продовжити пошук способу привернути його увагу', "172")
    ]
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(*Functions.Functions.create_inline_buttons(*buttons_data))

    await bot.send_message(user_id, text.text_188, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '189')
async def text_189(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 189)
    Functions.Functions.change_1_data(user_id, 'Endurance', 'user_id', 3)
    Functions.Functions.change_1_data(user_id, 'Luck', 'user_id', 1)
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("Go on", callback_data="114")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_189, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '190')
async def text_190(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 190)
    Functions.DB.update_add_enemy(user_id, 9, 16, 'e_mastery_190', 'e_endurance_190')
    flag190 = Functions.DB.select_one_value(user_id, 'flag190', 'user_id')
    flag190_2 = Functions.DB.select_one_value(user_id, 'flag190_2', 'user_id')

    character_data = Functions.DB.retrieve_character_data_id(1)
    character = Functions.Functions.Character(mastery=character_data[0], endurance=character_data[1],
                                              luck=character_data[2])
    if flag190 != 1:
        Functions.DB.update_one_value(user_id, 'attack_190', 1)
        Functions.DB.update_one_value(user_id, 'flag190', 1)
        result = Functions.Functions.roll_dice_2()
        markup = types.InlineKeyboardMarkup()
        if result > character.mastery:
            item1 = [types.InlineKeyboardButton('Go on', callback_data='227')]
            markup.add(*item1)
            await bot.send_message(callback_query.from_user.id, text.text_190, reply_markup=markup)
        else:
            item1 = [types.InlineKeyboardButton('Go on', callback_data='282')]
            markup.add(*item1)
            await bot.send_message(callback_query.from_user.id, text.text_190, reply_markup=markup)
    elif flag190 == 1:
        text_message = 'Часу на роздуми нема'
        if flag190_2 == 2:
            text_message = text.text_190_2
        markup = types.InlineKeyboardMarkup()
        item1 = [types.InlineKeyboardButton("Почати бійку", callback_data="fight")]
        markup.add(*item1)
        await bot.send_message(callback_query.from_user.id, text_message, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == 'deduct_2_endurance')
async def text_190_1(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    m1, m2 = 'Наступний удар', 'Випробувати Удачу'
    Functions.Functions.change_1_data(user_id, 'e_endurance_190', 'user_id', 2, multiplier=-1)
    character_data = Functions.DB.retrieve_character_data(user_id)
    character = Functions.Functions.Character(mastery=character_data[0], endurance=character_data[1],
                                              luck=character_data[2])
    creature_data = Functions.DB.retrieve_creature_data(user_id, f'e_mastery_190', 'e_endurance_190')
    creature = Functions.Functions.Character(mastery=creature_data[0], endurance=creature_data[1],
                                             luck=creature_data[2])
    markup = types.InlineKeyboardMarkup(row_width=2)
    if character.luck > 0 and creature.endurance > 0:
        item1 = [types.InlineKeyboardButton(m1, callback_data='fight'),
                 types.InlineKeyboardButton(m2, callback_data='way2')]
        markup.add(*item1)
        await bot.send_message(user_id,
                               f"Player damages the creature! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                               reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
    elif character.luck <= 0 and creature.endurance > 0:  # якщо відсутня можливість перевірити Удачу, але суперник ще живий
        item1 = [types.InlineKeyboardButton(m1, callback_data='4 rounds')]
        markup.add(*item1)
        await bot.send_message(user_id,
                               f"Player damages the creature! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                               reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
    elif creature.endurance <= 0:
        item1 = [types.InlineKeyboardButton('Go on', callback_data='309')]
        markup.add(*item1)
        await bot.send_message(user_id, 'The player wins!', reply_markup=markup, parse_mode='Markdown')


@dp.callback_query_handler(lambda c: c.data == 'decrease_mastery')
async def text_190_2(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    m1, m2 = 'Наступний удар', 'Випробувати Удачу'
    Functions.Functions.change_1_data(user_id, 'e_mastery_190', 'user_id', 1, multiplier=-1)
    character_data = Functions.DB.retrieve_character_data(user_id)
    character = Functions.Functions.Character(mastery=character_data[0], endurance=character_data[1],
                                              luck=character_data[2])
    creature_data = Functions.DB.retrieve_creature_data(user_id, f'e_mastery_190', 'e_endurance_190')
    creature = Functions.Functions.Character(mastery=creature_data[0], endurance=creature_data[1],
                                             luck=creature_data[2])
    markup = types.InlineKeyboardMarkup(row_width=2)
    if character.luck > 0 and creature.endurance > 0:
        item1 = [types.InlineKeyboardButton(m1, callback_data='fight'),
                 types.InlineKeyboardButton(m2, callback_data='way2')]
        markup.add(*item1)
        await bot.send_message(user_id,
                               f"Player damages the creature! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                               reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
    elif character.luck <= 0 and creature.endurance > 0:  # якщо відсутня можливість перевірити Удачу, але суперник ще живий
        item1 = [types.InlineKeyboardButton(m1, callback_data='4 rounds')]
        markup.add(*item1)
        await bot.send_message(user_id,
                               f"Player damages the creature! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                               reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
    elif creature.endurance <= 0:
        item1 = [types.InlineKeyboardButton('Go on', callback_data='309')]
        markup.add(*item1)
        await bot.send_message(user_id, 'The player wins!', reply_markup=markup, parse_mode='Markdown')


@dp.callback_query_handler(lambda c: c.data == '191')
async def text_191(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 191)
    Functions.Functions.change_1_data(user_id, 'Mastery', 'user_id', 1, multiplier=-1)

    endurance = Functions.DB.select_one_value(user_id, 'Endurance', 'user_id')
    max_endurance = Functions.DB.select_one_value(user_id, 'max_endurance', 'user_id')

    if endurance < max_endurance:
        add_value = math.ceil(min(endurance / 2, max_endurance - endurance))
        Functions.Functions.change_1_data(user_id, 'Endurance', 'user_id', add_value)

    buttons_data = [
        ("Вивчити можливість роздобути меч", "273"),
        ('Спробувати дізнатися про місцезнаходження с/г станції', "173")
    ]
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(*Functions.Functions.create_inline_buttons(*buttons_data))

    await bot.send_message(user_id, text.text_191, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '192')
async def text_192(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_game_over(callback_query, 192, text.text_192)


@dp.callback_query_handler(lambda c: c.data == '193')
async def text_193(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_move(callback_query, 193, "100", text.text_193)
    # user_id = callback_query.from_user.id
    # Functions.DB.update_one_value(user_id, 'text_number', 193)
    # markup = types.InlineKeyboardMarkup()
    # item1 = [types.InlineKeyboardButton("Go on", callback_data="100")]
    # markup.add(*item1)
    # await bot.send_message(user_id, text.text_193, reply_markup=markup, parse_mode='Markdown')
    # await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '194')
async def text_194(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 194)
    Functions.Functions.change_1_data(user_id, 'Luck', 'user_id', 1)

    buttons_data = [
        ("Одразу увійти всередину", "146"),
        ('Зачекати трохи зовні', "178")
    ]
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(*Functions.Functions.create_inline_buttons(*buttons_data))

    await bot.send_message(user_id, text.text_194, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '195')
async def text_195(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(callback_query.from_user.id, 'text_number', 195)
    markup = types.InlineKeyboardMarkup(row_width=1)
    if Functions.DB.is_cell_not_empty(user_id, 'brain_probe_355') or Functions.DB.is_cell_not_empty(user_id,
                                                                                                    'warder_355'):
        if Functions.DB.is_cell_not_empty(user_id, 'brain_probe_355') and Functions.DB.is_cell_not_empty(user_id,
                                                                                                         'warder_355'):
            text_message = text.text_195_1
            item1 = [types.InlineKeyboardButton('Палиця', callback_data="267"),
                     types.InlineKeyboardButton('Зонд', callback_data="226"),
                     types.InlineKeyboardButton("Не хочу відмовлятися ні від палиці, ні від зонду",
                                                callback_data="179")]
        elif Functions.DB.is_cell_not_empty(user_id, 'brain_probe_355'):
            text_message = text.text_195_2
            item1 = [types.InlineKeyboardButton('Зонд', callback_data="226"),
                     types.InlineKeyboardButton("Не хочу відмовлятися від зонду", callback_data="179")]
        elif Functions.DB.is_cell_not_empty(user_id, 'warder_355'):
            text_message = text.text_195_3
            item1 = [types.InlineKeyboardButton('Палиця', callback_data="267"),
                     types.InlineKeyboardButton("Не хочу відмовлятися від палиці", callback_data="179")]
    else:
        text_message = text.text_195_4
        item1 = [types.InlineKeyboardButton("Go on", callback_data="179")]

    markup.add(*item1)
    await bot.send_message(user_id, text_message, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '196')
async def text_196(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(callback_query.from_user.id, 'text_number', 196)
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = [types.InlineKeyboardButton('Зачекати, доки адміністратор помітить мене', callback_data="29"),
             types.InlineKeyboardButton("Повідомити про свою присутність", callback_data="188")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_196, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '197')
async def text_197(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 197)

    buttons_data = [
        ("Запитати про зброю", "217"),
        ('Спробувати отримати меч у аркадіанця', "16")
    ]
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(*Functions.Functions.create_inline_buttons(*buttons_data))

    await bot.send_message(user_id, text.text_197, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '198')
async def text_198(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(callback_query.from_user.id, 'text_number', 198)

    markup = types.InlineKeyboardMarkup(row_width=1)
    if Functions.DB.is_cell_not_empty(user_id, 'can_of_motor_oil_382') or Functions.DB.is_cell_not_empty(user_id,
                                                                                                         'manual_horn_382') or Functions.DB.is_cell_not_empty(
        user_id, 'stroboscope_382'):
        text_message = text.text_198
        if Functions.DB.is_cell_not_empty(user_id, 'can_of_motor_oil_382') and Functions.DB.is_cell_not_empty(user_id,
                                                                                                              'manual_horn_382') and Functions.DB.is_cell_not_empty(
            user_id, 'stroboscope_382'):
            item1 = [types.InlineKeyboardButton('Банка моторного масла', callback_data="256"),
                     types.InlineKeyboardButton('Ручний клаксон', callback_data="21"),
                     types.InlineKeyboardButton("Стробоскоп", callback_data="79"),
                     types.InlineKeyboardButton("Повернутися на 366", callback_data="366"),
                     types.InlineKeyboardButton("Повернутися на 295", callback_data="295")]
        elif Functions.DB.is_cell_not_empty(user_id, 'can_of_motor_oil_382') and Functions.DB.is_cell_not_empty(user_id,
                                                                                                                'manual_horn_382'):
            item1 = [types.InlineKeyboardButton('Банка моторного масла', callback_data="256"),
                     types.InlineKeyboardButton('Ручний клаксон', callback_data="21"),
                     types.InlineKeyboardButton("Повернутися на 366", callback_data="366"),
                     types.InlineKeyboardButton("Повернутися на 295", callback_data="295")]
        elif Functions.DB.is_cell_not_empty(user_id, 'can_of_motor_oil_382') and Functions.DB.is_cell_not_empty(
                user_id, 'stroboscope_382'):
            item1 = [types.InlineKeyboardButton('Банка моторного масла', callback_data="256"),
                     types.InlineKeyboardButton("Стробоскоп", callback_data="79"),
                     types.InlineKeyboardButton("Повернутися на 366", callback_data="366"),
                     types.InlineKeyboardButton("Повернутися на 295", callback_data="295")]
        elif Functions.DB.is_cell_not_empty(user_id, 'manual_horn_382') and Functions.DB.is_cell_not_empty(user_id,
                                                                                                           'stroboscope_382'):
            item1 = [types.InlineKeyboardButton('Ручний клаксон', callback_data="21"),
                     types.InlineKeyboardButton("Стробоскоп", callback_data="79"),
                     types.InlineKeyboardButton("Повернутися на 366", callback_data="366"),
                     types.InlineKeyboardButton("Повернутися на 295", callback_data="295")]
        elif Functions.DB.is_cell_not_empty(user_id, 'can_of_motor_oil_382'):
            item1 = [types.InlineKeyboardButton('Банка моторного масла', callback_data="256"),
                     types.InlineKeyboardButton("Повернутися на 366", callback_data="366"),
                     types.InlineKeyboardButton("Повернутися на 295", callback_data="295")]
        elif Functions.DB.is_cell_not_empty(user_id, 'manual_horn_382'):
            item1 = [types.InlineKeyboardButton('Ручний клаксон', callback_data="21"),
                     types.InlineKeyboardButton("Повернутися на 366", callback_data="366"),
                     types.InlineKeyboardButton("Повернутися на 295", callback_data="295")]
        elif Functions.DB.is_cell_not_empty(user_id, 'stroboscope_382'):
            item1 = [types.InlineKeyboardButton("Стробоскоп", callback_data="79"),
                     types.InlineKeyboardButton("Повернутися на 366", callback_data="366"),
                     types.InlineKeyboardButton("Повернутися на 295", callback_data="295")]
    else:
        text_message = 'Поверніться на 366 або 295.'
        item1 = [types.InlineKeyboardButton("Повернутися на 366", callback_data="366"),
                 types.InlineKeyboardButton("Повернутися на 295", callback_data="295")]

    markup.add(*item1)
    await bot.send_message(user_id, text_message, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '199')
async def text_199(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_game_over(callback_query, 199, text.text_199)


@dp.callback_query_handler(lambda c: c.data == '200')
async def text_200(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 200)

    character_data = Functions.DB.retrieve_character_data(user_id)
    character = Functions.Functions.Character(mastery=character_data[0], endurance=character_data[1],
                                              luck=character_data[2])
    result = Functions.Functions.roll_dice_2()
    print(result)
    markup = types.InlineKeyboardMarkup()
    if result <= character.luck:
        item1 = [types.InlineKeyboardButton('Go on', callback_data="318")]
    else:
        item1 = [types.InlineKeyboardButton('Go on', callback_data="83")]
    Functions.Functions.change_1_data(user_id, 'Luck', 'user_id', 1, multiplier=-1)
    markup.add(*item1)
    await bot.send_message(user_id, text.text_200, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '201')
async def text_201(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 201)
    Functions.Functions.change_1_data(user_id, 'money', 'user_id', 500, multiplier=-1)

    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton('Go on', callback_data="85")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_201, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '202')
async def text_202(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 202)
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = [types.InlineKeyboardButton("Піти на Художній поверх", callback_data="258"),
             types.InlineKeyboardButton("Покинути університет", callback_data="235")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_202, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '203')
async def text_203(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_move(callback_query, 203, "177", text.text_203)
    # user_id = callback_query.from_user.id
    # Functions.DB.update_one_value(user_id, 'text_number', 203)
    # markup = types.InlineKeyboardMarkup()
    # item1 = [types.InlineKeyboardButton('Go on', callback_data="177")]
    # markup.add(*item1)
    # await bot.send_message(user_id, text.text_203, reply_markup=markup, parse_mode='Markdown')
    # await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '204')
async def text_204(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 204)
    markup = types.InlineKeyboardMarkup(row_width=2)
    item1 = [types.InlineKeyboardButton("SAROS", callback_data="287"),
             types.InlineKeyboardButton("Великий візир Тропоса", callback_data="45"),
             types.InlineKeyboardButton("Беллатрікс", callback_data="240"),
             types.InlineKeyboardButton("Ніхто, я з Землі", callback_data="326")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_204, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '205')
async def text_205(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_game_over(callback_query, 205, text.text_205)


@dp.callback_query_handler(lambda c: c.data == '206')
async def text_206(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 206)
    Functions.DB.update_add_enemy(user_id, 7, 8, 'e_mastery_206', 'e_endurance_206')
    result = random.randint(1, 6)
    markup = types.InlineKeyboardMarkup()
    if result == 6:
        Functions.DB.update_one_value(user_id, 'sword', 1)
        text_message = 'Вам вдається вивести охоронця з ладу з першого удару. Ви берете собі його меч.'
        item1 = [types.InlineKeyboardButton("Go on", callback_data="131")]
    else:
        text_message = text.text_206
        item1 = [types.InlineKeyboardButton("Продовжити бійку", callback_data="fight")]
    markup.add(*item1)
    await bot.send_message(callback_query.from_user.id, text_message, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '207')
async def text_207(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 207)
    Functions.Functions.change_1_data(user_id, 'Endurance', 'user_id', 2, multiplier=-1)
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = [
        types.InlineKeyboardButton("Спробувати переконати їх", callback_data="168"),
        types.InlineKeyboardButton("Попросити їх самих довести свою особистість", callback_data="105")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_207, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '208')
async def text_208(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 208)
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = [types.InlineKeyboardButton("Покинути цю витівку", callback_data="327"),
             types.InlineKeyboardButton("Продовжити рух у гущавину листя", callback_data="161")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_208, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '209')
async def text_209(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 209)
    Functions.Functions.change_1_data(user_id, 'Luck', 'user_id', 2, multiplier=-1)
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = [types.InlineKeyboardButton("Go on", callback_data="74")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_209, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '210')
async def text_210(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 210)
    result = random.randint(1, 6)
    markup = types.InlineKeyboardMarkup(row_width=1)
    if result < 3:
        item1 = [types.InlineKeyboardButton("Go on", callback_data="396")]
    else:
        item1 = [types.InlineKeyboardButton("Go on", callback_data="160")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_210, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '211')
async def text_211(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 211)
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = [types.InlineKeyboardButton("Запропонувати їм ще трохи грошей", callback_data="91"),
             types.InlineKeyboardButton("Зачекати", callback_data="72")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_211, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '212')
async def text_212(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 212)
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = [types.InlineKeyboardButton("Cпробувати дізнатися більше", callback_data="290"),
             types.InlineKeyboardButton("Зачекати на більш слушний момент", callback_data="247")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_212, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '213')
async def text_213(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 213)
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = [types.InlineKeyboardButton("Дозволяю аркадіанцю втекти", callback_data="200"),
             types.InlineKeyboardButton("Не дозволяю аркадіанцю втекти", callback_data="318")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_213, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '214')
async def text_214(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 214)
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = [types.InlineKeyboardButton("Напасти на нього", callback_data="107"),
             types.InlineKeyboardButton("Вони, мабуть, не варті такого ризику", callback_data="58")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_214, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '215')
async def text_215(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_1_fight(callback_query, 215, 7, 8, "fight", text.text_215)
    # user_id = callback_query.from_user.id
    # Functions.DB.update_one_value(user_id, 'text_number', 215)
    # Functions.DB.update_add_enemy(user_id, 7, 8, 'e_mastery_215', 'e_endurance_215')
    # markup = types.InlineKeyboardMarkup()
    # item1 = [types.InlineKeyboardButton("Почати бійку", callback_data="fight")]
    # markup.add(*item1)
    # await bot.send_message(callback_query.from_user.id, text.text_215, reply_markup=markup, parse_mode='Markdown')
    # await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == 'take_grenade_215')
async def text_215_1(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'grenade_110_215', 1)
    text_message = 'Тепер у вас є граната.'
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("Go on", callback_data="320")]
    markup.add(*item1)
    await bot.send_message(callback_query.from_user.id, text_message, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '216')
async def text_216(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 216)

    character_data = Functions.DB.retrieve_character_data(user_id)
    character = Functions.Functions.Character(mastery=character_data[0], endurance=character_data[1],
                                              luck=character_data[2])
    result = Functions.Functions.roll_dice_2()
    print(result)
    markup = types.InlineKeyboardMarkup()
    if result <= character.luck:
        item1 = [types.InlineKeyboardButton('Go on', callback_data="323")]
    else:
        item1 = [types.InlineKeyboardButton('Go on', callback_data="389")]
    Functions.Functions.change_1_data(user_id, 'Luck', 'user_id', 1, multiplier=-1)
    markup.add(*item1)
    await bot.send_message(user_id, text.text_216, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '217')
async def text_217(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 217)
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = [types.InlineKeyboardButton("Піти з ним", callback_data="399"),
             types.InlineKeyboardButton("Спробувати знайти меч в іншому місці", callback_data="137")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_217, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '218')
async def text_218(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 218)
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = [types.InlineKeyboardButton("Піти на Художній поверх", callback_data="258"),
             types.InlineKeyboardButton("Залишити університет", callback_data="235")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_218, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '219')
async def text_219(callback_query: types.CallbackQuery):
    photo_path = 'table_219.jpg'

    # Send the photo
    await bot.send_photo(callback_query.from_user.id, photo=open(photo_path, 'rb'))

    await Functions.Functions.handle_move(callback_query, 219, "check_219", text.text_219)

    # Functions.DB.update_one_value(user_id, 'text_number', 219)
    # markup = types.InlineKeyboardMarkup(row_width=1)
    # item1 = [types.InlineKeyboardButton("Go on", callback_data="check_219")]
    # markup.add(*item1)
    # await bot.send_message(user_id, text.text_219, reply_markup=markup, parse_mode='Markdown')
    # await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == 'check_219')
async def text_check_219_callback(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_text = 'Введіть номер параграфу.'
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("Не знаю номеру параграфу", callback_data="death_219")]
    markup.add(*item1)
    await bot.send_message(user_id, message_text, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == 'death_219')
async def text_death_219(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_game_over(callback_query, 219, text.text_219_1)


# @dp.message_handler(text='111111111111111')
# async def paragraph_262(message: types.Message, state: FSMContext):
#     print('paragraph_262')
#     markup = types.InlineKeyboardMarkup()
#     markup.add(types.InlineKeyboardButton("Перевірити Удачу", callback_data="luck_262"))
#     await bot.send_message(message.chat.id, text.text_262, reply_markup=markup)


@dp.callback_query_handler(lambda c: c.data == '220')
async def text_220(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 220)
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = [types.InlineKeyboardButton("Go on", callback_data="78")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_220, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '221')
async def text_221(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 221)
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = [types.InlineKeyboardButton("Повернути на схід", callback_data="186"),
             types.InlineKeyboardButton("Повернути на захід", callback_data="324")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_221, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '222')
async def text_222(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_move(callback_query, 222, "400", text.text_222)
    # user_id = callback_query.from_user.id
    # Functions.DB.update_one_value(user_id, 'text_number', 222)
    # markup = types.InlineKeyboardMarkup(row_width=1)
    # item1 = [types.InlineKeyboardButton("Go on", callback_data="400")]
    # markup.add(*item1)
    # await bot.send_message(user_id, text.text_222, reply_markup=markup, parse_mode='Markdown')
    # await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '223')
async def text_223(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 223)
    Functions.Functions.change_1_data(user_id, 'money', 'user_id', 500, multiplier=-1)
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = [types.InlineKeyboardButton("Go on", callback_data="132")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_223, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '224')
async def text_224(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 224)
    Functions.DB.update_one_value(user_id, 'without_weapons', 2)
    Functions.DB.update_add_enemy(user_id, 6, 10, 'e_mastery_224', 'e_endurance_224')
    Functions.Functions.change_1_data(user_id, 'Mastery', 'user_id', 1, multiplier=-1)
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("Почати бійку", callback_data="fight")]
    markup.add(*item1)
    await bot.send_message(callback_query.from_user.id, text.text_224, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == 'take_sword_224')
async def text_224_1(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'sword', 1)
    Functions.DB.update_one_value(user_id, 'without_weapons', 1)
    Functions.Functions.change_1_data(user_id, 'Mastery', 'user_id', 1)
    text_message = 'Тепер у вас є меч.'
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("Go on", callback_data="336")]
    markup.add(*item1)
    await bot.send_message(callback_query.from_user.id, text_message, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '225')
async def text_225(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 225)
    Functions.Functions.change_1_data(user_id, 'Endurance', 'user_id', 2, multiplier=-1)
    Functions.Functions.change_1_data(user_id, 'Luck', 'user_id', 1)
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = [types.InlineKeyboardButton("Go on", callback_data="207")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_225, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '226')
async def text_226(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 226)
    Functions.DB.clear_cell(user_id, 'brain_probe_355')
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = [types.InlineKeyboardButton("У мене нема посоха", callback_data="179")]
    text_message = text.text_226_1
    if Functions.DB.is_cell_not_empty(user_id, 'warder_355'):
        item1 = [types.InlineKeyboardButton("Віддати посох", callback_data="267"),
                 types.InlineKeyboardButton("Не хочу віддавати посох", callback_data="179")]
        text_message = text.text_226_2
    markup.add(*item1)
    await bot.send_message(user_id, text_message, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '227')
async def text_227(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 227)
    Functions.DB.update_one_value(user_id, 'flag190_2', 1)
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("Go on", callback_data="190")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_227, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '228')
async def text_228(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 228)
    Functions.Functions.change_1_data(user_id, 'Endurance', 'user_id', 2, multiplier=-1)
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = [types.InlineKeyboardButton("Go on", callback_data="46")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_228, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '229')
async def text_229(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 229)
    result = random.randint(1, 6)
    markup = types.InlineKeyboardMarkup(row_width=1)
    if result < 3:
        item1 = [types.InlineKeyboardButton("Go on", callback_data="211")]
    else:
        item1 = [types.InlineKeyboardButton("Go on", callback_data="113")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_229, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '230')
async def text_230(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 230)
    Functions.Functions.change_1_data(user_id, 'Luck', 'user_id', 1)
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = [types.InlineKeyboardButton("Зізнатися, що Муска зі мною", callback_data="361"),
             types.InlineKeyboardButton("Не зізнаватися, що Муска зі мною", callback_data="379")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_230, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '231')
async def text_231(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 231)
    Functions.Functions.change_1_data(user_id, 'Luck', 'user_id', 1)
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = [types.InlineKeyboardButton("Go on", callback_data="313")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_231, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '232')
async def text_232(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 232)
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton('Перевірити Удачу', callback_data="check_luck_232")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_232, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == 'check_luck_232')
async def check_luck_232(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    character_data = Functions.DB.retrieve_character_data_id(1)
    character = Functions.Functions.Character(mastery=character_data[0], endurance=character_data[1],
                                              luck=character_data[2])
    if character.luck > 0:
        markup = types.InlineKeyboardMarkup()
        item1 = [types.InlineKeyboardButton('Go on', callback_data='147')]
        text_message = 'Вам пощастило, ви легко спускаєтеся вниз по скелі.'
        if not Functions.Functions.if_luck(character.luck):
            text_message = 'Вам не пощастило, наприкінці ви падаєте і втрачаєте 2 бали Витривалості.'
            Functions.Functions.change_1_data(user_id, 'Endurance', 'user_id', 2, multiplier=-1)
        markup.add(*item1)
        Functions.Functions.change_1_data(user_id, 'Luck', 'user_id', 1, multiplier=-1)
    await bot.send_message(user_id, text_message, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '233')
async def text_233(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 233)
    Functions.Functions.change_1_data(user_id, 'Endurance', 'user_id', 1, multiplier=-1)
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = [types.InlineKeyboardButton("Намагатися чинити опір", callback_data="156"),
             types.InlineKeyboardButton("Занадто втомлений, щоб чинити опір", callback_data="272")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_233, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '234')
async def text_234(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 234)
    Functions.DB.update_add_enemy(user_id, 6, 8, 'e_mastery_234_1', 'e_endurance_234_1')
    Functions.DB.update_add_enemy(user_id, 6, 6, 'e_mastery_234_2', 'e_endurance_234_2')
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("Аркадіанець житель півночі", callback_data="first_a_n"),
             types.InlineKeyboardButton("Другий аркадіанець", callback_data="second_a_2")]
    markup.add(*item1)
    await bot.send_message(callback_query.from_user.id, text.text_234, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == 'first_a_n')
async def text_234_1(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'flag234', 1)
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("До бою", callback_data="fight")]
    markup.add(*item1)
    await bot.send_message(user_id, "Ти обираєш битися з жителем півночі", reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == 'second_a_2')
async def text_234_2(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'flag234', 2)
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("До бою", callback_data="fight")]
    markup.add(*item1)
    await bot.send_message(user_id, "Ти обираєш битися з другим аркадіанцем", reply_markup=markup,
                           parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '235')
async def text_235(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 235)
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = [types.InlineKeyboardButton("Вийти на наступній станції пересадки", callback_data="162"),
             types.InlineKeyboardButton("Продовжити шлях до готелю", callback_data="27")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_235, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '236')
async def text_236(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 236)
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = [types.InlineKeyboardButton("Атакувати робота", callback_data="179"),
             types.InlineKeyboardButton("Спробувати поговорити з роботом", callback_data="195")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_236, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '237')
async def text_237(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 237)
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = [types.InlineKeyboardButton("Відповісти на образу", callback_data="35"),
             types.InlineKeyboardButton("Поступово випити келих", callback_data="322")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_237, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '238')
async def text_238(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 238)
    Functions.DB.update_one_value(user_id, 'number_238', 1)

    character_data = Functions.DB.retrieve_character_data_id(1)
    character = Functions.Functions.Character(mastery=character_data[0], endurance=character_data[1],
                                              luck=character_data[2])
    if character.luck > 0:
        for i in range(3):
            if Functions.Functions.if_luck(character.luck):
                Functions.Functions.change_1_data(user_id, 'number_238', 'user_id', 1)
                time.sleep(0.5)
        number_238 = Functions.DB.select_one_value(user_id, 'number_238', 'user_id')
        markup = types.InlineKeyboardMarkup()
        item1 = [types.InlineKeyboardButton('Go on', callback_data='165')]
        if number_238 == 4:
            item1 = [types.InlineKeyboardButton('Go on', callback_data='96')]
        markup.add(*item1)
        Functions.Functions.change_1_data(user_id, 'Luck', 'user_id', 1, multiplier=-1)
    else:
        pass
    await bot.send_message(user_id, text.text_238, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '239')
async def text_239(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 239)
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = [types.InlineKeyboardButton("Відвідати його лекцію", callback_data="170"),
             types.InlineKeyboardButton("Випити чашку кави у студентській їдальні", callback_data="182")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_239, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '240')
async def text_240(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 240)
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = [types.InlineKeyboardButton("Виконати те, що сказав брамник", callback_data="95"),
             types.InlineKeyboardButton("Спробувати розрубати замок на дверях своїм мечем", callback_data="366")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_240, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '241')
async def text_241(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_move(callback_query, 241, "278", text.text_241)
    # user_id = callback_query.from_user.id
    # Functions.DB.update_one_value(user_id, 'text_number', 241)
    # markup = types.InlineKeyboardMarkup(row_width=1)
    # item1 = [types.InlineKeyboardButton("Go on", callback_data="278")]
    # markup.add(*item1)
    # await bot.send_message(user_id, text.text_241, reply_markup=markup, parse_mode='Markdown')
    # await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '242')
async def text_242(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 242)
    character_data = Functions.DB.retrieve_character_data(user_id)
    character = Functions.Functions.Character(mastery=character_data[0], endurance=character_data[1],
                                              luck=character_data[2])
    if character.luck > 0:
        markup = types.InlineKeyboardMarkup()
        item1 = [types.InlineKeyboardButton('Go on', callback_data='132')]
        if not Functions.Functions.if_luck(character.luck):
            item1 = [types.InlineKeyboardButton('Go on', callback_data='52')]
        markup.add(*item1)
        Functions.Functions.change_1_data(user_id, 'Luck', 'user_id', 1, multiplier=-1)
    await bot.send_message(user_id, text.text_242, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '243')
async def text_243(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 243)
    Functions.DB.update_add_enemy(user_id, 7, 8, 'e_mastery_243', 'e_endurance_243')
    Functions.DB.update_one_value(user_id, 'sand243', 1)
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("Почати бійку", callback_data="fight")]
    markup.add(*item1)
    await bot.send_message(callback_query.from_user.id, text.text_243, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '244')
async def text_244(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 244)
    Functions.DB.update_add_enemy(user_id, 6, 8, 'e_mastery_244_1', 'e_endurance_244_1')
    Functions.DB.update_add_enemy(user_id, 5, 6, 'e_mastery_244_2', 'e_endurance_244_2')
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("Перший громила", callback_data="first_h"),
             types.InlineKeyboardButton("Другий громила", callback_data="second_h")]
    markup.add(*item1)
    await bot.send_message(callback_query.from_user.id, text.text_244, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == 'first_h')
async def text_244_1(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'flag244', 1)
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("До бою", callback_data="fight")]
    markup.add(*item1)
    await bot.send_message(user_id, "Ти обираєш битися з першим громилою", reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == 'second_h')
async def text_244_2(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'flag244', 2)
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("До бою", callback_data="fight")]
    markup.add(*item1)
    await bot.send_message(user_id, "Ти обираєш битися з другим громилою", reply_markup=markup,
                           parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '245')
async def text_245(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 245)
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = [types.InlineKeyboardButton("Увійти в праву печеру", callback_data="371"),
             types.InlineKeyboardButton("Увійти в ліву печеру", callback_data="294")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_245, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '246')
async def text_246(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 246)
    character_data = Functions.DB.retrieve_character_data(user_id)
    character = Functions.Functions.Character(mastery=character_data[0], endurance=character_data[1],
                                              luck=character_data[2])
    if character.luck > 0:
        markup = types.InlineKeyboardMarkup()
        item1 = [types.InlineKeyboardButton('Перевірити Удачу', callback_data='144')]
        if not Functions.Functions.if_luck(character.luck):  # якщо не пощастило
            item1 = [types.InlineKeyboardButton('Перевірити Удачу', callback_data='129')]
        markup.add(*item1)
        Functions.Functions.change_1_data(user_id, 'Luck', 'user_id', 1, multiplier=-1)
    await bot.send_message(user_id, text.text_246, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '247')
async def text_247(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_game_over(callback_query, 247, text.text_247)


@dp.callback_query_handler(lambda c: c.data == '248')
async def text_248(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 248)
    Functions.Functions.change_1_data(user_id, 'Luck', 'user_id', 1, multiplier=-1)
    Functions.Functions.change_1_data(user_id, 'Mastery', 'user_id', 1, multiplier=-1)
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = [types.InlineKeyboardButton("Go on", callback_data="289")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_248, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '249')
async def text_249(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 249)
    Functions.Functions.change_1_data(user_id, 'Endurance', 'user_id', 1, multiplier=-1)
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = [types.InlineKeyboardButton("Go on", callback_data="336")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_249, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '250')
async def text_250(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_game_over(callback_query, 250, text.text_250)


@dp.callback_query_handler(lambda c: c.data == '251')
async def text_251(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 251)
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = [types.InlineKeyboardButton("Подивитися на екран", callback_data="319"),
             types.InlineKeyboardButton("Продовжити свій шлях", callback_data="375")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_251, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '252')
async def text_252(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 252)
    character_data = Functions.DB.retrieve_character_data(user_id)
    character = Functions.Functions.Character(mastery=character_data[0], endurance=character_data[1],
                                              luck=character_data[2])
    if character.luck > 0:
        markup = types.InlineKeyboardMarkup()
        item1 = [types.InlineKeyboardButton('Go on', callback_data='233')]
        if not Functions.Functions.if_luck(character.luck):
            item1 = [types.InlineKeyboardButton('Go on', callback_data='330')]
        markup.add(*item1)
        Functions.Functions.change_1_data(user_id, 'Luck', 'user_id', 1, multiplier=-1)
    await bot.send_message(user_id, text.text_252, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '253')
async def text_253(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 253)
    Functions.DB.update_one_value(user_id, 'jetpack_253', 1)
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("Go on", callback_data="336")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_253, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '254')
async def text_254(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 254)
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = [types.InlineKeyboardButton("Повернути туди", callback_data="62"),
             types.InlineKeyboardButton("Продовжити йти прямо", callback_data="39")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_254, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '255')
async def text_255(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 255)
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("Знаю пароль", callback_data="check_255"),
             types.InlineKeyboardButton("Не знаю пароль", callback_data="death_255")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_255_1, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == 'check_255')
async def text_check_255_callback(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_text = 'Введіть пароль або зізнайтеся, що не знаєте паролю.'
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("Не знаю пароль", callback_data="death_255")]
    markup.add(*item1)
    await bot.send_message(user_id, message_text, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == 'death_255')
async def text_death_255(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_game_over(callback_query, 255, text.text_255_2)


@dp.message_handler(text='155')
async def paragraph_155(message: types.Message, state: FSMContext):
    print('paragraph_155')
    user_id = message.chat.id
    Functions.DB.update_one_value(user_id, 'text_number', 155)
    Functions.Functions.change_1_data(user_id, 'Luck', 'user_id', 1)
    Functions.DB.update_one_value(user_id, 'uniform_155', 1)
    Functions.Functions.change_1_data(user_id, 'Endurance', 'user_id', 4)
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("Go on", callback_data="163")]
    markup.add(*item1)
    await bot.send_message(message.chat.id, text.text_155, reply_markup=markup)


@dp.callback_query_handler(lambda c: c.data == '256')
async def text_256(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 256)

    paragraph_mapping = {
        366: 'e_mastery_366_1',
        295: 'e_mastery_295_1'
    }

    paragraph = Functions.DB.select_one_value(user_id, 'p_366_or_295', 'user_id')
    if paragraph not in paragraph_mapping:
        return  # handle the case where paragraph is not in the mapping

    Functions.Functions.change_1_data(user_id, paragraph_mapping[paragraph], 'user_id', 2, multiplier=-1)

    item1 = [
        types.InlineKeyboardButton("Використати ручний клаксон", callback_data="21"),
        types.InlineKeyboardButton("Використати стробоскоп", callback_data="79"),
        types.InlineKeyboardButton("Не використовувати ці предмети", callback_data=str(paragraph))
    ]

    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(*item1)
    await bot.send_message(user_id, text.text_256, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '257')
async def text_257(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 257)
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = [types.InlineKeyboardButton("Втікати прямо", callback_data="186"),
             types.InlineKeyboardButton("Втікати на північ", callback_data="142")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_257, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '258')
async def text_258(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 258)
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = [types.InlineKeyboardButton("Знаю про когось на цьому поверсі", callback_data="check_258"),
             types.InlineKeyboardButton("76", callback_data="76")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_258, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == 'check_258')
async def text_check_258_callback(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_text = 'Введіть номер кабінету або переходьте до 76, якщо не знаєте номеру параграфу'
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("Не знаю номеру кабінету. ", callback_data="76")]
    markup.add(*item1)
    await bot.send_message(user_id, message_text, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.message_handler(text='239')
async def paragraph_239(message: types.Message, state: FSMContext):
    print('paragraph_239')
    user_id = message.chat.id
    Functions.DB.update_one_value(user_id, 'text_number', 239)
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = [types.InlineKeyboardButton("Відвідати його лекцію", callback_data="170"),
             types.InlineKeyboardButton("Випити чашку кави у студентській їдальні", callback_data="182")]
    markup.add(*item1)
    await bot.send_message(message.chat.id, text.text_239, reply_markup=markup)


@dp.callback_query_handler(lambda c: c.data == '259')
async def text_259(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 259)
    character_data = Functions.DB.retrieve_character_data(user_id)
    character = Functions.Functions.Character(mastery=character_data[0], endurance=character_data[1],
                                              luck=character_data[2])
    if character.luck > 0:
        markup = types.InlineKeyboardMarkup()
        item1 = [types.InlineKeyboardButton('Перевірити Удачу', callback_data='228')]
        if not Functions.Functions.if_luck(character.luck):
            item1 = [types.InlineKeyboardButton('Перевірити Удачу', callback_data='288')]
        markup.add(*item1)
        Functions.Functions.change_1_data(user_id, 'Luck', 'user_id', 1, multiplier=-1)
    await bot.send_message(user_id, text.text_259, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '260')
async def text_260(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 260)
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = [types.InlineKeyboardButton("1,5 квартали на північ, а потім 2 квартали на захід", callback_data="204"),
             types.InlineKeyboardButton("2,5 квартали на північ, а потім 2 квартали на захід", callback_data="109")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_260, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '261')
async def text_261(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 261)
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = [types.InlineKeyboardButton("Підскочити до нього і спробувати вирвати зброю", callback_data="59"),
             types.InlineKeyboardButton("Поговорити з ним", callback_data="90")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_261, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '262')
async def text_262(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 262)
    character_data = Functions.DB.retrieve_character_data(user_id)
    character = Functions.Functions.Character(mastery=character_data[0], endurance=character_data[1],
                                              luck=character_data[2])
    if character.luck > 0:
        markup = types.InlineKeyboardMarkup()
        item1 = [types.InlineKeyboardButton('Go on', callback_data='341')]
        if not Functions.Functions.if_luck(character.luck):
            item1 = [types.InlineKeyboardButton('Go on', callback_data='133')]
        markup.add(*item1)
        Functions.Functions.change_1_data(user_id, 'Luck', 'user_id', 1, multiplier=-1)
    await bot.send_message(user_id, text.text_262, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '263')
async def text_263(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 263)
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = [types.InlineKeyboardButton("Піти на схід", callback_data="245"),
             types.InlineKeyboardButton("Піти на північ", callback_data="342"),
             types.InlineKeyboardButton("Піти на південь", callback_data="181")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_263, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '264')
async def text_264(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 264)
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("225", callback_data="225"),
             types.InlineKeyboardButton("250", callback_data="250")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_264, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '265')
async def text_265(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 265)
    character_data = Functions.DB.retrieve_character_data(user_id)
    character = Functions.Functions.Character(mastery=character_data[0], endurance=character_data[1],
                                              luck=character_data[2])
    if character.luck > 0:
        markup = types.InlineKeyboardMarkup()
        item1 = [types.InlineKeyboardButton('Go on', callback_data='69')]
        if not Functions.Functions.if_luck(character.luck):  # якщо не пощастило
            item1 = [types.InlineKeyboardButton('Go on', callback_data='36')]
        markup.add(*item1)
        Functions.Functions.change_1_data(user_id, 'Luck', 'user_id', 1, multiplier=-1)
    await bot.send_message(user_id, text.text_265, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '266')
async def text_266(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 266)
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("Взяти участь у розмові", callback_data="218"),
             types.InlineKeyboardButton("Промовчати", callback_data="11")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_266, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '267')
async def text_267(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 267)
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = [types.InlineKeyboardButton("Посох зламано", callback_data="179"),
             types.InlineKeyboardButton("Посох не зламано", callback_data="308")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_267, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '268')
async def text_268(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 268)
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = [types.InlineKeyboardButton("Сказати йому, що вам краще залишатися одному", callback_data="314"),
             types.InlineKeyboardButton("Піти з ним", callback_data="394")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_268, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '269')
async def text_269(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 269)
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = [types.InlineKeyboardButton("Спробувати перепрограмувати комп'ютер", callback_data="205"),
             types.InlineKeyboardButton("Вийти з цієї кімнати", callback_data="94")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_269, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '270')
async def text_270(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 270)
    money = Functions.DB.select_one_value(user_id, 'money', 'user_id')
    bracelet = Functions.DB.select_one_value(user_id, 'bracelet_ziridium_117', 'user_id')
    markup = types.InlineKeyboardMarkup(row_width=1)
    if bracelet and money >= 500:
        message_text = text.text_270_1
        item1 = [types.InlineKeyboardButton("Запропонувати йому 500 кредитів", callback_data="201"),
                 types.InlineKeyboardButton("Запропонувати йому браслет із зірідієвим покриттям", callback_data="365"),
                 types.InlineKeyboardButton("Вирушити до університету", callback_data="146")]
    elif bracelet and money < 500:
        message_text = text.text_270_2
        item1 = [types.InlineKeyboardButton("Запропонувати йому браслет із зірідієвим покриттям", callback_data="365"),
                 types.InlineKeyboardButton("Вирушити до університету", callback_data="146")]
    elif not bracelet and money >= 500:
        message_text = text.text_270_3
        item1 = [types.InlineKeyboardButton("Запропонувати йому 500 кредитів", callback_data="201"),
                 types.InlineKeyboardButton("Вирушити до університету", callback_data="146")]
    elif not bracelet and money < 500:
        message_text = text.text_270_4
        item1 = [types.InlineKeyboardButton("Go on", callback_data="146")]
    markup.add(*item1)
    await bot.send_message(user_id, message_text, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '271')
async def text_271(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 271)

    result = random.randint(1, 6)
    next_callback_data = "234" if result % 2 == 0 else "24"

    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = [types.InlineKeyboardButton("Go on", callback_data=next_callback_data)]
    markup.add(*item1)

    await bot.send_message(user_id, text.text_271, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '272')
async def text_272(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_move(callback_query, 272, "207", text.text_272)
    # user_id = callback_query.from_user.id
    # Functions.DB.update_one_value(user_id, 'text_number', 272)
    # markup = types.InlineKeyboardMarkup(row_width=1)
    # item1 = [types.InlineKeyboardButton("Go on", callback_data="207")]
    # markup.add(*item1)
    # await bot.send_message(user_id, text.text_272, reply_markup=markup, parse_mode='Markdown')
    # await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '273')
async def text_273(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 273)

    buttons_data = [
        ('Запитати про меч в когось у сірому', "197"),
        ('Запитати про меч в когось у синьому', "217"),
        ('Спробувати роздобути меч у аркадіанця', "16")
    ]
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(*Functions.Functions.create_inline_buttons(*buttons_data))

    await bot.send_message(user_id, text.text_273, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '274')
async def text_274(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 274)

    buttons_data = [
        ('Сказати, що знаю, що бармен не подвійний агент', "307"),
        ('Мені потрібні докази його провини', "343")
    ]
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(*Functions.Functions.create_inline_buttons(*buttons_data))

    await bot.send_message(user_id, text.text_274, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '275')
async def text_275(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 275)
    Functions.Functions.change_1_data(user_id, 'Luck', 'user_id', 1, multiplier=-1)
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = [types.InlineKeyboardButton("Go on", callback_data="114")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_275, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '276')
async def text_276(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 276)

    buttons_data = [
        ('Спробувати натиснути кнопку зліва', "180"),
        ('Спробувати натиснути кнопку справа', "386")
    ]
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(*Functions.Functions.create_inline_buttons(*buttons_data))

    await bot.send_message(user_id, text.text_276, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '277')
async def text_277(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_move(callback_query, 277, "346", text.text_277)
    # user_id = callback_query.from_user.id
    # Functions.DB.update_one_value(user_id, 'text_number', 277)
    # markup = types.InlineKeyboardMarkup(row_width=1)
    # item1 = [types.InlineKeyboardButton("Go on", callback_data="346")]
    # markup.add(*item1)
    # await bot.send_message(user_id, text.text_277, reply_markup=markup, parse_mode='Markdown')
    # await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '278')
async def text_278(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 278)
    Functions.Functions.change_1_data(user_id, 'Endurance', 'user_id', 2)
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = [types.InlineKeyboardButton("Go on", callback_data="292")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_278, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '279')
async def text_279(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 279)

    buttons_data = [
        ('Піти на схід', "245"),
        ('Піти на північ', "342"),
        ('Піти на південь', "181")
    ]
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(*Functions.Functions.create_inline_buttons(*buttons_data))

    await bot.send_message(user_id, text.text_279, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '280')
async def text_280(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 280)

    buttons_data = [
        ('Відмовитися від напою', "237"),
        ('Прийняти напій', "322")
    ]
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(*Functions.Functions.create_inline_buttons(*buttons_data))

    await bot.send_message(user_id, text.text_280, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '281')
async def text_281(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 281)
    character_data = Functions.DB.retrieve_character_data(user_id)
    character = Functions.Functions.Character(mastery=character_data[0], endurance=character_data[1],
                                              luck=character_data[2])
    if character.luck > 0:
        markup = types.InlineKeyboardMarkup()
        item1 = [types.InlineKeyboardButton('Перевірити Удачу', callback_data='104')]
        if not Functions.Functions.if_luck(character.luck):  # якщо не пощастило
            item1 = [types.InlineKeyboardButton('Перевірити Удачу', callback_data='82')]
        markup.add(*item1)
        Functions.Functions.change_1_data(user_id, 'Luck', 'user_id', 1, multiplier=-1)
    await bot.send_message(user_id, text.text_281, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '282')
async def text_282(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 282)
    Functions.DB.update_one_value(user_id, 'flag190_2', 2)
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("Go on", callback_data="190")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_282, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '283')
async def text_283(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 283)

    buttons_data = [
        ('Не дозволити владі ідентифікувати вас', "378"),
        ('Зачекати, щоб дізнатися, що робитиме ваш новий друг', "41")
    ]
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(*Functions.Functions.create_inline_buttons(*buttons_data))

    await bot.send_message(user_id, text.text_283, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '284')
async def text_284(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_game_over(callback_query, 284, text.text_284)


@dp.callback_query_handler(lambda c: c.data == '285')
async def text_285(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 285)

    grenade = Functions.DB.select_one_value(user_id, 'grenade_110_215', 'user_id')
    next_callback_data = "388" if grenade else "190"

    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = [types.InlineKeyboardButton("Go on", callback_data=next_callback_data)]
    markup.add(*item1)

    await bot.send_message(user_id, text.text_285, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '286')
async def text_286(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 286)
    money = Functions.DB.select_one_value(user_id, 'money', 'user_id')
    markup = types.InlineKeyboardMarkup(row_width=1)
    if money >= 1000:
        message_text = text.text_286_1
        item1 = [types.InlineKeyboardButton("Заплатити непомірну ціну", callback_data="84"),
                 types.InlineKeyboardButton("Запропонувати відпрацювати вартість товару", callback_data="238")]
    elif money < 1000:
        message_text = text.text_286_2
        item1 = [types.InlineKeyboardButton("Go on", callback_data="238")]
    markup.add(*item1)
    await bot.send_message(user_id, message_text, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '287')
async def text_287(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 287)

    sword = Functions.DB.select_one_value(user_id, 'sword', 'user_id')
    markup = types.InlineKeyboardMarkup(row_width=1)

    if sword:
        message_text = text.text_287_1
        item1 = [types.InlineKeyboardButton("Зробити, що він каже", callback_data="95"),
                 types.InlineKeyboardButton("Спробувати розрубати замок на дверях своїм мечем", callback_data="366")]
    elif not sword:
        message_text = text.text_287_2
        item1 = [types.InlineKeyboardButton("Go on", callback_data="95")]

    markup.add(*item1)
    await bot.send_message(user_id, message_text, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '288')
async def text_288(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 288)
    Functions.Functions.change_1_data(user_id, 'Endurance', 'user_id', 4, multiplier=-1)
    endurance = Functions.DB.select_one_value(user_id, 'Endurance', 'user_id')
    if endurance > 0:
        markup = types.InlineKeyboardMarkup(row_width=1)
        item1 = [types.InlineKeyboardButton("Go on", callback_data="46")]
        markup.add(*item1)
        await bot.send_message(user_id, text.text_288, reply_markup=markup, parse_mode='Markdown')
    elif endurance < 0:
        await bot.send_message(user_id, 'Вас засипає уламками корабля, що вибухнув. Гру закінчено.')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '289')
async def text_289(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_1_fight(callback_query, 289, 8, 10, "fight", text.text_289)
    # user_id = callback_query.from_user.id
    # Functions.DB.update_one_value(user_id, 'text_number', 289)
    # Functions.DB.update_add_enemy(user_id, 8, 10, 'e_mastery_289', 'e_endurance_289')
    # markup = types.InlineKeyboardMarkup()
    # item1 = [types.InlineKeyboardButton("Почати бійку", callback_data="fight")]
    # markup.add(*item1)
    # await bot.send_message(callback_query.from_user.id, text.text_289, reply_markup=markup, parse_mode='Markdown')
    # await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '290')
async def text_290(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 290)

    buttons_data = [
        ('Зробити те, що він каже, і чекати ще однієї можливості', "247"),
        ('Вдарити у двері ногою', "281")
    ]
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(*Functions.Functions.create_inline_buttons(*buttons_data))

    await bot.send_message(user_id, text.text_290, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '291')
async def text_291(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 291)

    buttons_data = [
        ('Відчинити двері і спробувати зблефувати та пройти повз них', "87"),
        ('Вивчити кнопки на столі', "276")
    ]
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(*Functions.Functions.create_inline_buttons(*buttons_data))

    await bot.send_message(user_id, text.text_291, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '292')
async def text_292(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 292)
    Functions.Functions.change_1_data(user_id, 'Luck', 'user_id', 2)
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = [types.InlineKeyboardButton("Go on", callback_data="118")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_292, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '293')
async def text_293(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_game_over(callback_query, 293, text.text_293)


@dp.callback_query_handler(lambda c: c.data == '294')
async def text_294(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 294)
    character_data = Functions.DB.retrieve_character_data(user_id)
    character = Functions.Functions.Character(mastery=character_data[0], endurance=character_data[1],
                                              luck=character_data[2])
    if character.luck > 0:
        markup = types.InlineKeyboardMarkup()
        item1 = [types.InlineKeyboardButton('Перевірити Удачу', callback_data='193')]
        if not Functions.Functions.if_luck(character.luck):  # якщо не пощастило
            item1 = [types.InlineKeyboardButton('Перевірити Удачу', callback_data='143')]
        markup.add(*item1)
        Functions.Functions.change_1_data(user_id, 'Luck', 'user_id', 1, multiplier=-1)
    await bot.send_message(user_id, text.text_294, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '295')
async def text_295(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 295)
    sword = Functions.DB.select_one_value(user_id, 'sword', 'user_id')
    if not sword:
        Functions.Functions.change_1_data(user_id, 'Mastery', 'user_id', 1, multiplier=-1)

    Functions.DB.update_add_enemy(user_id, 8, 12, 'e_mastery_295', 'e_endurance_295')
    Functions.DB.update_add_enemy(user_id, 8, 12, 'e_mastery_295_1', 'e_endurance_295_1')
    Functions.DB.update_add_enemy(user_id, 7, 8, 'e_mastery_295_2', 'e_endurance_295_2')
    Functions.DB.update_add_enemy(user_id, 7, 6, 'e_mastery_295_3', 'e_endurance_295_3')
    Functions.DB.update_add_enemy(user_id, 6, 6, 'e_mastery_295_4', 'e_endurance_295_4')
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("198", callback_data="198"),
             types.InlineKeyboardButton("Почати бійку", callback_data="fight")]
    markup.add(*item1)
    await bot.send_message(callback_query.from_user.id, text.text_295, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '296')
async def text_296(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 296)

    buttons_data = [
        ('Залишити це місце, щоб уникнути конфронтації', "275"),
        ('Спробувати врятувати людину', "243")
    ]
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(*Functions.Functions.create_inline_buttons(*buttons_data))

    await bot.send_message(user_id, text.text_296, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '297')
async def text_297(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 297)

    buttons_data = [
        ("Піти прямо до комп'ютерної кімнату", "381"),
        ('Піти спочатку у підвал', "169")
    ]
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(*Functions.Functions.create_inline_buttons(*buttons_data))

    await bot.send_message(user_id, text.text_297, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '298')
async def text_298(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_1_fight(callback_query, 298, 6, 8, "fight", text.text_298)
    # user_id = callback_query.from_user.id
    # Functions.DB.update_one_value(user_id, 'text_number', 298)
    # Functions.DB.update_add_enemy(user_id, 6, 8, 'e_mastery_298', 'e_endurance_298')
    # markup = types.InlineKeyboardMarkup()
    # item1 = [types.InlineKeyboardButton("Почати бійку", callback_data="fight")]
    # markup.add(*item1)
    # await bot.send_message(callback_query.from_user.id, text.text_298, reply_markup=markup, parse_mode='Markdown')
    # await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '299')
async def text_299(callback_query: types.CallbackQuery):
    Functions.DB.update_one_value(callback_query.from_user.id, 'text_number', 299)
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = [types.InlineKeyboardButton('Доручите таксі доставити вас прямо до "Вщент"', callback_data="176"),
             types.InlineKeyboardButton("Доручите таксі доставити вас прямо до гуртожинку", callback_data="196")]
    markup.add(*item1)
    await bot.send_message(callback_query.from_user.id, text.text_299, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '300')
async def text_300(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 300)

    buttons_data = [
        ("Очистити свідомість від усього зайвого", "141"),
        ("Зосередитися на своїх думках та спогадах", "357")
    ]
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(*Functions.Functions.create_inline_buttons(*buttons_data))

    await bot.send_message(user_id, text.text_300, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '301')
async def text_301(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 301)
    Functions.Functions.change_1_data(user_id, 'Luck', 'user_id', 1)
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = [types.InlineKeyboardButton("Go on", callback_data="349")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_301, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '302')
async def text_302(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_move(callback_query, 302, "78", text.text_302)
    # user_id = callback_query.from_user.id
    # Functions.DB.update_one_value(user_id, 'text_number', 302)
    # markup = types.InlineKeyboardMarkup(row_width=1)
    # item1 = [types.InlineKeyboardButton("Go on", callback_data="78")]
    # markup.add(*item1)
    # await bot.send_message(user_id, text.text_302, reply_markup=markup, parse_mode='Markdown')
    # await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '303')
async def text_303(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 303)
    Functions.Functions.change_1_data(user_id, 'Luck', 'user_id', 1, multiplier=-1)
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = [types.InlineKeyboardButton("Go on", callback_data="132")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_303, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '304')
async def text_304(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_game_over(callback_query, 304, text.text_304)


@dp.callback_query_handler(lambda c: c.data == '305')
async def text_305(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 305)

    button = Functions.DB.select_one_value(user_id, 'button_172', 'user_id')
    markup = types.InlineKeyboardMarkup(row_width=1)

    if button:
        message_text = text.text_305_1
        item1 = [types.InlineKeyboardButton("Go on", callback_data="347")]
    elif not button:
        message_text = text.text_305_2
        item1 = [types.InlineKeyboardButton("Go on", callback_data="103")]

    markup.add(*item1)
    await bot.send_message(user_id, message_text, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '306')
async def text_306(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 306)

    buttons_data = [
        ("Увійти відразу", "146"),
        ("Трохи зачекати зовні", "178")
    ]
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(*Functions.Functions.create_inline_buttons(*buttons_data))

    await bot.send_message(user_id, text.text_306, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '307')
async def text_307(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_game_over(callback_query, 307, text.text_307)


@dp.callback_query_handler(lambda c: c.data == '308')
async def text_308(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 308)

    buttons_data = [
        ("Попросити його відновити частину моєї Витривалості", "363"),
        ("Запитати, чи не знає він випадково, де знаходиться людина, яку шукаю", "377")
    ]
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(*Functions.Functions.create_inline_buttons(*buttons_data))

    await bot.send_message(user_id, text.text_308, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '309')
async def text_309(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 309)

    buttons_data = [
        ("158", "158"),
        ("134", "134")
    ]
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(*Functions.Functions.create_inline_buttons(*buttons_data))

    await bot.send_message(user_id, text.text_309, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '310')
async def text_310(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 310)

    buttons_data = [
        ('Запитати про зброю в цієї людини', "197"),
        ('Спробувати поговорити про це з кимось із людей у синьому', "217"),
        ('Спробувати отримати меч у аркадіанця', "16")
    ]
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(*Functions.Functions.create_inline_buttons(*buttons_data))

    await bot.send_message(user_id, text.text_310, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '311')
async def text_311(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_move(callback_query, 311, "207", text.text_311)
    # user_id = callback_query.from_user.id
    # Functions.DB.update_one_value(user_id, 'text_number', 311)
    # markup = types.InlineKeyboardMarkup(row_width=1)
    # item1 = [types.InlineKeyboardButton("Go on", callback_data="207")]
    # markup.add(*item1)
    # await bot.send_message(user_id, text.text_311, reply_markup=markup, parse_mode='Markdown')
    # await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '312')
async def text_312(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 312)

    buttons_data = [
        ("Лівий комп'ютер", "203"),
        ("Правий комп'ютер", "51"),
        ("Комп'ютер, який навпроти дверей", "139"),
        ("Повернутися і зробити інший вибір", "381")
    ]
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(*Functions.Functions.create_inline_buttons(*buttons_data))

    await bot.send_message(user_id, text.text_312, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '313')
async def text_313(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_1_fight(callback_query, 313, 7, 12, "fight", text.text_313)
    # user_id = callback_query.from_user.id
    # Functions.DB.update_one_value(user_id, 'text_number', 313)
    # Functions.DB.update_add_enemy(user_id, 7, 12, 'e_mastery_313', 'e_endurance_313')
    # markup = types.InlineKeyboardMarkup()
    # item1 = [types.InlineKeyboardButton("Почати бійку", callback_data="fight")]
    # markup.add(*item1)
    # await bot.send_message(callback_query.from_user.id, text.text_313, reply_markup=markup, parse_mode='Markdown')
    # await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '314')
async def text_314(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_move(callback_query, 314, "99", text.text_314)
    # user_id = callback_query.from_user.id
    # Functions.DB.update_one_value(user_id, 'text_number', 314)
    # markup = types.InlineKeyboardMarkup(row_width=1)
    # item1 = [types.InlineKeyboardButton("Go on", callback_data="99")]
    # markup.add(*item1)
    # await bot.send_message(user_id, text.text_314, reply_markup=markup, parse_mode='Markdown')
    # await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '315')
async def text_315(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 315)
    Functions.Functions.change_1_data(user_id, 'Luck', 'user_id', 1)
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = [types.InlineKeyboardButton("Go on", callback_data="118")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_315, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '316')
async def text_316(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_move(callback_query, 316, "235", text.text_316)
    # user_id = callback_query.from_user.id
    # Functions.DB.update_one_value(user_id, 'text_number', 316)
    # markup = types.InlineKeyboardMarkup(row_width=1)
    # item1 = [types.InlineKeyboardButton("Go on", callback_data="235")]
    # markup.add(*item1)
    # await bot.send_message(user_id, text.text_316, reply_markup=markup, parse_mode='Markdown')
    # await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '317')
async def text_317(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_game_over(callback_query, 317, text.text_317)


@dp.callback_query_handler(lambda c: c.data == '318')
async def text_318(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_move(callback_query, 318, "33", text.text_318)
    # user_id = callback_query.from_user.id
    # Functions.DB.update_one_value(user_id, 'text_number', 318)
    # markup = types.InlineKeyboardMarkup()
    # item1 = [types.InlineKeyboardButton("Go on", callback_data="33")]
    # markup.add(*item1)
    # await bot.send_message(user_id, text.text_318, reply_markup=markup, parse_mode='Markdown')
    # await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '319')
async def text_319(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_game_over(callback_query, 319, text.text_319)


@dp.callback_query_handler(lambda c: c.data == '320')
async def text_320(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 320)

    buttons_data = [
        ("Піти в лівий коридор", "127"),
        ("Піти в правий коридор", "257")
    ]
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(*Functions.Functions.create_inline_buttons(*buttons_data))

    await bot.send_message(user_id, text.text_320, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '321')
async def text_321(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 321)

    buttons_data = [
        ("Боротися з викрадачами", "80"),
        ("Прийняти цю пропозицію", "238")
    ]
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(*Functions.Functions.create_inline_buttons(*buttons_data))

    await bot.send_message(user_id, text.text_321, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '322')
async def text_322(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 322)

    buttons_data = [
        ("372", "372"),
        ("207", "207")
    ]
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(*Functions.Functions.create_inline_buttons(*buttons_data))

    await bot.send_message(user_id, text.text_322, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '323')
async def text_323(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 323)
    Functions.Functions.change_1_data(user_id, 'Endurance', 'user_id', 2, multiplier=-1)

    buttons_data = [
        ("Побігти до будівлі", "338"),
        ("Побігти до скель", "259")
    ]
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(*Functions.Functions.create_inline_buttons(*buttons_data))

    await bot.send_message(user_id, text.text_323, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '324')
async def text_324(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_game_over(callback_query, 324, text.text_324)


@dp.callback_query_handler(lambda c: c.data == '325')
async def text_325(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_game_over(callback_query, 325, text.text_325)


@dp.callback_query_handler(lambda c: c.data == '326')
async def text_326(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 326)
    money = Functions.DB.select_one_value(user_id, 'money', 'user_id')
    if money >= 250:
        sword = Functions.DB.select_one_value(user_id, 'sword', 'user_id')
        Functions.Functions.change_1_data(user_id, 'money', 'user_id', 250, multiplier=-1)
        markup = types.InlineKeyboardMarkup(row_width=1)
        if sword:
            message_text = text.text_326_1
            item1 = [types.InlineKeyboardButton("Сказати, що передумав і залишити клуб", callback_data="390"),
                     types.InlineKeyboardButton("Дозволити себе обшукати", callback_data="358")]
        elif not sword:
            message_text = text.text_326_2
            item1 = [types.InlineKeyboardButton("Go on", callback_data="64")]
        markup.add(*item1)
        await bot.send_message(user_id, message_text, reply_markup=markup, parse_mode='Markdown')
    else:
        await bot.send_message(user_id, 'У вас недостатньо коштів. Гру закінчено!')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '327')
async def text_327(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_game_over(callback_query, 327, text.text_327)


@dp.callback_query_handler(lambda c: c.data == '328')
async def text_328(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_game_over(callback_query, 328, text.text_328)


@dp.callback_query_handler(lambda c: c.data == '329')
async def text_329(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 329)
    Functions.Functions.change_1_data(user_id, 'money', 'user_id', 750)

    buttons_data = [
        ("Відразу увійти", "146"),
        ("Зачекати трохи зовні", "178")
    ]
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(*Functions.Functions.create_inline_buttons(*buttons_data))

    await bot.send_message(user_id, text.text_329, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '330')
async def text_330(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_game_over(callback_query, 330, text.text_330)


@dp.callback_query_handler(lambda c: c.data == '331')
async def text_331(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 331)
    Functions.Functions.change_1_data(user_id, 'Endurance', 'user_id', 2, multiplier=-1)

    buttons_data = [
        ("Дослідити іншу ущелину", "355"),
        ("Настав час продовжити подорож", "10")
    ]
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(*Functions.Functions.create_inline_buttons(*buttons_data))

    await bot.send_message(user_id, text.text_331, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '332')
async def text_332(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 332)

    buttons_data = [
        ("Зробити це", "325"),
        ("Повернутися і обрати знову", "381")
    ]
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(*Functions.Functions.create_inline_buttons(*buttons_data))

    await bot.send_message(user_id, text.text_332, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '333')
async def text_333(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 333)

    buttons_data = [
        ("Іти прямо", "346"),
        ("Повернути на північ", "277")
    ]
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(*Functions.Functions.create_inline_buttons(*buttons_data))

    await bot.send_message(user_id, text.text_333, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '334')
async def text_334(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 334)

    buttons_data = [
        ("Напасти на провідника", "157"),
        ("Втекти", "124")
    ]
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(*Functions.Functions.create_inline_buttons(*buttons_data))

    await bot.send_message(user_id, text.text_334, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '335')
async def text_335(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_move(callback_query, 335, "385", text.text_335)
    # user_id = callback_query.from_user.id
    # Functions.DB.update_one_value(user_id, 'text_number', 335)
    # markup = types.InlineKeyboardMarkup()
    # item1 = [types.InlineKeyboardButton("Go on", callback_data="385")]
    # markup.add(*item1)
    # await bot.send_message(user_id, text.text_335, reply_markup=markup, parse_mode='Markdown')
    # await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '336')
async def text_336(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 336)
    jetpack = Functions.DB.select_one_value(user_id, 'jetpack_253', 'user_id')
    wire_cutters = Functions.DB.select_one_value(user_id, 'wire_cutters', 'user_id')
    markup = types.InlineKeyboardMarkup(row_width=1)
    if jetpack and wire_cutters:
        message_text = text.text_336_1
        item1 = [types.InlineKeyboardButton("Реактивний ранець", callback_data="128"),
                 types.InlineKeyboardButton("Пара кусачок", callback_data="393")]
    elif jetpack and not wire_cutters:
        message_text = text.text_336_2
        item1 = [types.InlineKeyboardButton("Go on", callback_data="128")]
    elif not jetpack and wire_cutters:
        message_text = text.text_336_3
        item1 = [types.InlineKeyboardButton("Go on", callback_data="393")]
    elif not jetpack and not wire_cutters:
        message_text = text.text_336_4
        item1 = [types.InlineKeyboardButton("Go on", callback_data="2")]
    markup.add(*item1)
    await bot.send_message(user_id, message_text, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '337')
async def text_337(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 337)
    Functions.Functions.change_1_data(user_id, 'Endurance', 'user_id', 3)

    buttons_data = [
        ("Піти на Науковий поверх", "266"),
        ("Піти в офіс секретаря університету", "214"),
        ("Покинети університет", "235")
    ]
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(*Functions.Functions.create_inline_buttons(*buttons_data))

    await bot.send_message(user_id, text.text_337, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '338')
async def text_338(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_game_over(callback_query, 338, text.text_338)


@dp.callback_query_handler(lambda c: c.data == '339')
async def text_339(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_move(callback_query, 339, "374", text.text_339)
    # user_id = callback_query.from_user.id
    # Functions.DB.update_one_value(user_id, 'text_number', 339)
    # markup = types.InlineKeyboardMarkup()
    # item1 = [types.InlineKeyboardButton("Go on", callback_data="374")]
    # markup.add(*item1)
    # await bot.send_message(user_id, text.text_339, reply_markup=markup, parse_mode='Markdown')
    # await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '340')
async def text_340(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_game_over(callback_query, 340, text.text_340)


@dp.callback_query_handler(lambda c: c.data == '341')
async def text_341(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_1_fight(callback_query, 341, 7, 12, "fight", text.text_341)
    # user_id = callback_query.from_user.id
    # Functions.DB.update_one_value(user_id, 'text_number', 341)
    # Functions.DB.update_add_enemy(user_id, 7, 12, 'e_mastery_341', 'e_endurance_341')
    # markup = types.InlineKeyboardMarkup()
    # item1 = [types.InlineKeyboardButton("Почати бійку", callback_data="fight")]
    # markup.add(*item1)
    # await bot.send_message(user_id, text.text_341, reply_markup=markup, parse_mode='Markdown')
    # await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '342')
async def text_342(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 342)

    buttons_data = [
        ("Спробувати проникнути всередину", "208"),
        ("Не довіряю цій таємничій рухомій рослині і продовжую шлях", "327")
    ]
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(*Functions.Functions.create_inline_buttons(*buttons_data))

    await bot.send_message(user_id, text.text_342, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '343')
async def text_343(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 343)
    Functions.Functions.change_1_data(user_id, 'Luck', 'user_id', 2)
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("Купити флакон із зіллям", callback_data="343_1"),
             types.InlineKeyboardButton("Продовжити", callback_data="25")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_343, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '343_1')
async def text_343_1(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.Functions.change_1_data(user_id, 'money', 'user_id', 50, multiplier=-1)
    Functions.Functions.change_1_data(user_id, 'Endurance', 'user_id', 4)
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("Продовжити", callback_data="25")]
    markup.add(*item1)
    await bot.send_message(user_id, "Флакон із зіллям придбано, Витривалість відновлено.", reply_markup=markup,
                           parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '344')
async def text_344(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 344)

    buttons_data = [
        ("Сказати, що ходив до гелікоптера, який розбився", "26"),
        ("Сказати, що відносив провізію для патруля", "220")
    ]
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(*Functions.Functions.create_inline_buttons(*buttons_data))

    await bot.send_message(user_id, text.text_344, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '345')
async def text_345(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 345)

    buttons_data = [
        ("Пройти через праві двері", "293"),
        ("Пройти через ліві двері", "397")
    ]
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(*Functions.Functions.create_inline_buttons(*buttons_data))

    await bot.send_message(user_id, text.text_345, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '346')
async def text_346(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 346)

    buttons_data = [
        ("Обрати прохід, що веде на південь", "62"),
        ("Продовжити рух уперед", "8")
    ]
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(*Functions.Functions.create_inline_buttons(*buttons_data))

    await bot.send_message(user_id, text.text_346, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '347')
async def text_347(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_move(callback_query, 347, "81", text.text_347)
    # user_id = callback_query.from_user.id
    # Functions.DB.update_one_value(user_id, 'text_number', 347)
    # markup = types.InlineKeyboardMarkup()
    # item1 = [types.InlineKeyboardButton("Go on", callback_data="81")]
    # markup.add(*item1)
    # await bot.send_message(user_id, text.text_347, reply_markup=markup, parse_mode='Markdown')
    # await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '348')
async def text_348(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 348)
    grenade = Functions.DB.select_one_value(user_id, 'grenade_110_215', 'user_id')
    hand_phaser = Functions.DB.select_one_value(user_id, 'hand_phaser_110', 'user_id')

    if grenade or hand_phaser:
        markup = types.InlineKeyboardMarkup(row_width=1)
        if grenade and hand_phaser:
            message_text = text.text_348_1
            item1 = [types.InlineKeyboardButton("Використати фотонну гранату", callback_data="86"),
                     types.InlineKeyboardButton("Використати ручний фазер", callback_data="271")]
        elif grenade and not hand_phaser:
            message_text = text.text_348_2
            item1 = [types.InlineKeyboardButton("Використати фотонну гранату", callback_data="86")]
        elif not grenade and hand_phaser:
            message_text = text.text_348_3
            item1 = [types.InlineKeyboardButton("Використати ручний фазер", callback_data="271")]
        markup.add(*item1)
        await bot.send_message(user_id, message_text, reply_markup=markup, parse_mode='Markdown')
        await callback_query.answer()

    elif not grenade and not hand_phaser:
        # Send the message
        await bot.send_message(user_id, 'Оскільки у вас нема ні фотонної гранати, ні ручного фазера, ви мертві.')

        # Answer the callback query
        await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '349')
async def text_349(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 349)
    Functions.Functions.change_1_data(user_id, 'Endurance', 'user_id', 3)

    buttons_data = [
        ("Напасти на охоронця", "206"),
        ("Дозволити охоронцю відвести мене на ігри", "231")
    ]
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(*Functions.Functions.create_inline_buttons(*buttons_data))

    await bot.send_message(user_id, text.text_349, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '350')
async def text_350(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 350)

    buttons_data = [
        ("Сказати, що робот принесе йому ліки у його каюту", "212"),
        ("Запросити увійти", "230")
    ]
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(*Functions.Functions.create_inline_buttons(*buttons_data))

    await bot.send_message(user_id, text.text_350, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '351')
async def text_351(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_1_fight(callback_query, 351, 5, 6, "fight", text.text_351)
    # user_id = callback_query.from_user.id
    # Functions.DB.update_one_value(user_id, 'text_number', 351)
    # Functions.DB.update_add_enemy(user_id, 5, 6, 'e_mastery_351', 'e_endurance_351')
    # markup = types.InlineKeyboardMarkup()
    # item1 = [types.InlineKeyboardButton("Почати бійку", callback_data="fight")]
    # markup.add(*item1)
    # await bot.send_message(user_id, text.text_351, reply_markup=markup, parse_mode='Markdown')
    # await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '352')
async def text_352(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_move(callback_query, 352, "190", text.text_352)
    # user_id = callback_query.from_user.id
    # Functions.DB.update_one_value(user_id, 'text_number', 352)
    # markup = types.InlineKeyboardMarkup()
    # item1 = [types.InlineKeyboardButton("Go on", callback_data="190")]
    # markup.add(*item1)
    # await bot.send_message(user_id, text.text_352, reply_markup=markup, parse_mode='Markdown')
    # await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '353')
async def text_353(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 353)
    Functions.Functions.change_1_data(user_id, 'Endurance', 'user_id', 2, multiplier=-1)
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("Go on", callback_data="321")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_353, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '354')
async def text_354(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 354)

    buttons_data = [
        ("Залишитися з ним, щоб заспокоїти його", "136"),
        ("Залишити його наодинці зі своїм горем", "60")
    ]
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(*Functions.Functions.create_inline_buttons(*buttons_data))

    await bot.send_message(user_id, text.text_354, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '355')
async def text_355(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 355)

    buttons_data = [
        ("Взяти щось", "355_1"),
        ("Далі", "355_2")
    ]
    markup = types.InlineKeyboardMarkup()
    markup.add(*Functions.Functions.create_inline_buttons(*buttons_data))
    await bot.send_message(user_id, text.text_355, reply_markup=markup, parse_mode='Markdown')


@dp.callback_query_handler(lambda c: c.data == '355_1')
async def text_355_1(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    data_list = ["Посох", "Шкатулка", "Мозковий зонд"]
    Functions.DB.insert_list_data(user_id, data_list, 'buttons_data_355')
    buttons_data = [
        ("Посох", "355_1_1"),
        ("Шкатулка", "355_1_2"),
        ("Мозковий зонд", "355_1_3")
    ]
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(*Functions.Functions.create_inline_buttons(*buttons_data))
    await bot.send_message(callback_query.from_user.id, 'Що ви візьмете?', reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '355_1_1')
async def text_355_1_1(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    data_string = Functions.DB.select_one_value(user_id, 'buttons_data_355', 'user_id')
    # Wrap the string with brackets to make it a valid list literal
    formatted_string = f'[{data_string}]'

    # Use ast.literal_eval to safely evaluate the string as a list
    data_list = ast.literal_eval(formatted_string)

    data_list.remove("Посох")
    Functions.DB.insert_list_data(user_id, data_list, 'buttons_data_355')
    Functions.DB.update_one_value(user_id, 'warder_355', 1)

    buttons_data_0 = {
        "Посох": ("Посох", "355_1_1"),
        "Шкатулка": ("Шкатулка", "355_1_2"),
        "Мозковий зонд": ("Мозковий зонд", "355_1_3"),
    }
    buttons_data = []
    for key, value in buttons_data_0.items():
        for item in data_list:
            if key == item:
                buttons_data.append(value)
    if buttons_data:  # якщо не пусто
        buttons_data.append(("Дослідити іншу ущелину", "14"))
        buttons_data.append(("Продовжити подорож", "10"))
        text_message = 'Ви берете посох. Бажаєте ще щось взяти?'
    else:
        text_message = text.text_355_2
        buttons_data = [
            ("Дослідити іншу ущелину", "14"),
            ("Продовжити подорож", "10")
        ]
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(*Functions.Functions.create_inline_buttons(*buttons_data))
    await bot.send_message(callback_query.from_user.id, text_message, reply_markup=markup,
                           parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '355_1_2')
async def text_355_1_2(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    data_string = Functions.DB.select_one_value(user_id, 'buttons_data_355', 'user_id')
    # Wrap the string with brackets to make it a valid list literal
    formatted_string = f'[{data_string}]'

    # Use ast.literal_eval to safely evaluate the string as a list
    data_list = ast.literal_eval(formatted_string)

    data_list.remove("Шкатулка")
    Functions.Functions.change_1_data(user_id, 'money', 'user_id', 180)
    Functions.DB.insert_list_data(user_id, data_list, 'buttons_data_355')

    buttons_data_0 = {
        "Посох": ("Посох", "355_1_1"),
        "Шкатулка": ("Шкатулка", "355_1_2"),
        "Мозковий зонд": ("Мозковий зонд", "355_1_3"),
    }
    buttons_data = []
    for key, value in buttons_data_0.items():
        for item in data_list:
            if key == item:
                buttons_data.append(value)
    if buttons_data:  # якщо не пусто
        buttons_data.append(("Дослідити іншу ущелину", "14"))
        buttons_data.append(("Продовжити подорож", "10"))
        text_message = 'Ви берете шкатулку зі 180 кредитами. Бажаєте ще щось взяти?'
    else:
        text_message = text.text_355_2
        buttons_data = [
            ("Дослідити іншу ущелину", "14"),
            ("Продовжити подорож", "10")
        ]
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(*Functions.Functions.create_inline_buttons(*buttons_data))
    await bot.send_message(callback_query.from_user.id, text_message, reply_markup=markup,
                           parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '355_1_3')
async def text_355_1_3(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    data_string = Functions.DB.select_one_value(user_id, 'buttons_data_355', 'user_id')
    # Wrap the string with brackets to make it a valid list literal
    formatted_string = f'[{data_string}]'

    # Use ast.literal_eval to safely evaluate the string as a list
    data_list = ast.literal_eval(formatted_string)

    data_list.remove("Посох")
    Functions.DB.insert_list_data(user_id, data_list, 'buttons_data_355')
    Functions.DB.update_one_value(user_id, 'brain_probe_355', 1)

    buttons_data_0 = {
        "Посох": ("Посох", "355_1_1"),
        "Шкатулка": ("Шкатулка", "355_1_2"),
        "Мозковий зонд": ("Мозковий зонд", "355_1_3"),
    }
    buttons_data = []
    for key, value in buttons_data_0.items():
        for item in data_list:
            if key == item:
                buttons_data.append(value)
    if buttons_data:  # якщо не пусто
        buttons_data.append(("Дослідити іншу ущелину", "14"))
        buttons_data.append(("Продовжити подорож", "10"))
        text_message = 'Ви берете мозковий зонд. Бажаєте ще щось взяти?'
    else:
        text_message = text.text_355_2
        buttons_data = [
            ("Дослідити іншу ущелину", "14"),
            ("Продовжити подорож", "10")
        ]
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(*Functions.Functions.create_inline_buttons(*buttons_data))
    await bot.send_message(callback_query.from_user.id, text_message, reply_markup=markup,
                           parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '355_2')
async def text_355_2(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id

    buttons_data = [
        ("Дослідити іншу ущелину", "14"),
        ("Продовжити подорож", "10")
    ]
    markup = types.InlineKeyboardMarkup()
    markup.add(*Functions.Functions.create_inline_buttons(*buttons_data))
    await bot.send_message(user_id, text.text_355_2, reply_markup=markup, parse_mode='Markdown')


@dp.callback_query_handler(lambda c: c.data == '356')
async def text_356(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 356)

    buttons_data = [
        ("Прийняти пропозицію", "392"),
        ("Піти до університету", "146")
    ]
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(*Functions.Functions.create_inline_buttons(*buttons_data))

    await bot.send_message(user_id, text.text_356, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '357')
async def text_357(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_move(callback_query, 357, "55", text.text_357)
    # user_id = callback_query.from_user.id
    # Functions.DB.update_one_value(user_id, 'text_number', 357)
    # markup = types.InlineKeyboardMarkup()
    # item1 = [types.InlineKeyboardButton("Go on", callback_data="55")]
    # markup.add(*item1)
    # await bot.send_message(user_id, text.text_357, reply_markup=markup, parse_mode='Markdown')
    # await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '358')
async def text_358(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_move(callback_query, 358, "37", text.text_358)
    # user_id = callback_query.from_user.id
    # Functions.DB.update_one_value(user_id, 'text_number', 358)
    # markup = types.InlineKeyboardMarkup()
    # item1 = [types.InlineKeyboardButton("Go on", callback_data="37")]
    # markup.add(*item1)
    # await bot.send_message(user_id, text.text_358, reply_markup=markup, parse_mode='Markdown')
    # await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '359')
async def text_359(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_move(callback_query, 359, "30", text.text_359)
    # user_id = callback_query.from_user.id
    # Functions.DB.update_one_value(user_id, 'text_number', 359)
    # markup = types.InlineKeyboardMarkup()
    # item1 = [types.InlineKeyboardButton("Go on", callback_data="30")]
    # markup.add(*item1)
    # await bot.send_message(user_id, text.text_359, reply_markup=markup, parse_mode='Markdown')
    # await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '360')
async def text_360(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_move(callback_query, 360, "301", text.text_360)
    # user_id = callback_query.from_user.id
    # Functions.DB.update_one_value(user_id, 'text_number', 360)
    # markup = types.InlineKeyboardMarkup()
    # item1 = [types.InlineKeyboardButton("Go on", callback_data="301")]
    # markup.add(*item1)
    # await bot.send_message(user_id, text.text_360, reply_markup=markup, parse_mode='Markdown')
    # await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '361')
async def text_361(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 361)

    buttons_data = [
        ("Сказати аркадіанцю, що я все знаю", "167"),
        ("Нехай аркадіанець поки виведе Муску", "290")
    ]
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(*Functions.Functions.create_inline_buttons(*buttons_data))

    await bot.send_message(user_id, text.text_361, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '362')
async def text_362(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 362)

    buttons_data = [
        ("Пожертвувати собою, сподіваючись врятувати підпільників у клубі", "192"),
        ("Битися", "295")
    ]
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(*Functions.Functions.create_inline_buttons(*buttons_data))

    await bot.send_message(user_id, text.text_362, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '363')
async def text_363(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 363)
    Functions.Functions.change_1_data(user_id, 'Endurance', 'user_id', 4)
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("Go on", callback_data="114")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_363, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '364')
async def text_364(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_move(callback_query, 364, "264", text.text_364)
    # user_id = callback_query.from_user.id
    # Functions.DB.update_one_value(user_id, 'text_number', 364)
    # markup = types.InlineKeyboardMarkup()
    # item1 = [types.InlineKeyboardButton("Go on", callback_data="264")]
    # markup.add(*item1)
    # await bot.send_message(user_id, text.text_364, reply_markup=markup, parse_mode='Markdown')
    # await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '365')
async def text_365(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 365)
    Functions.DB.clear_cell(user_id, 'bracelet_ziridium_117')
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("Go on", callback_data="392")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_365, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '366')
async def text_366(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 366)
    Functions.DB.update_add_enemy(user_id, 8, 12, 'e_mastery_366', 'e_endurance_366')
    Functions.DB.update_add_enemy(user_id, 8, 12, 'e_mastery_366_1', 'e_endurance_366_1')
    Functions.DB.update_add_enemy(user_id, 7, 8, 'e_mastery_366_2', 'e_endurance_366_2')
    Functions.DB.update_add_enemy(user_id, 7, 6, 'e_mastery_366_3', 'e_endurance_366_3')
    Functions.DB.update_add_enemy(user_id, 6, 6, 'e_mastery_366_4', 'e_endurance_366_4')
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("198", callback_data="198"),
             types.InlineKeyboardButton("Почати бійку", callback_data="fight")]
    markup.add(*item1)
    await bot.send_message(callback_query.from_user.id, text.text_366, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '367')
async def text_367(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_1_fight(callback_query, 367, 6, 10, "fight", text.text_367)
    # user_id = callback_query.from_user.id
    # Functions.DB.update_one_value(user_id, 'text_number', 367)
    # Functions.DB.update_add_enemy(user_id, 6, 10, 'e_mastery_367', 'e_endurance_367')
    # markup = types.InlineKeyboardMarkup()
    # item1 = [types.InlineKeyboardButton("Почати бійку", callback_data="fight")]
    # markup.add(*item1)
    # await bot.send_message(user_id, text.text_367, reply_markup=markup, parse_mode='Markdown')
    # await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == 'take_sword_367')
async def text_367_1(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'sword', 1)
    text_message = 'Тепер у вас є меч.'
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("Go on", callback_data="336")]
    markup.add(*item1)
    await bot.send_message(callback_query.from_user.id, text_message, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '368')
async def text_368(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_game_over(callback_query, 368, text.text_368)


@dp.callback_query_handler(lambda c: c.data == '369')
async def text_369(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 369)

    buttons_data = [
        ("Стріляти з фазера", "325"),
        ("Повернутися на 381", "381")
    ]
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(*Functions.Functions.create_inline_buttons(*buttons_data))

    await bot.send_message(user_id, text.text_369, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '370')
async def text_370(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 370)
    Functions.Functions.change_1_data(user_id, 'Endurance', 'user_id', 2)
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("Продовжити", callback_data="299")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_370, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '371')
async def text_371(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_game_over(callback_query, 371, text.text_371)


@dp.callback_query_handler(lambda c: c.data == '372')
async def text_372(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_game_over(callback_query, 372, text.text_372)


@dp.callback_query_handler(lambda c: c.data == '373')
async def text_373(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 373)
    # Functions.DB.update_one_value(user_id, 'text_number', 373)
    Functions.DB.update_add_enemy(user_id, 7, 14, 'e_mastery_373', 'e_endurance_373')
    # Functions.DB.update_add_enemy(user_id, 6, 6, 'e_mastery_373_2', 'e_endurance_373_2')
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("Перший аркадіанець", callback_data="fight")]
    # types.InlineKeyboardButton("Другий аркадіанець", callback_data="second_a_373")]
    markup.add(*item1)
    await bot.send_message(callback_query.from_user.id, text.text_373, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '374')
async def text_374(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 374)
    endurance = Functions.DB.select_one_value(user_id, 'Endurance', 'user_id')
    Functions.DB.update_one_value(user_id, 'Endurance', endurance + math.ceil(endurance / 2))
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("Go on", callback_data='47')]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_374, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '375')
async def text_375(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_1_fight(callback_query, 375, 8, 12, "fight", text.text_375)
    # user_id = callback_query.from_user.id
    # Functions.DB.update_one_value(user_id, 'text_number', 375)
    # Functions.DB.update_add_enemy(user_id, 8, 12, 'e_mastery_375', 'e_endurance_375')
    # markup = types.InlineKeyboardMarkup()
    # item1 = [types.InlineKeyboardButton("Почати бійку", callback_data="fight")]
    # markup.add(*item1)
    # await bot.send_message(user_id, text.text_375, reply_markup=markup, parse_mode='Markdown')
    # await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '376')
async def text_376(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 376)

    photo_path = '376.png'

    # Send the photo
    await bot.send_photo(user_id, photo=open(photo_path, 'rb'))

    # Continue with existing logic
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("Go on", callback_data="43")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_376, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '377')
async def text_377(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 377)
    Functions.Functions.change_1_data(user_id, 'Luck', 'user_id', 2)
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("Go on", callback_data="114")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_377, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '378')
async def text_378(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 378)
    endurance = Functions.DB.select_one_value(user_id, 'Endurance', 'user_id')
    item1 = [types.InlineKeyboardButton("Go on", callback_data='351')]
    markup = types.InlineKeyboardMarkup()
    if endurance < 12:
        item1 = [types.InlineKeyboardButton("Go on", callback_data='242')]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_378, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '379')
async def text_379(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_game_over(callback_query, 379, text.text_379)


@dp.callback_query_handler(lambda c: c.data == '380')
async def text_380(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 380)

    buttons_data = [
        ("Попросити його показати вам їх", "270"),
        ("Піти до університету", "146")
    ]
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(*Functions.Functions.create_inline_buttons(*buttons_data))

    await bot.send_message(user_id, text.text_380, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '381')
async def text_381(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 381)

    buttons_data = [
        ("Кусачки", "61"),
        ("Фотонна граната", "312"),
        ("Ельмоніт", "395"),
        ("Магнітна міна", "6"),
        ("Лазерний меч", "332"),
        ("Фазер", "369"),
        ("Інфрачервоний сканер", "149")
    ]
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(*Functions.Functions.create_inline_buttons(*buttons_data))

    await bot.send_message(user_id, text.text_381, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '382')
async def text_382(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 382)
    data_list = ["Стробоскоп", "Ручний клаксон", "Моток нейлонової мотузки", "Банка моторного масла",
                 "Персональний робот"]
    Functions.DB.insert_list_data(user_id, data_list, 'buttons_data_382')
    buttons_data = [
        ("Стробоскоп", "382_1"),
        ("Ручний клаксон", "382_2"),
        ("Моток нейлонової мотузки", "382_3"),
        ("Банка моторного масла", "382_4"),
        ("Персональний робот", "382_5")
    ]
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(*Functions.Functions.create_inline_buttons(*buttons_data))
    await bot.send_message(user_id, text.text_382, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '382_1')
async def text_382_1(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    data_string = Functions.DB.select_one_value(user_id, 'buttons_data_382', 'user_id')
    # Wrap the string with brackets to make it a valid list literal
    formatted_string = f'[{data_string}]'

    # Use ast.literal_eval to safely evaluate the string as a list
    data_list = ast.literal_eval(formatted_string)

    data_list.remove("Стробоскоп")
    Functions.Functions.change_1_data(user_id, 'money', 'user_id', 70, multiplier=-1)
    Functions.DB.insert_list_data(user_id, data_list, 'buttons_data_382')
    Functions.DB.update_one_value(user_id, 'stroboscope_382', 1)
    money382 = Functions.DB.select_one_value(user_id, 'money382', 'user_id')
    if money382:
        Functions.Functions.change_1_data(user_id, 'money382', 'user_id', 70)
    else:
        Functions.DB.update_one_value(user_id, 'money382', 70)

    buttons_data_0 = {
        "Стробоскоп": ("Стробоскоп", "382_1"),
        "Ручний клаксон": ("Ручний клаксон", "382_2"),
        "Моток нейлонової мотузки": ("Моток нейлонової мотузки", "382_3"),
        "Банка моторного масла": ("Банка моторного масла", "382_4"),
        "Персональний робот": ("Персональний робот", "382_5")
    }
    buttons_data = []
    for key, value in buttons_data_0.items():
        for item in data_list:
            if key == item:
                buttons_data.append(value)
    if buttons_data:  # якщо не пусто
        buttons_data.append(("Покупки завершено", "382_6"))
        text_message = 'Ви берете стробоскоп. Бажаєте ще щось взяти?'
    else:
        text_message = text.text_382_1
        buttons_data = [
            ("Я знаю, про що він говорить", "check_382"),
            ("Я не знаю, про що він говорить", "44")
        ]
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(*Functions.Functions.create_inline_buttons(*buttons_data))
    await bot.send_message(user_id, text_message, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '382_2')
async def text_382_2(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    data_string = Functions.DB.select_one_value(user_id, 'buttons_data_382', 'user_id')
    # Wrap the string with brackets to make it a valid list literal
    formatted_string = f'[{data_string}]'

    # Use ast.literal_eval to safely evaluate the string as a list
    data_list = ast.literal_eval(formatted_string)

    data_list.remove("Ручний клаксон")
    Functions.Functions.change_1_data(user_id, 'money', 'user_id', 50, multiplier=-1)
    Functions.DB.insert_list_data(user_id, data_list, 'buttons_data_382')
    Functions.DB.update_one_value(user_id, 'manual_horn_382', 1)
    money382 = Functions.DB.select_one_value(user_id, 'money382', 'user_id')
    if money382:
        Functions.Functions.change_1_data(user_id, 'money382', 'user_id', 50)
    else:
        Functions.DB.update_one_value(user_id, 'money382', 50)
    buttons_data_0 = {
        "Стробоскоп": ("Стробоскоп", "382_1"),
        "Ручний клаксон": ("Ручний клаксон", "382_2"),
        "Моток нейлонової мотузки": ("Моток нейлонової мотузки", "382_3"),
        "Банка моторного масла": ("Банка моторного масла", "382_4"),
        "Персональний робот": ("Персональний робот", "382_5")
    }
    buttons_data = []
    for key, value in buttons_data_0.items():
        for item in data_list:
            if key == item:
                buttons_data.append(value)
    if buttons_data:  # якщо не пусто
        buttons_data.append(("Покупки завершено", "382_6"))
        text_message = 'Ви берете ручний клаксон. Бажаєте ще щось взяти?'
    else:
        text_message = text.text_382_1
        buttons_data = [
            ("Я знаю, про що він говорить", "check_382"),
            ("Я не знаю, про що він говорить", "44")
        ]
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(*Functions.Functions.create_inline_buttons(*buttons_data))
    await bot.send_message(user_id, text_message, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '382_3')
async def text_382_3(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    data_string = Functions.DB.select_one_value(user_id, 'buttons_data_382', 'user_id')
    # Wrap the string with brackets to make it a valid list literal
    formatted_string = f'[{data_string}]'

    # Use ast.literal_eval to safely evaluate the string as a list
    data_list = ast.literal_eval(formatted_string)

    data_list.remove("Моток нейлонової мотузки")
    Functions.Functions.change_1_data(user_id, 'money', 'user_id', 50, multiplier=-1)
    Functions.DB.insert_list_data(user_id, data_list, 'buttons_data_382')
    Functions.DB.update_one_value(user_id, 'skein_of_nylon_rope_382', 1)
    money382 = Functions.DB.select_one_value(user_id, 'money382', 'user_id')
    if money382:
        Functions.Functions.change_1_data(user_id, 'money382', 'user_id', 50)
    else:
        Functions.DB.update_one_value(user_id, 'money382', 50)
    buttons_data_0 = {
        "Стробоскоп": ("Стробоскоп", "382_1"),
        "Ручний клаксон": ("Ручний клаксон", "382_2"),
        "Моток нейлонової мотузки": ("Моток нейлонової мотузки", "382_3"),
        "Банка моторного масла": ("Банка моторного масла", "382_4"),
        "Персональний робот": ("Персональний робот", "382_5")
    }
    buttons_data = []
    for key, value in buttons_data_0.items():
        for item in data_list:
            if key == item:
                buttons_data.append(value)
    if buttons_data:  # якщо не пусто
        buttons_data.append(("Покупки завершено", "382_6"))
        text_message = 'Ви берете моток нейлонової мотузки. Бажаєте ще щось взяти?'
    else:
        text_message = text.text_382_1
        buttons_data = [
            ("Я знаю, про що він говорить", "check_382"),
            ("Я не знаю, про що він говорить", "44")
        ]
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(*Functions.Functions.create_inline_buttons(*buttons_data))
    await bot.send_message(user_id, text_message, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '382_4')
async def text_382_4(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    data_string = Functions.DB.select_one_value(user_id, 'buttons_data_382', 'user_id')
    # Wrap the string with brackets to make it a valid list literal
    formatted_string = f'[{data_string}]'

    # Use ast.literal_eval to safely evaluate the string as a list
    data_list = ast.literal_eval(formatted_string)

    data_list.remove("Банка моторного масла")
    Functions.Functions.change_1_data(user_id, 'money', 'user_id', 20, multiplier=-1)
    Functions.DB.insert_list_data(user_id, data_list, 'buttons_data_382')
    Functions.DB.update_one_value(user_id, 'can_of_motor_oil_382', 1)
    money382 = Functions.DB.select_one_value(user_id, 'money382', 'user_id')
    if money382:
        Functions.Functions.change_1_data(user_id, 'money382', 'user_id', 20)
    else:
        Functions.DB.update_one_value(user_id, 'money382', 20)
    buttons_data_0 = {
        "Стробоскоп": ("Стробоскоп", "382_1"),
        "Ручний клаксон": ("Ручний клаксон", "382_2"),
        "Моток нейлонової мотузки": ("Моток нейлонової мотузки", "382_3"),
        "Банка моторного масла": ("Банка моторного масла", "382_4"),
        "Персональний робот": ("Персональний робот", "382_5")
    }
    buttons_data = []
    for key, value in buttons_data_0.items():
        for item in data_list:
            if key == item:
                buttons_data.append(value)
    if buttons_data:  # якщо не пусто
        buttons_data.append(("Покупки завершено", "382_6"))
        text_message = 'Ви берете банку моторного масла. Бажаєте ще щось взяти?'
    else:
        text_message = text.text_382_1
        buttons_data = [
            ("Я знаю, про що він говорить", "check_382"),
            ("Я не знаю, про що він говорить", "44")
        ]
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(*Functions.Functions.create_inline_buttons(*buttons_data))
    await bot.send_message(user_id, text_message, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '382_5')
async def text_382_5(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    data_string = Functions.DB.select_one_value(user_id, 'buttons_data_382', 'user_id')
    # Wrap the string with brackets to make it a valid list literal
    formatted_string = f'[{data_string}]'

    # Use ast.literal_eval to safely evaluate the string as a list
    data_list = ast.literal_eval(formatted_string)

    data_list.remove("Персональний робот")
    Functions.Functions.change_1_data(user_id, 'money', 'user_id', 650, multiplier=-1)
    Functions.DB.insert_list_data(user_id, data_list, 'buttons_data_382')
    Functions.DB.update_one_value(user_id, 'personal_robot_382', 1)
    money382 = Functions.DB.select_one_value(user_id, 'money382', 'user_id')
    if money382:
        Functions.Functions.change_1_data(user_id, 'money382', 'user_id', 650)
    else:
        Functions.DB.update_one_value(user_id, 'money382', 650)
    buttons_data_0 = {
        "Стробоскоп": ("Стробоскоп", "382_1"),
        "Ручний клаксон": ("Ручний клаксон", "382_2"),
        "Моток нейлонової мотузки": ("Моток нейлонової мотузки", "382_3"),
        "Банка моторного масла": ("Банка моторного масла", "382_4"),
        "Персональний робот": ("Персональний робот", "382_5")
    }
    buttons_data = []
    for key, value in buttons_data_0.items():
        for item in data_list:
            if key == item:
                buttons_data.append(value)
    if buttons_data:  # якщо не пусто
        buttons_data.append(("Покупки завершено", "382_6"))
        text_message = 'Ви берете персонального робота. Бажаєте ще щось взяти?'
    else:
        text_message = text.text_382_1
        buttons_data = [
            ("Я знаю, про що він говорить", "check_382"),
            ("Я не знаю, про що він говорить", "44")
        ]
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(*Functions.Functions.create_inline_buttons(*buttons_data))
    await bot.send_message(user_id, text_message, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '382_6')
async def text_382_6(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    text_message = text.text_382_1
    buttons_data = [
        ("Я знаю, про що він говорить", "check_382"),
        ("Я не знаю, про що він говорить", "44")
    ]
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(*Functions.Functions.create_inline_buttons(*buttons_data))
    await bot.send_message(user_id, text_message, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == 'check_382')
async def text_check_106_callback(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_text = "Введіть код або продовжуйте подорож"
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("Не знаю код. Продовжити подорож.", callback_data="44")]
    markup.add(*item1)
    await bot.send_message(user_id, message_text, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '383')
async def text_383(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 383)

    buttons_data = [
        ("Зістрибнути на уступ", "298"),
        ("Повернутись на стежку", "147")
    ]
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(*Functions.Functions.create_inline_buttons(*buttons_data))

    await bot.send_message(user_id, text.text_383, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '384')
async def text_384(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 384)

    buttons_data = [
        ("Повернути", "123"),
        ("Продовжити йти прямо", "154")
    ]
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(*Functions.Functions.create_inline_buttons(*buttons_data))

    await bot.send_message(user_id, text.text_384, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '385')
async def text_385(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 385)
    Functions.Functions.change_1_data(user_id, 'Luck', 'user_id', 1, multiplier=-1)
    markup = types.InlineKeyboardMarkup()
    item1 = [types.InlineKeyboardButton("Спитати про меч", callback_data="286")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_385, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '386')
async def text_386(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_move(callback_query, 386, "299", text.text_386)
    # user_id = callback_query.from_user.id
    # Functions.DB.update_one_value(user_id, 'text_number', 386)
    # markup = types.InlineKeyboardMarkup()
    # item1 = [types.InlineKeyboardButton("Go on", callback_data="299")]
    # markup.add(*item1)
    # await bot.send_message(user_id, text.text_386, reply_markup=markup, parse_mode='Markdown')
    # await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '387')
async def text_387(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 387)

    buttons_data = [
        ("Спробувати розбити машину", "265"),
        ("Дозволити продовжити експеримент", "116")
    ]
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(*Functions.Functions.create_inline_buttons(*buttons_data))

    await bot.send_message(user_id, text.text_387, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '388')
async def text_388(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 388)
    character_data = Functions.DB.retrieve_character_data(user_id)
    character = Functions.Functions.Character(mastery=character_data[0], endurance=character_data[1],
                                              luck=character_data[2])
    if character.luck > 0:
        markup = types.InlineKeyboardMarkup()
        item1 = [types.InlineKeyboardButton('Перевірити Удачу', callback_data='63')]
        if not Functions.Functions.if_luck(character.luck):  # якщо не пощастило
            item1 = [types.InlineKeyboardButton('Перевірити Удачу', callback_data='352')]
        markup.add(*item1)
        Functions.Functions.change_1_data(user_id, 'Luck', 'user_id', 1, multiplier=-1)
    await bot.send_message(user_id, text.text_388, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '389')
async def text_389(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 389)

    buttons_data = [
        ("Побігти до будівлі", "338"),
        ("Побігти до скель", "259")
    ]
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(*Functions.Functions.create_inline_buttons(*buttons_data))

    await bot.send_message(user_id, text.text_389, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '390')
async def text_390(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_game_over(callback_query, 390, text.text_390)


@dp.callback_query_handler(lambda c: c.data == '391')
async def text_391(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_1_fight(callback_query, 391, 8, 10, "fight", text.text_391)
    # user_id = callback_query.from_user.id
    # Functions.DB.update_one_value(user_id, 'text_number', 391)
    # Functions.DB.update_add_enemy(user_id, 8, 10, 'e_mastery_391', 'e_endurance_391')
    # markup = types.InlineKeyboardMarkup()
    # item1 = [types.InlineKeyboardButton("Почати бійку", callback_data="fight")]
    # markup.add(*item1)
    # await bot.send_message(user_id, text.text_391, reply_markup=markup, parse_mode='Markdown')
    # await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '392')
async def text_392(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_move(callback_query, 392, "215", text.text_392)
    # user_id = callback_query.from_user.id
    # Functions.DB.update_one_value(user_id, 'text_number', 392)
    # markup = types.InlineKeyboardMarkup()
    # item1 = [types.InlineKeyboardButton("Go on", callback_data="215")]
    # markup.add(*item1)
    # await bot.send_message(user_id, text.text_392, reply_markup=markup, parse_mode='Markdown')
    # await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '393')
async def text_393(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 393)
    character_data = Functions.DB.retrieve_character_data(user_id)
    character = Functions.Functions.Character(mastery=character_data[0], endurance=character_data[1],
                                              luck=character_data[2])
    result = Functions.Functions.roll_dice_2()
    print(result)
    markup = types.InlineKeyboardMarkup()
    if result < character.mastery:
        item1 = [types.InlineKeyboardButton('Go on', callback_data="279")]
    else:
        item1 = [types.InlineKeyboardButton('Go on', callback_data="199")]
    markup.add(*item1)
    await bot.send_message(user_id, text.text_393, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '394')
async def text_394(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 394)

    buttons_data = [
        ("Наполягати на тому, щоб увійти в будинок разом з ним", "229"),
        ("Залишитися в провулку", "56")
    ]
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(*Functions.Functions.create_inline_buttons(*buttons_data))

    await bot.send_message(user_id, text.text_394, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '395')
async def text_395(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 395)

    buttons_data = [
        ("Розділити ельмоніт на три частини", "222"),
        ("Замінувати лише один елемент", "395_2")
    ]
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(*Functions.Functions.create_inline_buttons(*buttons_data))

    await bot.send_message(user_id, text.text_395, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '395_2')
async def text_395_2(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id

    buttons_data = [
        ("Комп'ютер біля стіни навпроти дверей", "139"),
        ("Комп'ютер праворуч", "51"),
        ("Комп'ютер ліворуч", "203"),
        ("381", "381")
    ]
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(*Functions.Functions.create_inline_buttons(*buttons_data))

    await bot.send_message(user_id, text.text_395_2, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '396')
async def text_396(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_move(callback_query, 396, "374", text.text_396)
    # user_id = callback_query.from_user.id
    # Functions.DB.update_one_value(user_id, 'text_number', 396)
    # markup = types.InlineKeyboardMarkup()
    # item1 = [types.InlineKeyboardButton("Go on", callback_data="374")]
    # markup.add(*item1)
    # await bot.send_message(user_id, text.text_396, reply_markup=markup, parse_mode='Markdown')
    # await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '397')
async def text_397(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 397)

    buttons_data = [
        ("Залишитися тут", "4"),
        ("Продовжити рух коридором", "71")
    ]
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(*Functions.Functions.create_inline_buttons(*buttons_data))

    await bot.send_message(user_id, text.text_397, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '398')
async def text_398(callback_query: types.CallbackQuery):
    await Functions.Functions.handle_move(callback_query, 398, "299", text.text_398)
    # user_id = callback_query.from_user.id
    # Functions.DB.update_one_value(user_id, 'text_number', '398')
    # markup = types.InlineKeyboardMarkup()
    # item1 = [types.InlineKeyboardButton("Go on", callback_data="299")]
    # markup.add(*item1)
    # await bot.send_message(user_id, text.text_398, reply_markup=markup, parse_mode='Markdown')
    # await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '399')
async def text_399(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    Functions.DB.update_one_value(user_id, 'text_number', 399)

    buttons_data = [
        ("Дозволити супутнику постукати у двері", "145"),
        ("Кинути цю справу", "334")
    ]
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(*Functions.Functions.create_inline_buttons(*buttons_data))

    await bot.send_message(user_id, text.text_399, reply_markup=markup, parse_mode='Markdown')
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == '400')
async def text_400(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id

    # Update text_number to 400
    Functions.DB.update_one_value(user_id, 'text_number', 400)

    # Send the message
    await bot.send_message(user_id, text.text_400)

    # Delay for 5 seconds
    await asyncio.sleep(12)

    # Send the sticker
    sticker_path = 'winner_Che.webp'
    with open(sticker_path, 'rb') as sticker_file:
        await bot.send_sticker(user_id, sticker_file)

    # Answer the callback query
    await callback_query.answer()