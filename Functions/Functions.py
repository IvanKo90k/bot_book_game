import time
import asyncio
import logging
import string
from loader import dp, types, bot
from Functions.DB import get_values_if_conditions, insert_character_data, update_mastery_endurance_luck, \
    update_character_endurance, retrieve_character_data, retrieve_creature_data, update_luck, select_one_value, \
    update_one_value, update_add_enemy, clear_row_by_id
# from Handlers.User import name_button2
import random

# name_button1, name_button2 = 'Заробити 1 лексикрону', 'Заробити 2 лексикрони'

counter = 0
flag_161 = False


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


class Character:
    def __init__(self, mastery, endurance, luck):
        self.mastery = mastery
        self.endurance = endurance
        self.luck = luck


def create_character_and_insert(user_id, column1):
    # Create a character with random values
    character = create_character()

    # Insert character data into the database
    insert_character_data(user_id, column1, character)


def update_character(user_id):
    # Create a character with random values
    character = create_character()

    update_mastery_endurance_luck(user_id, character)


def create_character():
    """
    Creates a new character with random attributes.

    Returns:
    Character: A Character object with random values for mastery, endurance, and luck.
    """
    mastery = random.randint(1, 6) + 6
    endurance = random.randint(1, 6) + random.randint(1, 6) + 12
    luck = random.randint(1, 6) + 6

    return Character(mastery, endurance, luck)


def change_1_data(user_id, column_name1, column_name2, value, multiplier=1):
    """
    Modifies a numeric data entry in the database for a specific user.

    Args:
    - user_id (int): The user identifier.
    - column_name1 (str): The first column name to identify the specific data entry.
    - column_name2 (str): The second column name to identify the specific data entry.
    - value (int): The value to be added or subtracted from the existing data entry.
    - multiplier (int, optional): A factor to multiply the value before updating. Defaults to 1.

    Returns:
    None
    """
    value_old = select_one_value(user_id, column_name1, column_name2)
    updated_value = value_old + multiplier * value
    update_one_value(user_id, column_name1, updated_value)


def roll_dice_2():
    """
    Simulates the roll of two six-sided dice and returns the sum.

    Returns:
    int: The sum of the two dice rolls, ranging from 2 to 12.
    """
    return random.randint(1, 6) + random.randint(1, 6)


def if_luck(luck_threshold):
    """
    Determines if a luck roll is successful by comparing the result of rolling two dice
    with a specified luck threshold.

    Args:
    luck_threshold (int): The luck threshold to compare with the dice roll result.

    Returns:
    bool: True if the dice roll result is less than or equal to the luck threshold,
          indicating a successful luck roll. False otherwise.
    """
    roll_result = roll_dice_2()
    print(roll_result, luck_threshold)
    return roll_result <= luck_threshold


def retrieve_creature_data_by_flag(user_id, text_number, flag):
    return retrieve_creature_data(user_id, f'e_mastery_{text_number}_{flag}', f'e_endurance_{text_number}_{flag}')


def create_inline_buttons(*buttons_data):
    """
    Create a list of InlineKeyboardButton objects based on the provided data.

    Parameters:
    - buttons_data (tuple): A tuple containing pairs of label and callback_data.

    Returns:
    List[types.InlineKeyboardButton]: A list of InlineKeyboardButton objects.
    """
    return [types.InlineKeyboardButton(label, callback_data=data) for label, data in buttons_data]


def handle_creature_attack(user_id, text_number, flag, player_attack, character):
    creature_mastery_column = f'e_mastery_{text_number}_{flag}' if flag == 2 else f'e_mastery_{text_number}_1'
    creature_mastery = select_one_value(user_id, creature_mastery_column, 'user_id')
    other_creature_attack = roll_dice_2() + creature_mastery
    if other_creature_attack > player_attack and character.endurance > 0:
        character.endurance -= 2
        update_character_endurance(user_id, 'Endurance', character.endurance)

async def handle_game_over(callback_query: types.CallbackQuery, text_number: int, response_text: str):
    user_id = callback_query.from_user.id

    # Update text_number
    update_one_value(user_id, 'text_number', text_number)

    # Clear the row by ID
    clear_row_by_id(user_id)

    # Send the message
    await bot.send_message(user_id, response_text)

    # Answer the callback query
    await callback_query.answer()


async def battle_for_2(bot, user_id, character, creature):
    global counter, flag_161
    m1, m2 = 'Наступний удар', 'Випробувати Удачу'
    text_number = select_one_value(user_id, 'text_number', 'user_id')
    flag24 = select_one_value(user_id, 'flag24', 'user_id')
    flag113 = select_one_value(user_id, 'flag113', 'user_id')
    flag172 = select_one_value(user_id, 'flag172', 'user_id')
    flag234 = select_one_value(user_id, 'flag234', 'user_id')
    flag190_2 = select_one_value(user_id, 'flag190_2', 'user_id')
    sand243 = select_one_value(user_id, 'sand243', 'user_id')
    rounds243 = select_one_value(user_id, 'rounds243', 'user_id')
    flag244 = select_one_value(user_id, 'flag244', 'user_id')

    # Step 1: Roll dice for creature's attack
    creature_attack = roll_dice_2() + creature.mastery

    if text_number == 24:
        creature_mastery_column = f'e_mastery_{text_number}_1' if flag24 == 2 else f'e_mastery_{text_number}_2'
        creature_mastery = select_one_value(user_id, creature_mastery_column, 'user_id')
        other_creature_attack = roll_dice_2() + creature_mastery

    elif text_number == 113:
        creature_mastery_column = f'e_mastery_{text_number}_1' if flag113 == 2 else f'e_mastery_{text_number}_2'
        creature_mastery = select_one_value(user_id, creature_mastery_column, 'user_id')
        other_creature_attack = roll_dice_2() + creature_mastery

    elif text_number == 161:
        endurance_column = 'e_endurance_161'
        dice_roll_result = roll_dice_2()
        print(dice_roll_result)

        if dice_roll_result < 7:
            target = character
        else:
            target = creature
            flag_161 = True

        target.endurance -= 2
        update_character_endurance(user_id, endurance_column if dice_roll_result >= 7 else 'Endurance',
                                   target.endurance)
        endurance_last = select_one_value(user_id, endurance_column, 'user_id')
        endurance = select_one_value(user_id, 'Endurance', 'user_id')
        markup = types.InlineKeyboardMarkup(row_width=2)
        if character.luck > 0 and creature.endurance > 0 and character.endurance > 0:
            if flag_161 == True:
                item1 = [types.InlineKeyboardButton(m1, callback_data='fight'),
                         types.InlineKeyboardButton(m2, callback_data='way2')]
                markup.add(*item1)
                await bot.send_message(user_id,
                                       f"Player damages the creature! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                       reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
            elif flag_161 == False:
                item1 = [types.InlineKeyboardButton(m1, callback_data='fight'),
                         types.InlineKeyboardButton(m2, callback_data='way3')]
                markup.add(*item1)
                await bot.send_message(user_id,
                                       f"Creature damages the player! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                       reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі

        elif character.luck <= 0 and creature.endurance > 0 and character.endurance > 0:  # якщо відсутня можливість перевірити Удачу, але суперник ще живий
            item1 = [types.InlineKeyboardButton(m1, callback_data='4 rounds')]
            markup.add(*item1)
            if flag_161 == True:
                await bot.send_message(user_id,
                                       f"Player damages the creature! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                       reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
            elif flag_161 == False:
                await bot.send_message(user_id,
                                       f"Creature damages the player! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                       reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
        elif endurance_last <= 0:
            item1 = [types.InlineKeyboardButton('135', callback_data='135')]
            markup.add(*item1)
            await bot.send_message(user_id, 'The player wins!', reply_markup=markup, parse_mode='Markdown')
        elif endurance <= 0:
            await bot.send_message(user_id, "Ти програв! Починай спочатку.")  # бот повідомляє про програш
        flag_161 = False

    elif text_number == 172:
        creature_mastery_column = f'e_mastery_{text_number}_1' if flag172 == 2 else f'e_mastery_{text_number}_2'
        creature_mastery = select_one_value(user_id, creature_mastery_column, 'user_id')
        other_creature_attack = roll_dice_2() + creature_mastery

    elif text_number == 234:
        creature_mastery_column = f'e_mastery_{text_number}_1' if flag234 == 2 else f'e_mastery_{text_number}_2'
        creature_mastery = select_one_value(user_id, creature_mastery_column, 'user_id')
        other_creature_attack = roll_dice_2() + creature_mastery

    elif text_number == 243 and sand243 == 2:
        if rounds243 < 3:
            change_1_data(user_id, 'rounds243', 'user_id', 1)
        elif rounds243 == 3:
            change_1_data(user_id, 'Mastery', 'user_id', 1)

    elif text_number == 244:
        creature_mastery_column = f'e_mastery_{text_number}_2' if flag244 == 1 else f'e_mastery_{text_number}_1'
        creature_mastery = select_one_value(user_id, creature_mastery_column, 'user_id')
        other_creature_attack = roll_dice_2() + creature_mastery

    # Step 2: Roll dice for player's attack
    player_attack = roll_dice_2() + character.mastery
    print('player_attack = ', player_attack, 'creature_attack = ', creature_attack)

    # Update character endurance based on text_number
    if player_attack > creature_attack:
        if text_number != 190:
            creature.endurance -= 2

        if text_number in [2, 3, 4, 17, 55, 82, 84, 104, 106, 133, 150, 206, 215, 243, 295, 298, 313, 341, 351, 366,
                           367,
                           373, 375, 391]:
            endurance_mapping = {
                2: 'e_endurance_2',
                3: 'e_endurance_3',
                4: 'e_endurance_4',
                17: 'e_endurance_17',
                55: 'e_endurance_55',
                82: 'e_endurance_82',
                84: 'e_endurance_84',
                104: 'e_endurance_104',
                106: 'e_endurance_106',
                133: 'e_endurance_133',
                150: 'e_endurance_150',
                206: 'e_endurance_206',
                215: 'e_endurance_215',
                243: 'e_endurance_243',
                295: 'e_endurance_295',
                298: 'e_endurance_298',
                313: 'e_endurance_313',
                341: 'e_endurance_341',
                351: 'e_endurance_351',
                366: 'e_endurance_366',
                367: 'e_endurance_367',
                373: 'e_endurance_373',
                375: 'e_endurance_375',
                391: 'e_endurance_391',
            }
            update_character_endurance(user_id, endurance_mapping.get(text_number, ''), creature.endurance)

        elif text_number == 24:
            enemy1_endurance = select_one_value(user_id, f'e_endurance_{text_number}_1', 'user_id')
            enemy2_endurance = select_one_value(user_id, f'e_endurance_{text_number}_2', 'user_id')
            if flag24 in [1, 2]:
                update_character_endurance(user_id, f'e_endurance_{text_number}_{flag24}', creature.endurance)
                if (flag24 == 1 and enemy2_endurance > 0) or (flag24 == 2 and enemy1_endurance > 0):
                    if player_attack < other_creature_attack:
                        character.endurance -= 2
                update_character_endurance(user_id, 'Endurance', character.endurance)

        elif text_number == 35:
            CRITICAL_HIT_THRESHOLD = 6
            endurance_column = f'e_endurance_{text_number}'

            new_endurance = 0 if random.randint(1, 6) == CRITICAL_HIT_THRESHOLD else creature.endurance
            update_character_endurance(user_id, endurance_column, new_endurance)


        elif text_number == 107:
            dogfight_107 = select_one_value(user_id, f'dogfight_{text_number}', 'user_id')
            endurance_column = f'e_endurance_{text_number}'

            if f'dogfight_{text_number}' == 1:
                update_character_endurance(user_id, endurance_column, creature.endurance)
            elif f'dogfight_{text_number}' == 2:  # якщо рукопашний бій
                CRITICAL_HIT_THRESHOLD = 6
                new_endurance = 0 if random.randint(1, 6) == CRITICAL_HIT_THRESHOLD else creature.endurance
                update_character_endurance(user_id, endurance_column, new_endurance)


        elif text_number == 113 and flag113 in {1, 2}:
            enemy1_endurance = select_one_value(user_id, f'e_endurance_{text_number}_1', 'user_id')
            enemy2_endurance = select_one_value(user_id, f'e_endurance_{text_number}_2', 'user_id')
            endurance_column = f'e_endurance_{text_number}_{flag113}'
            CRITICAL_HIT_THRESHOLD = 6

            new_endurance = 0 if random.randint(1, 6) == CRITICAL_HIT_THRESHOLD else creature.endurance
            update_character_endurance(user_id, endurance_column, new_endurance)

            if (flag113 == 1 and enemy2_endurance > 0) or (flag113 == 2 and enemy1_endurance > 0):
                if player_attack < other_creature_attack:
                    character.endurance -= 2
            update_character_endurance(user_id, 'Endurance', character.endurance)

        elif text_number == 124:
            CRITICAL_HIT_THRESHOLD = 6
            endurance_column = f'e_endurance_{text_number}'

            new_endurance = 0 if random.randint(1, 6) == CRITICAL_HIT_THRESHOLD else creature.endurance
            update_character_endurance(user_id, endurance_column, new_endurance)
            if new_endurance > 0 and random.randint(1, 6) in {5, 6}:
                character.endurance -= 2
                update_character_endurance(user_id, 'Endurance', character.endurance)

        elif text_number == 136:
            update_character_endurance(user_id, f'e_endurance_{text_number}', creature.endurance)
            if character.endurance > 0 and random.randint(1, 6) in {5, 6}:
                character.endurance -= 2
                update_character_endurance(user_id, 'Endurance', character.endurance)

        elif text_number == 157:
            CRITICAL_HIT_THRESHOLD = 6
            endurance_column = f'e_endurance_{text_number}'

            new_endurance = 0 if random.randint(1, 6) == CRITICAL_HIT_THRESHOLD else creature.endurance
            update_character_endurance(user_id, endurance_column, new_endurance)

        elif text_number == 165:
            CRITICAL_HIT_THRESHOLD = 6
            endurance_column = f'e_endurance_{text_number}'

            new_endurance = 0 if random.randint(1, 6) == CRITICAL_HIT_THRESHOLD else creature.endurance
            update_character_endurance(user_id, endurance_column, new_endurance)

        elif text_number == 172:
            enemy1_endurance = select_one_value(user_id, f'e_endurance_{text_number}_1', 'user_id')
            enemy2_endurance = select_one_value(user_id, f'e_endurance_{text_number}_2', 'user_id')
            if flag172 in [1, 2]:
                update_character_endurance(user_id, f'e_endurance_{text_number}_{flag172}', creature.endurance)
                if (flag172 == 1 and enemy2_endurance > 0) or (flag172 == 2 and enemy1_endurance > 0):
                    if player_attack < other_creature_attack:
                        character.endurance -= 2
                update_character_endurance(user_id, 'Endurance', character.endurance)

        elif text_number == 224:
            CRITICAL_HIT_THRESHOLD = 6
            endurance_column = f'e_endurance_{text_number}'

            new_endurance = 0 if random.randint(1, 6) == CRITICAL_HIT_THRESHOLD else creature.endurance
            update_character_endurance(user_id, endurance_column, new_endurance)

        elif text_number == 234:
            enemy1_endurance = select_one_value(user_id, f'e_endurance_{text_number}_1', 'user_id')
            enemy2_endurance = select_one_value(user_id, f'e_endurance_{text_number}_2', 'user_id')
            if flag234 in [1, 2]:
                update_character_endurance(user_id, f'e_endurance_{text_number}_{flag234}', creature.endurance)
                if (flag234 == 1 and enemy2_endurance > 0) or (flag234 == 2 and enemy1_endurance > 0):
                    if player_attack < other_creature_attack:
                        character.endurance -= 2
                # оскільки перший суперник - сіверянин, то він може вдарити хвостом:
                if enemy1_endurance > 0 and character.endurance > 0 and random.randint(1, 6) in {5, 6}:
                    character.endurance -= 2
                update_character_endurance(user_id, 'Endurance', character.endurance)

        elif text_number == 244 and flag244 in {1, 2}:
            enemy1_endurance = select_one_value(user_id, f'e_endurance_{text_number}_1', 'user_id')
            enemy2_endurance = select_one_value(user_id, f'e_endurance_{text_number}_2', 'user_id')
            endurance_column = f'e_endurance_{text_number}_{flag244}'
            CRITICAL_HIT_THRESHOLD = 6

            new_endurance = 0 if random.randint(1, 6) == CRITICAL_HIT_THRESHOLD else creature.endurance
            update_character_endurance(user_id, endurance_column, new_endurance)

            if (flag244 == 1 and enemy2_endurance > 0) or (flag244 == 2 and enemy1_endurance > 0):
                if player_attack < other_creature_attack:
                    character.endurance -= 2
            update_character_endurance(user_id, 'Endurance', character.endurance)

        elif text_number == 289:
            endurance_column = f'e_endurance_{text_number}'
            CRITICAL_HIT_THRESHOLD = 6
            new_endurance = 0 if random.randint(1, 6) == CRITICAL_HIT_THRESHOLD else creature.endurance
            update_character_endurance(user_id, endurance_column, new_endurance)
            if character.endurance > 0 and random.randint(1, 6) in {5, 6}:
                character.endurance -= 2
                update_character_endurance(user_id, 'Endurance', character.endurance)

        # Check luck and creature endurance for different scenarios
        if character.luck > 0 and creature.endurance > 0:
            if text_number == 2:
                markup = types.InlineKeyboardMarkup(row_width=2)
                item1 = [types.InlineKeyboardButton(m1, callback_data='4 rounds'),
                         types.InlineKeyboardButton(m2, callback_data='way2')]
                markup.add(*item1)
                await bot.send_message(user_id,
                                       f"Player damages the creature! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                       reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
            elif text_number in [3, 4, 17, 35, 55, 82, 84, 104, 106, 107, 124, 133, 136, 150, 157, 165, 206, 215, 224,
                                 243, 289, 295, 298, 313, 341, 351, 366, 367, 375, 391]:
                markup = types.InlineKeyboardMarkup(row_width=2)
                item1 = [types.InlineKeyboardButton(m1, callback_data='fight'),
                         types.InlineKeyboardButton(m2, callback_data='way2')]
                markup.add(*item1)
                await bot.send_message(user_id,
                                       f"Player damages the creature! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                       reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
            elif text_number == 24:
                enemy1_endurance = select_one_value(user_id, f'e_endurance_{text_number}_1', 'user_id')
                enemy2_endurance = select_one_value(user_id, f'e_endurance_{text_number}_2', 'user_id')
                if enemy1_endurance > 0 and enemy2_endurance > 0:
                    markup = types.InlineKeyboardMarkup(row_width=1)
                    item1 = [types.InlineKeyboardButton("Битися з першим аркадіанцем", callback_data='first_a'),
                             types.InlineKeyboardButton("Битися з другим аркадіанцем", callback_data='second_a'),
                             types.InlineKeyboardButton(m2, callback_data='way2')]
                    markup.add(*item1)
                    if player_attack > other_creature_attack:
                        await bot.send_message(user_id,
                                               f"Player damages the creature! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                               reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                    elif player_attack < other_creature_attack:
                        await bot.send_message(user_id,
                                               f"Player damages the creature, but another creature damages the player! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                               reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                elif enemy1_endurance <= 0 and enemy2_endurance > 0:
                    markup = types.InlineKeyboardMarkup(row_width=1)
                    item1 = [types.InlineKeyboardButton("Битися з другим аркадіанцем", callback_data='second_a'),
                             types.InlineKeyboardButton(m2, callback_data='way2')]
                    markup.add(*item1)
                    if player_attack > other_creature_attack:
                        await bot.send_message(user_id,
                                               f"Player damages the creature! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                               reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                    elif player_attack < other_creature_attack:
                        await bot.send_message(user_id,
                                               f"Player damages the creature, but another creature damages the player! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                               reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                elif enemy1_endurance > 0 and enemy2_endurance <= 0:
                    markup = types.InlineKeyboardMarkup(row_width=1)
                    item1 = [types.InlineKeyboardButton("Битися з першим аркадіанцем", callback_data='first_a'),
                             types.InlineKeyboardButton(m2, callback_data='way2')]
                    markup.add(*item1)
                    if player_attack > other_creature_attack:
                        await bot.send_message(user_id,
                                               f"Player damages the creature! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                               reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                    elif player_attack < other_creature_attack:
                        await bot.send_message(user_id,
                                               f"Player damages the creature, but another creature damages the player! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                               reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
            elif text_number == 113:
                enemy1_endurance = select_one_value(user_id, f'e_endurance_{text_number}_1', 'user_id')
                enemy2_endurance = select_one_value(user_id, f'e_endurance_{text_number}_2', 'user_id')
                if enemy1_endurance > 0 and enemy2_endurance > 0:
                    markup = types.InlineKeyboardMarkup(row_width=1)
                    item1 = [types.InlineKeyboardButton("Битися з Грусом", callback_data='grus'),
                             types.InlineKeyboardButton("Битися з Індусом", callback_data='indus'),
                             types.InlineKeyboardButton(m2, callback_data='way2')]
                    markup.add(*item1)
                    if player_attack > other_creature_attack:
                        await bot.send_message(user_id,
                                               f"Player damages the creature! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                               reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                    elif player_attack < other_creature_attack:
                        await bot.send_message(user_id,
                                               f"Player damages the creature, but another creature damages the player! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                               reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                elif enemy1_endurance <= 0 and enemy2_endurance > 0:
                    markup = types.InlineKeyboardMarkup(row_width=1)
                    item1 = [types.InlineKeyboardButton("Битися з Індусом", callback_data='indus'),
                             types.InlineKeyboardButton(m2, callback_data='way2')]
                    markup.add(*item1)
                    if player_attack > other_creature_attack:
                        await bot.send_message(user_id,
                                               f"Player damages the creature! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                               reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                    elif player_attack < other_creature_attack:
                        await bot.send_message(user_id,
                                               f"Player damages the creature, but another creature damages the player! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                               reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                elif enemy1_endurance > 0 and enemy2_endurance <= 0:
                    markup = types.InlineKeyboardMarkup(row_width=1)
                    item1 = [types.InlineKeyboardButton("Битися з Грусом", callback_data='grus'),
                             types.InlineKeyboardButton(m2, callback_data='way2')]
                    markup.add(*item1)
                    if player_attack > other_creature_attack:
                        await bot.send_message(user_id,
                                               f"Player damages the creature! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                               reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                    elif player_attack < other_creature_attack:
                        await bot.send_message(user_id,
                                               f"Player damages the creature, but another creature damages the player! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                               reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі

            elif text_number == 172:
                enemy1_endurance = select_one_value(user_id, f'e_endurance_{text_number}_1', 'user_id')
                enemy2_endurance = select_one_value(user_id, f'e_endurance_{text_number}_2', 'user_id')
                if enemy1_endurance > 0 and enemy2_endurance > 0:
                    markup = types.InlineKeyboardMarkup(row_width=1)
                    item1 = [types.InlineKeyboardButton("Битися з першим стражником", callback_data='first_g'),
                             types.InlineKeyboardButton("Битися з другим стражником", callback_data='second_g'),
                             types.InlineKeyboardButton(m2, callback_data='way2')]
                    markup.add(*item1)
                    if player_attack > other_creature_attack:
                        await bot.send_message(user_id,
                                               f"Player damages the creature! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                               reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                    elif player_attack < other_creature_attack:
                        await bot.send_message(user_id,
                                               f"Player damages the creature, but another creature damages the player! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                               reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                elif enemy1_endurance <= 0 and enemy2_endurance > 0:
                    markup = types.InlineKeyboardMarkup(row_width=1)
                    item1 = [types.InlineKeyboardButton("Битися з другим стражником", callback_data='second_g'),
                             types.InlineKeyboardButton(m2, callback_data='way2')]
                    markup.add(*item1)
                    if player_attack > other_creature_attack:
                        await bot.send_message(user_id,
                                               f"Player damages the creature! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                               reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                    elif player_attack < other_creature_attack:
                        await bot.send_message(user_id,
                                               f"Player damages the creature, but another creature damages the player! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                               reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                elif enemy1_endurance > 0 and enemy2_endurance <= 0:
                    markup = types.InlineKeyboardMarkup(row_width=1)
                    item1 = [types.InlineKeyboardButton("Битися з першим стражником", callback_data='first_g'),
                             types.InlineKeyboardButton(m2, callback_data='way2')]
                    markup.add(*item1)
                    if player_attack > other_creature_attack:
                        await bot.send_message(user_id,
                                               f"Player damages the creature! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                               reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                    elif player_attack < other_creature_attack:
                        await bot.send_message(user_id,
                                               f"Player damages the creature, but another creature damages the player! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                               reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
            elif text_number == 190:
                markup = types.InlineKeyboardMarkup(row_width=1)
                if creature.mastery > 0:
                    item1 = [types.InlineKeyboardButton('Відняти 2 пункти Витривалості робота',
                                                        callback_data='deduct_2_endurance'),
                             types.InlineKeyboardButton('Знизити Майстерність робота на 1 бал',
                                                        callback_data='decrease_mastery')]
                else:
                    item1 = [types.InlineKeyboardButton('Відняти 2 пункти Витривалості робота',
                                                        callback_data='deduct_2_endurance')]
                markup.add(*item1)
                await bot.send_message(user_id, f"Перемога в цьому раунді за вами.",
                                       reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі

            elif text_number == 234:
                enemy1_endurance = select_one_value(user_id, f'e_endurance_{text_number}_1', 'user_id')
                enemy2_endurance = select_one_value(user_id, f'e_endurance_{text_number}_2', 'user_id')
                if enemy1_endurance > 0 and enemy2_endurance > 0:
                    markup = types.InlineKeyboardMarkup(row_width=1)
                    item1 = [types.InlineKeyboardButton("Битися з жителем півночі", callback_data='first_a_n'),
                             types.InlineKeyboardButton("Битися з другим аркадіанцем", callback_data='second_a_2'),
                             types.InlineKeyboardButton(m2, callback_data='way2')]
                    markup.add(*item1)
                    if player_attack > other_creature_attack:
                        await bot.send_message(user_id,
                                               f"Player damages the creature! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                               reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                    elif player_attack < other_creature_attack:
                        await bot.send_message(user_id,
                                               f"Player damages the creature, but another creature damages the player! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                               reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                elif enemy1_endurance <= 0 and enemy2_endurance > 0:
                    markup = types.InlineKeyboardMarkup(row_width=1)
                    item1 = [types.InlineKeyboardButton("Битися з другим аркадіанцем", callback_data='second_a_2'),
                             types.InlineKeyboardButton(m2, callback_data='way2')]
                    markup.add(*item1)
                    if player_attack > other_creature_attack:
                        await bot.send_message(user_id,
                                               f"Player damages the creature! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                               reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                    elif player_attack < other_creature_attack:
                        await bot.send_message(user_id,
                                               f"Player damages the creature, but another creature damages the player! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                               reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                elif enemy1_endurance > 0 and enemy2_endurance <= 0:
                    markup = types.InlineKeyboardMarkup(row_width=1)
                    item1 = [types.InlineKeyboardButton("Битися з жителем півночі", callback_data='first_a_n'),
                             types.InlineKeyboardButton(m2, callback_data='way2')]
                    markup.add(*item1)
                    if player_attack > other_creature_attack:
                        await bot.send_message(user_id,
                                               f"Player damages the creature! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                               reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                    elif player_attack < other_creature_attack:
                        await bot.send_message(user_id,
                                               f"Player damages the creature, but another creature damages the player! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                               reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі

            elif text_number == 244:
                if character.endurance > 4:
                    enemy1_endurance = select_one_value(user_id, f'e_endurance_{text_number}_1', 'user_id')
                    enemy2_endurance = select_one_value(user_id, f'e_endurance_{text_number}_2', 'user_id')
                    if enemy1_endurance > 0 and enemy2_endurance > 0:
                        markup = types.InlineKeyboardMarkup(row_width=1)
                        item1 = [types.InlineKeyboardButton("Перший громила", callback_data="first_h"),
                                 types.InlineKeyboardButton("Другий громила", callback_data="second_h"),
                                 types.InlineKeyboardButton(m2, callback_data='way2')]
                        markup.add(*item1)
                        if player_attack > other_creature_attack:
                            await bot.send_message(user_id,
                                                   f"Player damages the creature! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                                   reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                        elif player_attack < other_creature_attack:
                            await bot.send_message(user_id,
                                                   f"Player damages the creature, but another creature damages the player! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                                   reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                    elif enemy1_endurance <= 0 and enemy2_endurance > 0:
                        markup = types.InlineKeyboardMarkup(row_width=1)
                        item1 = [types.InlineKeyboardButton("Другий громила", callback_data="second_h"),
                                 types.InlineKeyboardButton(m2, callback_data='way2')]
                        markup.add(*item1)
                        if player_attack > other_creature_attack:
                            await bot.send_message(user_id,
                                                   f"Player damages the creature! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                                   reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                        elif player_attack < other_creature_attack:
                            await bot.send_message(user_id,
                                                   f"Player damages the creature, but another creature damages the player! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                                   reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                    elif enemy1_endurance > 0 and enemy2_endurance <= 0:
                        markup = types.InlineKeyboardMarkup(row_width=1)
                        item1 = [types.InlineKeyboardButton("Перший громила", callback_data="first_h"),
                                 types.InlineKeyboardButton(m2, callback_data='way2')]
                        markup.add(*item1)
                        if player_attack > other_creature_attack:
                            await bot.send_message(user_id,
                                                   f"Player damages the creature! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                                   reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                        elif player_attack < other_creature_attack:
                            await bot.send_message(user_id,
                                                   f"Player damages the creature, but another creature damages the player! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                                   reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                else:
                    update_one_value(user_id, 'Endurance', 4)
                    item1 = [types.InlineKeyboardButton('Go on', callback_data='337')]
                    markup.add(*item1)
                    await bot.send_message(user_id,
                                           'Бій завершено. Ваша Витривалість становить 4 бали. Ваші супротивники втікають.',
                                           reply_markup=markup, parse_mode='Markdown')
            elif text_number == 373:
                markup = types.InlineKeyboardMarkup(row_width=2)
                if creature.endurance > 6:
                    item1 = [types.InlineKeyboardButton(m1, callback_data='fight'),
                             types.InlineKeyboardButton(m2, callback_data='way2')]
                    markup.add(*item1)
                    await bot.send_message(user_id,
                                           f"Player damages the creature! Player endurance: {character.endurance}, Creature endurance: {creature.endurance - 6}",
                                           reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                else:
                    mastery = select_one_value(user_id, 'e_mastery_373', 'user_id')
                    if creature.endurance == 6 and mastery == 7:
                        update_one_value(user_id, 'e_mastery_373', 6)
                        item1 = [types.InlineKeyboardButton(m1, callback_data='fight')]
                        markup.add(*item1)
                        await bot.send_message(user_id,
                                               f"Першого аркадіанця переможено! Player endurance: {character.endurance}, Creature endurance: 0. Переходьте до бою з другим аркадіанцем.",
                                               reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                    elif creature.endurance < 6 and mastery == 7:
                        update_one_value(user_id, 'e_endurance_373', 6)
                        update_one_value(user_id, 'e_mastery_373', 6)
                        item1 = [types.InlineKeyboardButton(m1, callback_data='fight')]
                        markup.add(*item1)
                        await bot.send_message(user_id,
                                               f"Першого аркадіанця переможено! Player endurance: {character.endurance}, Creature endurance: 0. Переходьте до бою з другим аркадіанцем.",
                                               reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                    elif creature.endurance < 6 and mastery == 6:
                        item1 = [types.InlineKeyboardButton(m1, callback_data='fight'),
                                 types.InlineKeyboardButton(m2, callback_data='way2')]
                        markup.add(*item1)
                        await bot.send_message(user_id,
                                               f"Player damages the creature! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                               reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі


        elif character.luck <= 0 and creature.endurance > 0:  # якщо відсутня можливість застосувати Удачу, але суперник ще живий
            markup = types.InlineKeyboardMarkup()
            if text_number in [2, 3, 4, 17, 35, 55, 82, 84, 104, 106, 107, 124, 133, 136, 150, 157, 165, 206, 215, 224,
                               243, 289, 295, 298, 313, 341, 351, 366, 367, 375, 391]:
                item1 = [types.InlineKeyboardButton(m1, callback_data='4 rounds')]
                markup.add(*item1)
                await bot.send_message(user_id,
                                       f"Player damages the creature! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                       reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
            elif text_number == 24:
                enemy1_endurance = select_one_value(user_id, f'e_endurance_{text_number}_1', 'user_id')
                enemy2_endurance = select_one_value(user_id, f'e_endurance_{text_number}_2', 'user_id')
                if enemy1_endurance > 0 and enemy2_endurance > 0:
                    markup = types.InlineKeyboardMarkup(row_width=1)
                    item1 = [types.InlineKeyboardButton("Битися з першим аркадіанцем", callback_data='first_a'),
                             types.InlineKeyboardButton("Битися з другим аркадіанцем", callback_data='second_a')]
                    markup.add(*item1)
                    if player_attack > other_creature_attack:
                        await bot.send_message(user_id,
                                               f"Player damages the creature! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                               reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                    elif player_attack < other_creature_attack:
                        await bot.send_message(user_id,
                                               f"Player damages the creature, but another creature damages the player! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                               reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                elif enemy1_endurance <= 0 and enemy2_endurance > 0:
                    markup = types.InlineKeyboardMarkup(row_width=1)
                    item1 = [types.InlineKeyboardButton("Битися з другим аркадіанцем", callback_data='second_a')]
                    markup.add(*item1)
                    if player_attack > other_creature_attack:
                        await bot.send_message(user_id,
                                               f"Player damages the creature! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                               reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                    elif player_attack < other_creature_attack:
                        await bot.send_message(user_id,
                                               f"Player damages the creature, but another creature damages the player! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                               reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                elif enemy1_endurance > 0 and enemy2_endurance <= 0:
                    markup = types.InlineKeyboardMarkup(row_width=1)
                    item1 = [types.InlineKeyboardButton("Битися з першим аркадіанцем", callback_data='first_a')]
                    markup.add(*item1)
                    if player_attack > other_creature_attack:
                        await bot.send_message(user_id,
                                               f"Player damages the creature! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                               reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                    elif player_attack < other_creature_attack:
                        await bot.send_message(user_id,
                                               f"Player damages the creature, but another creature damages the player! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                               reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
            elif text_number == 113:
                enemy1_endurance = select_one_value(user_id, f'e_endurance_{text_number}_1', 'user_id')
                enemy2_endurance = select_one_value(user_id, f'e_endurance_{text_number}_2', 'user_id')
                if enemy1_endurance > 0 and enemy2_endurance > 0:
                    markup = types.InlineKeyboardMarkup(row_width=1)
                    item1 = [types.InlineKeyboardButton("Битися з Грусом", callback_data='grus'),
                             types.InlineKeyboardButton("Битися з Індусом", callback_data='indus')]
                    markup.add(*item1)
                    if player_attack > other_creature_attack:
                        await bot.send_message(user_id,
                                               f"Player damages the creature! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                               reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                    elif player_attack < other_creature_attack:
                        await bot.send_message(user_id,
                                               f"Player damages the creature, but another creature damages the player! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                               reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                elif enemy1_endurance <= 0 and enemy2_endurance > 0:
                    markup = types.InlineKeyboardMarkup(row_width=1)
                    item1 = [types.InlineKeyboardButton("Битися з Індусом", callback_data='indus')]
                    markup.add(*item1)
                    if player_attack > other_creature_attack:
                        await bot.send_message(user_id,
                                               f"Player damages the creature! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                               reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                    elif player_attack < other_creature_attack:
                        await bot.send_message(user_id,
                                               f"Player damages the creature, but another creature damages the player! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                               reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                elif enemy1_endurance > 0 and enemy2_endurance <= 0:
                    markup = types.InlineKeyboardMarkup(row_width=1)
                    item1 = [types.InlineKeyboardButton("Битися з Грусом", callback_data='grus')]
                    markup.add(*item1)
                    if player_attack > other_creature_attack:
                        await bot.send_message(user_id,
                                               f"Player damages the creature! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                               reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                    elif player_attack < other_creature_attack:
                        await bot.send_message(user_id,
                                               f"Player damages the creature, but another creature damages the player! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                               reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
            elif text_number == 172:
                enemy1_endurance = select_one_value(user_id, f'e_endurance_{text_number}_1', 'user_id')
                enemy2_endurance = select_one_value(user_id, f'e_endurance_{text_number}_2', 'user_id')
                if enemy1_endurance > 0 and enemy2_endurance > 0:
                    markup = types.InlineKeyboardMarkup(row_width=1)
                    item1 = [types.InlineKeyboardButton("Битися з першим стражником", callback_data='first_g'),
                             types.InlineKeyboardButton("Битися з другим стражником", callback_data='second_g')]
                    markup.add(*item1)
                    if player_attack > other_creature_attack:
                        await bot.send_message(user_id,
                                               f"Player damages the creature! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                               reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                    elif player_attack < other_creature_attack:
                        await bot.send_message(user_id,
                                               f"Player damages the creature, but another creature damages the player! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                               reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                elif enemy1_endurance <= 0 and enemy2_endurance > 0:
                    markup = types.InlineKeyboardMarkup(row_width=1)
                    item1 = [types.InlineKeyboardButton("Битися з другим стражником", callback_data='second_g')]
                    markup.add(*item1)
                    if player_attack > other_creature_attack:
                        await bot.send_message(user_id,
                                               f"Player damages the creature! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                               reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                    elif player_attack < other_creature_attack:
                        await bot.send_message(user_id,
                                               f"Player damages the creature, but another creature damages the player! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                               reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                elif enemy1_endurance > 0 and enemy2_endurance <= 0:
                    markup = types.InlineKeyboardMarkup(row_width=1)
                    item1 = [types.InlineKeyboardButton("Битися з першим стражником", callback_data='first_g')]
                    markup.add(*item1)
                    if player_attack > other_creature_attack:
                        await bot.send_message(user_id,
                                               f"Player damages the creature! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                               reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                    elif player_attack < other_creature_attack:
                        await bot.send_message(user_id,
                                               f"Player damages the creature, but another creature damages the player! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                               reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
            elif text_number == 190:
                markup = types.InlineKeyboardMarkup(row_width=1)
                if creature.mastery > 0:
                    item1 = [types.InlineKeyboardButton('Відняти 2 пункти Витривалості робота',
                                                        callback_data='deduct_2_endurance'),
                             types.InlineKeyboardButton('Знизити Майстерність робота на 1 бал',
                                                        callback_data='decrease_mastery')]
                else:
                    item1 = [types.InlineKeyboardButton('Відняти 2 пункти Витривалості робота',
                                                        callback_data='deduct_2_endurance')]
                markup.add(*item1)
                await bot.send_message(user_id, f"Перемога в цьому раунді за вами.",
                                       reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі

            elif text_number == 234:
                enemy1_endurance = select_one_value(user_id, f'e_endurance_{text_number}_1', 'user_id')
                enemy2_endurance = select_one_value(user_id, f'e_endurance_{text_number}_2', 'user_id')
                if enemy1_endurance > 0 and enemy2_endurance > 0:
                    markup = types.InlineKeyboardMarkup(row_width=1)
                    item1 = [types.InlineKeyboardButton("Битися з жителем півночі", callback_data='first_a_n'),
                             types.InlineKeyboardButton("Битися з другим аркадіанцем", callback_data='second_a_2')]
                    markup.add(*item1)
                    if player_attack > other_creature_attack:
                        await bot.send_message(user_id,
                                               f"Player damages the creature! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                               reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                    elif player_attack < other_creature_attack:
                        await bot.send_message(user_id,
                                               f"Player damages the creature, but another creature damages the player! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                               reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                elif enemy1_endurance <= 0 and enemy2_endurance > 0:
                    markup = types.InlineKeyboardMarkup(row_width=1)
                    item1 = [types.InlineKeyboardButton("Битися з другим аркадіанцем", callback_data='second_a_2')]
                    markup.add(*item1)
                    if player_attack > other_creature_attack:
                        await bot.send_message(user_id,
                                               f"Player damages the creature! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                               reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                    elif player_attack < other_creature_attack:
                        await bot.send_message(user_id,
                                               f"Player damages the creature, but another creature damages the player! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                               reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                elif enemy1_endurance > 0 and enemy2_endurance <= 0:
                    markup = types.InlineKeyboardMarkup(row_width=1)
                    item1 = [types.InlineKeyboardButton("Битися з жителем півночі", callback_data='first_a_n')]
                    markup.add(*item1)
                    if player_attack > other_creature_attack:
                        await bot.send_message(user_id,
                                               f"Player damages the creature! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                               reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                    elif player_attack < other_creature_attack:
                        await bot.send_message(user_id,
                                               f"Player damages the creature, but another creature damages the player! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                               reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
            elif text_number == 244:
                if character.endurance > 4:
                    enemy1_endurance = select_one_value(user_id, f'e_endurance_{text_number}_1', 'user_id')
                    enemy2_endurance = select_one_value(user_id, f'e_endurance_{text_number}_2', 'user_id')
                    if enemy1_endurance > 0 and enemy2_endurance > 0:
                        markup = types.InlineKeyboardMarkup(row_width=1)
                        item1 = [types.InlineKeyboardButton("Перший громила", callback_data="first_h"),
                                 types.InlineKeyboardButton("Другий громила", callback_data="second_h")]
                        markup.add(*item1)
                        if player_attack > other_creature_attack:
                            await bot.send_message(user_id,
                                                   f"Player damages the creature! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                                   reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                        elif player_attack < other_creature_attack:
                            await bot.send_message(user_id,
                                                   f"Player damages the creature, but another creature damages the player! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                                   reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                    elif enemy1_endurance <= 0 and enemy2_endurance > 0:
                        markup = types.InlineKeyboardMarkup(row_width=1)
                        item1 = [types.InlineKeyboardButton("Другий громила", callback_data="second_h")]
                        markup.add(*item1)
                        if player_attack > other_creature_attack:
                            await bot.send_message(user_id,
                                                   f"Player damages the creature! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                                   reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                        elif player_attack < other_creature_attack:
                            await bot.send_message(user_id,
                                                   f"Player damages the creature, but another creature damages the player! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                                   reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                    elif enemy1_endurance > 0 and enemy2_endurance <= 0:
                        markup = types.InlineKeyboardMarkup(row_width=1)
                        item1 = [types.InlineKeyboardButton("Перший громила", callback_data="first_h")]
                        markup.add(*item1)
                        if player_attack > other_creature_attack:
                            await bot.send_message(user_id,
                                                   f"Player damages the creature! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                                   reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                        elif player_attack < other_creature_attack:
                            await bot.send_message(user_id,
                                                   f"Player damages the creature, but another creature damages the player! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                                   reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                else:
                    update_one_value(user_id, 'Endurance', 4)
                    item1 = [types.InlineKeyboardButton('Go on', callback_data='337')]
                    markup.add(*item1)
                    await bot.send_message(user_id,
                                           'Бій завершено. Ваша Витривалість становить 4 бали. Ваші супротивники втікають.',
                                           reply_markup=markup, parse_mode='Markdown')
            elif text_number == 373:
                markup = types.InlineKeyboardMarkup(row_width=2)
                if creature.endurance > 6:
                    item1 = [types.InlineKeyboardButton(m1, callback_data='4 rounds')]
                    markup.add(*item1)
                    await bot.send_message(user_id,
                                           f"Player damages the creature! Player endurance: {character.endurance}, Creature endurance: {creature.endurance - 6}",
                                           reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                else:
                    mastery = select_one_value(user_id, 'e_mastery_373', 'user_id')
                    if creature.endurance == 6 and mastery == 7:
                        update_one_value(user_id, 'e_mastery_373', 6)
                        item1 = [types.InlineKeyboardButton(m1, callback_data='fight')]
                        markup.add(*item1)
                        await bot.send_message(user_id,
                                               f"Першого аркадіанця переможено! Player endurance: {character.endurance}, Creature endurance: 0. Переходьте до бою з другим аркадіанцем.",
                                               reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                    elif creature.endurance < 6 and mastery == 7:
                        update_one_value(user_id, 'e_endurance_373', 6)
                        update_one_value(user_id, 'e_mastery_373', 6)
                        item1 = [types.InlineKeyboardButton(m1, callback_data='fight')]
                        markup.add(*item1)
                        await bot.send_message(user_id,
                                               f"Першого аркадіанця переможено! Player endurance: {character.endurance}, Creature endurance: 0. Переходьте до бою з другим аркадіанцем.",
                                               reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                    elif creature.endurance < 6 and mastery == 6:
                        item1 = [types.InlineKeyboardButton(m1, callback_data='fight')]
                        markup.add(*item1)
                        await bot.send_message(user_id,
                                               f"Player damages the creature! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                               reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі


        elif creature.endurance <= 0:
            markup = types.InlineKeyboardMarkup()
            if text_number == 2:
                item1 = [types.InlineKeyboardButton('Go on', callback_data='263' if text_number == 2 else '119')]
                markup.add(*item1)
                win_message = 'Ви перемогли його за чотири раунди.' if text_number == 2 else 'The player wins!'
                await bot.send_message(user_id, win_message, reply_markup=markup, parse_mode='Markdown')
            elif text_number == 3:
                item1 = [types.InlineKeyboardButton('Go on', callback_data='119')]
                markup.add(*item1)
                await bot.send_message(user_id, 'The player wins!', reply_markup=markup, parse_mode='Markdown')
            elif text_number == 4:
                item1 = [types.InlineKeyboardButton('Go on', callback_data='71')]
                markup.add(*item1)
                await bot.send_message(user_id, 'The player wins!', reply_markup=markup, parse_mode='Markdown')
            elif text_number == 17:
                item1 = [types.InlineKeyboardButton('291', callback_data='291')]
                if counter >= 2:
                    item1 = [types.InlineKeyboardButton('328', callback_data='328')]
                markup.add(*item1)
                await bot.send_message(user_id, 'The player wins!', reply_markup=markup, parse_mode='Markdown')
            elif text_number == 24:
                enemy1_endurance = select_one_value(user_id, f'e_endurance_{text_number}_1', 'user_id')
                enemy2_endurance = select_one_value(user_id, f'e_endurance_{text_number}_2', 'user_id')
                if flag24 == 1:  # перший аркадіанець загинув
                    item1 = [types.InlineKeyboardButton("381", callback_data='381')]
                    if enemy2_endurance > 0:
                        item1 = [types.InlineKeyboardButton("Битися з другим аркадіанцем", callback_data='second_a')]
                    markup.add(*item1)
                    if player_attack < other_creature_attack:
                        await bot.send_message(user_id, 'The player wins, but another creature damages the player!',
                                               reply_markup=markup, parse_mode='Markdown')
                    else:
                        await bot.send_message(user_id, 'The player wins!', reply_markup=markup, parse_mode='Markdown')
                    update_one_value(user_id, f'flag{text_number}', 2)
                elif flag24 == 2:  # другий аркадіанець загинув
                    item1 = [types.InlineKeyboardButton("381", callback_data='381')]
                    if enemy1_endurance > 0:
                        item1 = [types.InlineKeyboardButton("Битися з першим аркадіанцем", callback_data='first_a')]
                    markup.add(*item1)
                    if player_attack < other_creature_attack:
                        await bot.send_message(user_id, 'The player wins, but another creature damages the player!',
                                               reply_markup=markup, parse_mode='Markdown')
                    else:
                        await bot.send_message(user_id, 'The player wins!', reply_markup=markup,
                                               parse_mode='Markdown')
                    update_one_value(user_id, f'flag{text_number}', 1)
                else:  # enemy1_endurance <= 0 and enemy2_endurance <= 0:
                    item1 = [types.InlineKeyboardButton('381', callback_data='381')]
                    markup.add(*item1)
                    await bot.send_message(user_id, 'The player wins!', reply_markup=markup, parse_mode='Markdown')
            elif text_number == 113:
                enemy1_endurance = select_one_value(user_id, f'e_endurance_{text_number}_1', 'user_id')
                enemy2_endurance = select_one_value(user_id, f'e_endurance_{text_number}_2', 'user_id')
                if flag113 == 1:  # перший аркадіанець загинув
                    item1 = [types.InlineKeyboardButton("9", callback_data='9')]
                    if enemy2_endurance > 0:
                        item1 = [types.InlineKeyboardButton("Битися з Індусом", callback_data='indus')]
                    markup.add(*item1)
                    if player_attack < other_creature_attack:
                        await bot.send_message(user_id, 'The player wins, but another creature damages the player!',
                                               reply_markup=markup, parse_mode='Markdown')
                    else:
                        await bot.send_message(user_id, 'The player wins!', reply_markup=markup, parse_mode='Markdown')
                    update_one_value(user_id, 'flag113', 2)
                elif flag113 == 2:  # другий аркадіанець загинув
                    item1 = [types.InlineKeyboardButton("9", callback_data='9')]
                    if enemy1_endurance > 0:
                        item1 = [types.InlineKeyboardButton("Битися з Грусом", callback_data='grus')]
                    markup.add(*item1)
                    if player_attack < other_creature_attack:
                        await bot.send_message(user_id, 'The player wins, but another creature damages the player!',
                                               reply_markup=markup, parse_mode='Markdown')
                    else:
                        await bot.send_message(user_id, 'The player wins!', reply_markup=markup,
                                               parse_mode='Markdown')
                    update_one_value(user_id, f'flag{text_number}', 1)
                else:  # enemy1_endurance <= 0 and enemy2_endurance <= 0:
                    item1 = [types.InlineKeyboardButton('9', callback_data='9')]
                    markup.add(*item1)
                    await bot.send_message(user_id, 'The player wins!', reply_markup=markup, parse_mode='Markdown')
            elif text_number == 35:
                item1 = [types.InlineKeyboardButton('272', callback_data='272')]
                markup.add(*item1)
                await bot.send_message(user_id, 'The player wins!', reply_markup=markup, parse_mode='Markdown')
            elif text_number == 55:
                item1 = [types.InlineKeyboardButton('251', callback_data='251')]
                markup.add(*item1)
                await bot.send_message(user_id, 'The player wins!', reply_markup=markup, parse_mode='Markdown')
            elif text_number == 82:
                item1 = [types.InlineKeyboardButton('261', callback_data='261')]
                markup.add(*item1)
                await bot.send_message(user_id, 'The player wins!', reply_markup=markup, parse_mode='Markdown')
            elif text_number == 84:
                item1 = [types.InlineKeyboardButton('Продовжити', callback_data='112')]
                markup.add(*item1)
                await bot.send_message(user_id,
                                       'The player wins! Під час бою перекинувся ящик і впав на блок кондиціювання повітря, який спочатку заіскрив, а потім спалахнув. Коли бій закінчено, вогонь уже палає на повну силу.',
                                       reply_markup=markup, parse_mode='Markdown')
            elif text_number == 104:
                item1 = [types.InlineKeyboardButton('315', callback_data='315')]
                markup.add(*item1)
                await bot.send_message(user_id, 'The player wins!', reply_markup=markup, parse_mode='Markdown')
            elif text_number == 106:
                item1 = [types.InlineKeyboardButton('54', callback_data='54')]
                markup.add(*item1)
                await bot.send_message(user_id, 'The player wins!', reply_markup=markup, parse_mode='Markdown')
            elif text_number == 107:
                endurance_last = select_one_value(user_id, 'Endurance', 'user_id')
                if endurance_last > 0:
                    if dogfight_107 == 1:
                        change_1_data(user_id, 'Mastery', 'user_id', 1, multiplier=-1)
                    item1 = [types.InlineKeyboardButton('Перевірити Удачу', callback_data='check_luck_107')]
                    markup.add(*item1)
                    await bot.send_message(user_id, 'The player wins!', reply_markup=markup, parse_mode='Markdown')
            elif text_number == 124:
                change_1_data(user_id, 'Mastery', 'user_id', 1)
                endurance_last = select_one_value(user_id, 'Endurance', 'user_id')
                if endurance_last > 0:
                    item1 = [types.InlineKeyboardButton('151', callback_data='151')]
                    markup.add(*item1)
                    await bot.send_message(user_id, 'The player wins!', reply_markup=markup, parse_mode='Markdown')
            elif text_number == 133:
                item1 = [types.InlineKeyboardButton('54', callback_data='54')]
                markup.add(*item1)
                await bot.send_message(user_id, 'The player wins!', reply_markup=markup, parse_mode='Markdown')
            elif text_number == 136:
                item1 = [types.InlineKeyboardButton('268', callback_data='268')]
                markup.add(*item1)
                await bot.send_message(user_id, 'The player wins!', reply_markup=markup, parse_mode='Markdown')
            elif text_number == 150:
                item1 = [types.InlineKeyboardButton('66', callback_data='66')]
                markup.add(*item1)
                await bot.send_message(user_id, 'The player wins!', reply_markup=markup, parse_mode='Markdown')
            elif text_number == 157:
                item1 = [types.InlineKeyboardButton('Обшукати тіло', callback_data='12'),
                         types.InlineKeyboardButton('Піти', callback_data='124')]
                markup.add(*item1)
                await bot.send_message(user_id, 'The player wins!', reply_markup=markup, parse_mode='Markdown')
            elif text_number == 165:
                change_1_data(user_id, 'Mastery', 'user_id', 1)
                item1 = [types.InlineKeyboardButton('336', callback_data='336')]
                markup.add(*item1)
                await bot.send_message(user_id, 'The player wins!', reply_markup=markup, parse_mode='Markdown')
            elif text_number == 172:
                enemy1_endurance = select_one_value(user_id, f'e_endurance_{text_number}_1', 'user_id')
                enemy2_endurance = select_one_value(user_id, f'e_endurance_{text_number}_2', 'user_id')
                if flag172 == 1:  # перший аркадіанець загинув
                    item1 = [types.InlineKeyboardButton("268", callback_data='268')]
                    if enemy2_endurance > 0:
                        item1 = [types.InlineKeyboardButton("Битися з другим стражником", callback_data='second_g')]
                    markup.add(*item1)
                    if player_attack < other_creature_attack:
                        await bot.send_message(user_id, 'The player wins, but another creature damages the player!',
                                               reply_markup=markup, parse_mode='Markdown')
                    else:
                        await bot.send_message(user_id, 'The player wins!', reply_markup=markup, parse_mode='Markdown')
                    update_one_value(user_id, 'flag172', 2)
                elif flag24 == 2:  # другий аркадіанець загинув
                    item1 = [types.InlineKeyboardButton("268", callback_data='268')]
                    if enemy1_endurance > 0:
                        item1 = [types.InlineKeyboardButton("Битися з першим стражником", callback_data='first_g')]
                    markup.add(*item1)
                    if player_attack < other_creature_attack:
                        await bot.send_message(user_id, 'The player wins, but another creature damages the player!',
                                               reply_markup=markup, parse_mode='Markdown')
                    else:
                        await bot.send_message(user_id, 'The player wins!', reply_markup=markup,
                                               parse_mode='Markdown')
                    update_one_value(user_id, 'flag172', 1)
                else:  # enemy1_endurance <= 0 and enemy2_endurance <= 0:
                    item1 = [types.InlineKeyboardButton('268', callback_data='268')]
                    markup.add(*item1)
                    await bot.send_message(user_id, 'The player wins!', reply_markup=markup, parse_mode='Markdown')
            elif text_number == 206:
                update_one_value(user_id, 'sword', 1)
                item1 = [types.InlineKeyboardButton('131', callback_data='131')]
                markup.add(*item1)
                await bot.send_message(user_id, 'Ви перемогли і берете собі його меч.', reply_markup=markup,
                                       parse_mode='Markdown')
            elif text_number == 215:
                item1 = [types.InlineKeyboardButton('Взяти гранату', callback_data='take_grenade_215'),
                         types.InlineKeyboardButton('Не треба граната', callback_data='320')]
                markup.add(*item1)
                await bot.send_message(user_id, 'Ви виграєте! Можете взяти гранату.', reply_markup=markup,
                                       parse_mode='Markdown')
            elif text_number == 224:
                item1 = [types.InlineKeyboardButton('Взяти меч', callback_data='take_sword_224'),
                         types.InlineKeyboardButton('Не треба меч', callback_data='336')]
                markup.add(*item1)
                await bot.send_message(user_id, 'Ви виграєте! Можете взяти меч. Ви повинні негайно залишити космопорт.',
                                       reply_markup=markup, parse_mode='Markdown')
            elif text_number == 234:
                enemy1_endurance = select_one_value(user_id, f'e_endurance_{text_number}_1', 'user_id')
                enemy2_endurance = select_one_value(user_id, f'e_endurance_{text_number}_2', 'user_id')
                if flag234 == 1:  # перший аркадіанець загинув
                    item1 = [types.InlineKeyboardButton("381", callback_data='381')]
                    if enemy2_endurance > 0:
                        item1 = [types.InlineKeyboardButton("Битися з другим аркадіанцем", callback_data='second_a_2')]
                    markup.add(*item1)
                    if player_attack < other_creature_attack:
                        await bot.send_message(user_id, 'The player wins!',
                                               reply_markup=markup, parse_mode='Markdown')
                    else:
                        await bot.send_message(user_id, 'The player wins!', reply_markup=markup, parse_mode='Markdown')
                    update_one_value(user_id, 'flag234', 2)
                elif flag234 == 2:  # другий аркадіанець загинув
                    item1 = [types.InlineKeyboardButton("381", callback_data='381')]
                    if enemy1_endurance > 0:
                        item1 = [types.InlineKeyboardButton("Битися з жителем півночі", callback_data='first_a_n')]
                    markup.add(*item1)
                    if player_attack < other_creature_attack:
                        await bot.send_message(user_id, 'The player wins!',
                                               reply_markup=markup, parse_mode='Markdown')
                    else:
                        await bot.send_message(user_id, 'The player wins!', reply_markup=markup,
                                               parse_mode='Markdown')
                    update_one_value(user_id, 'flag234', 1)
                else:  # enemy1_endurance <= 0 and enemy2_endurance <= 0:
                    item1 = [types.InlineKeyboardButton('381', callback_data='381')]
                    markup.add(*item1)
                    await bot.send_message(user_id, 'The player wins!', reply_markup=markup, parse_mode='Markdown')
            elif text_number == 243:
                item1 = [types.InlineKeyboardButton('189', callback_data='189')]
                markup.add(*item1)
                await bot.send_message(user_id, 'The player wins!', reply_markup=markup, parse_mode='Markdown')
            elif text_number == 244:
                if character.endurance > 4:
                    enemy1_endurance = select_one_value(user_id, f'e_endurance_{text_number}_1', 'user_id')
                    enemy2_endurance = select_one_value(user_id, f'e_endurance_{text_number}_2', 'user_id')
                    if flag244 == 1:  # перший аркадіанець загинув
                        item1 = [types.InlineKeyboardButton("337", callback_data='337')]
                        if enemy2_endurance > 0:
                            item1 = [types.InlineKeyboardButton("Другий громила", callback_data="second_h")]
                        markup.add(*item1)
                        if player_attack < other_creature_attack:
                            await bot.send_message(user_id, 'The player wins, but another creature damages the player!',
                                                   reply_markup=markup, parse_mode='Markdown')
                        else:
                            await bot.send_message(user_id, 'The player wins!', reply_markup=markup,
                                                   parse_mode='Markdown')
                        update_one_value(user_id, 'flag244', 2)
                    elif flag244 == 2:  # другий аркадіанець загинув
                        item1 = [types.InlineKeyboardButton("337", callback_data='337')]
                        if enemy1_endurance > 0:
                            item1 = [types.InlineKeyboardButton("Перший громила", callback_data="first_h")]
                        markup.add(*item1)
                        if player_attack < other_creature_attack:
                            await bot.send_message(user_id, 'The player wins, but another creature damages the player!',
                                                   reply_markup=markup, parse_mode='Markdown')
                        else:
                            await bot.send_message(user_id, 'The player wins!', reply_markup=markup,
                                                   parse_mode='Markdown')
                        update_one_value(user_id, f'flag{text_number}', 1)
                    else:  # enemy1_endurance <= 0 and enemy2_endurance <= 0:
                        item1 = [types.InlineKeyboardButton('337', callback_data='337')]
                        markup.add(*item1)
                        await bot.send_message(user_id, 'The player wins!', reply_markup=markup, parse_mode='Markdown')
                else:
                    update_one_value(user_id, 'Endurance', 4)
                    item1 = [types.InlineKeyboardButton('Go on', callback_data='337')]
                    markup.add(*item1)
                    await bot.send_message(user_id,
                                           'Бій завершено. Ваша Витривалість становить 4 бали. Ваші супротивники втікають.',
                                           reply_markup=markup, parse_mode='Markdown')

            elif text_number == 289:
                item1 = [types.InlineKeyboardButton('Go on', callback_data='329')]
                markup.add(*item1)
                await bot.send_message(user_id, 'The player wins!', reply_markup=markup, parse_mode='Markdown')

            elif text_number == 295:
                e_endurance_295_1 = select_one_value(user_id, 'e_endurance_295_1', 'user_id')
                e_endurance_295_2 = select_one_value(user_id, 'e_endurance_295_2', 'user_id')
                e_endurance_295_3 = select_one_value(user_id, 'e_endurance_295_3', 'user_id')
                e_endurance_295_4 = select_one_value(user_id, 'e_endurance_295_4', 'user_id')
                item1 = [types.InlineKeyboardButton('До бою!', callback_data='fight')]
                if e_endurance_295_1 > 0:
                    update_one_value(user_id, 'e_endurance_295_1', 0)
                    update_add_enemy(user_id, 7, 8, 'e_mastery_295', 'e_endurance_295')
                    markup.add(*item1)
                    await bot.send_message(user_id,
                                           'Ви перемогли першого аркадіанця! Далі на черзі другий аркадіанець.',
                                           reply_markup=markup, parse_mode='Markdown')
                elif e_endurance_295_2 > 0:
                    update_one_value(user_id, 'e_endurance_295_2', 0)
                    update_add_enemy(user_id, 7, 6, 'e_mastery_295', 'e_endurance_295')
                    markup.add(*item1)
                    await bot.send_message(user_id,
                                           'Ви перемогли другого аркадіанця! Тепер доведеться битися з третім аркадіанцем.',
                                           reply_markup=markup, parse_mode='Markdown')
                elif e_endurance_295_3 > 0:
                    update_one_value(user_id, 'e_endurance_295_3', 0)
                    update_add_enemy(user_id, 6, 6, 'e_mastery_295', 'e_endurance_295')
                    markup.add(*item1)
                    await bot.send_message(user_id,
                                           "Ви перемогли третього аркадіанця! До бою з четвертим аркадіанцем.",
                                           reply_markup=markup, parse_mode='Markdown')
                elif e_endurance_295_4 > 0:
                    markup = types.InlineKeyboardMarkup(row_width=1)
                    update_one_value(user_id, 'e_endurance_295_4', 0)
                    sword = select_one_value(user_id, 'sword', 'user_id')
                    if not sword:
                        change_1_data(user_id, 'Mastery', 'user_id', 1)
                    item1 = [types.InlineKeyboardButton('Повернутися до кабіни відеофонів', callback_data='311'),
                             types.InlineKeyboardButton(
                                 'Покинути клуб, відчуваючи, що вже привернули до себе забагато уваги',
                                 callback_data='252')]
                    markup.add(*item1)
                    await bot.send_message(user_id, 'The player wins!', reply_markup=markup, parse_mode='Markdown')

            elif text_number == 298:
                item1 = [types.InlineKeyboardButton('Go on', callback_data='40')]
                markup.add(*item1)
                await bot.send_message(user_id, 'The player wins!', reply_markup=markup, parse_mode='Markdown')

            elif text_number == 313:
                item1 = [types.InlineKeyboardButton('Go on', callback_data='106')]
                markup.add(*item1)
                await bot.send_message(user_id, 'The player wins!', reply_markup=markup, parse_mode='Markdown')

            elif text_number == 341:
                item1 = [types.InlineKeyboardButton('Go on', callback_data='54')]
                markup.add(*item1)
                await bot.send_message(user_id, 'The player wins!', reply_markup=markup, parse_mode='Markdown')

            elif text_number == 351:
                item1 = [types.InlineKeyboardButton('Go on', callback_data='7')]
                markup.add(*item1)
                await bot.send_message(user_id, 'The player wins!', reply_markup=markup, parse_mode='Markdown')

            elif text_number == 366:
                e_endurance_366_1 = select_one_value(user_id, 'e_endurance_366_1', 'user_id')
                e_endurance_366_2 = select_one_value(user_id, 'e_endurance_366_2', 'user_id')
                e_endurance_366_3 = select_one_value(user_id, 'e_endurance_366_3', 'user_id')
                e_endurance_366_4 = select_one_value(user_id, 'e_endurance_366_4', 'user_id')
                item1 = [types.InlineKeyboardButton('До бою!', callback_data='fight')]
                if e_endurance_366_1 > 0:
                    update_one_value(user_id, 'e_endurance_366_1', 0)
                    update_add_enemy(user_id, 7, 8, 'e_mastery_366', 'e_endurance_366')
                    markup.add(*item1)
                    await bot.send_message(user_id,
                                           'Ви перемогли аркадіанця, жителя півночі! Далі на черзі перший аркадіанець, житель півдня.',
                                           reply_markup=markup, parse_mode='Markdown')
                elif e_endurance_366_2 > 0:
                    update_one_value(user_id, 'e_endurance_366_2', 0)
                    update_add_enemy(user_id, 7, 6, 'e_mastery_366', 'e_endurance_366')
                    markup.add(*item1)
                    await bot.send_message(user_id,
                                           'Ви перемогли першого аркадіанця, жителя півдня! Тепер доведеться битися з другим аркадіанцем, жителем півдня.',
                                           reply_markup=markup, parse_mode='Markdown')
                elif e_endurance_366_3 > 0:
                    update_one_value(user_id, 'e_endurance_366_3', 0)
                    update_add_enemy(user_id, 6, 6, 'e_mastery_366', 'e_endurance_366')
                    markup.add(*item1)
                    await bot.send_message(user_id,
                                           "Ви перемогли другого аркадіанця, жителя півдня! До бою з п'яним аркадіанцем, жителем півдня.",
                                           reply_markup=markup, parse_mode='Markdown')
                elif e_endurance_366_4 > 0:
                    update_one_value(user_id, 'e_endurance_366_4', 0)
                    item1 = [types.InlineKeyboardButton('Go on', callback_data='125')]
                    markup.add(*item1)
                    await bot.send_message(user_id, 'The player wins!', reply_markup=markup, parse_mode='Markdown')


            elif text_number == 367:
                item1 = [types.InlineKeyboardButton('Взяти меч', callback_data='take_sword_367'),
                         types.InlineKeyboardButton('Не треба меч', callback_data='336')]
                markup.add(*item1)
                await bot.send_message(user_id, 'Ви виграєте! Можете взяти меч. Ви повинні негайно залишити космопорт.',
                                       reply_markup=markup, parse_mode='Markdown')

            elif text_number == 373:
                item1 = [types.InlineKeyboardButton('Go on', callback_data='285')]
                markup.add(*item1)
                await bot.send_message(user_id, 'The player wins!', reply_markup=markup, parse_mode='Markdown')

            elif text_number == 375:
                item1 = [types.InlineKeyboardButton('Go on', callback_data='159')]
                markup.add(*item1)
                await bot.send_message(user_id, 'The player wins!', reply_markup=markup, parse_mode='Markdown')

            elif text_number == 391:
                item1 = [types.InlineKeyboardButton('Go on', callback_data='269')]
                markup.add(*item1)
                await bot.send_message(user_id, 'The player wins!', reply_markup=markup, parse_mode='Markdown')



    elif creature_attack > player_attack:
        # Creature damages the player
        # if text_number != 190:
        character.endurance -= 2
        print(character.endurance)
        update_character_endurance(user_id, 'Endurance', character.endurance)

        if text_number == 24:
            enemy1_endurance = select_one_value(user_id, f'e_endurance_{text_number}_1', 'user_id')
            enemy2_endurance = select_one_value(user_id, f'e_endurance_{text_number}_2', 'user_id')
            creature_mastery_column = f'e_mastery_{text_number}_2' if flag113 == 1 else f'e_mastery_{text_number}_1'
            creature_mastery = select_one_value(user_id, creature_mastery_column, 'user_id')
            other_creature_attack = roll_dice_2() + creature_mastery
            if (flag24 == 1 and enemy2_endurance > 0) or (flag24 == 2 and enemy1_endurance > 0):
                if player_attack < other_creature_attack and character.endurance > 0:
                    character.endurance -= 2
            update_character_endurance(user_id, 'Endurance', character.endurance)

        elif text_number == 35:
            CRITICAL_HIT_THRESHOLD = 6
            if random.randint(1, 6) == CRITICAL_HIT_THRESHOLD:
                update_character_endurance(user_id, 'Endurance', 0)
                await bot.send_message(user_id, "Ти програв! Починай спочатку.")  # бот повідомляє про програш

        elif text_number == 113:
            enemy1_endurance = select_one_value(user_id, f'e_endurance_{text_number}_1', 'user_id')
            enemy2_endurance = select_one_value(user_id, f'e_endurance_{text_number}_2', 'user_id')
            creature_mastery_column = f'e_mastery_{text_number}_2' if flag113 == 1 else f'e_mastery_{text_number}_1'
            creature_mastery = select_one_value(user_id, creature_mastery_column, 'user_id')
            other_creature_attack = roll_dice_2() + creature_mastery
            if (flag113 == 1 and enemy2_endurance > 0) or (flag113 == 2 and enemy1_endurance > 0):
                if player_attack < other_creature_attack and character.endurance > 0:
                    character.endurance -= 2
            update_character_endurance(user_id, 'Endurance', character.endurance)

        elif text_number == 124:
            if character.endurance > 0 and random.randint(1, 6) in {5, 6}:
                character.endurance -= 2
                update_character_endurance(user_id, 'Endurance', character.endurance)

        elif text_number == 136:
            if character.endurance > 0 and random.randint(1, 6) in {5, 6}:
                character.endurance -= 2
                update_character_endurance(user_id, 'Endurance', character.endurance)

        elif text_number == 172:
            enemy1_endurance = select_one_value(user_id, f'e_endurance_{text_number}_1', 'user_id')
            enemy2_endurance = select_one_value(user_id, f'e_endurance_{text_number}_2', 'user_id')
            creature_mastery_column = f'e_mastery_{text_number}_2' if flag172 == 1 else f'e_mastery_{text_number}_1'
            creature_mastery = select_one_value(user_id, creature_mastery_column, 'user_id')
            other_creature_attack = roll_dice_2() + creature_mastery
            if (flag172 == 1 and enemy2_endurance > 0) or (flag172 == 2 and enemy1_endurance > 0):
                if player_attack < other_creature_attack and character.endurance > 0:
                    character.endurance -= 2
            update_character_endurance(user_id, 'Endurance', character.endurance)

        elif text_number == 190:
            change_1_data(user_id, 'attack_190', 'user_id', 1)
            successful_attack = select_one_value(user_id, 'attack_190', 'user_id')
            print(successful_attack)
            character.endurance += 2
            # print(character.endurance)
            character.endurance -= successful_attack
            update_character_endurance(user_id, 'Endurance', character.endurance)
            print(character.endurance)

        elif text_number == 224:
            CRITICAL_HIT_THRESHOLD = 6
            if random.randint(1, 6) == CRITICAL_HIT_THRESHOLD:
                update_character_endurance(user_id, 'Endurance', 0)
                await bot.send_message(user_id, "Ти програв! Починай спочатку.")  # бот повідомляє про програш

        elif text_number == 234:
            enemy1_endurance = select_one_value(user_id, f'e_endurance_{text_number}_1', 'user_id')
            enemy2_endurance = select_one_value(user_id, f'e_endurance_{text_number}_2', 'user_id')
            if enemy1_endurance > 0 and character.endurance > 0 and random.randint(1, 6) in {5, 6}:
                character.endurance -= 2
            creature_mastery_column = f'e_mastery_{text_number}_2' if flag234 == 1 else f'e_mastery_{text_number}_1'
            creature_mastery = select_one_value(user_id, creature_mastery_column, 'user_id')
            other_creature_attack = roll_dice_2() + creature_mastery
            if (flag234 == 1 and enemy2_endurance > 0) or (flag234 == 2 and enemy1_endurance > 0):
                if player_attack < other_creature_attack and character.endurance > 0:
                    character.endurance -= 2
            update_character_endurance(user_id, 'Endurance', character.endurance)

        elif text_number == 244 and character.endurance > 4:
            # якщо Витривалість героя більше 4, то так, а якщо менше або дорівнює 4, то описано в наступному блоці
            enemy1_endurance = select_one_value(user_id, f'e_endurance_{text_number}_1', 'user_id')
            enemy2_endurance = select_one_value(user_id, f'e_endurance_{text_number}_2', 'user_id')
            creature_mastery_column = f'e_mastery_{text_number}_2' if flag244 == 1 else f'e_mastery_{text_number}_1'
            creature_mastery = select_one_value(user_id, creature_mastery_column, 'user_id')
            other_creature_attack = roll_dice_2() + creature_mastery
            if (flag244 == 1 and enemy2_endurance > 0) or (flag244 == 2 and enemy1_endurance > 0):
                if player_attack < other_creature_attack and character.endurance > 4:
                    character.endurance -= 2
            update_character_endurance(user_id, 'Endurance', character.endurance)
            # else:
            #     update_one_value(user_id, 'Endurance', 4)
            #     item1 = [types.InlineKeyboardButton('Go on', callback_data='337')]
            #     markup.add(*item1)
            #     await bot.send_message(user_id,
            #                            'Бій завершено. Ваша Витривалість становить 4 бали. Ваші супротивники втікають.',
            #                            reply_markup=markup, parse_mode='Markdown')
        elif text_number == 289:
            if character.endurance > 0 and random.randint(1, 6) in {5, 6}:
                character.endurance -= 2
                update_character_endurance(user_id, 'Endurance', character.endurance)

        elif text_number == 298:
            character.endurance = 0
            update_character_endurance(user_id, 'Endurance', character.endurance)
        counter += 1

        # Check luck for different scenarios
        if character.endurance > 0:
            if character.luck > 0:
                if text_number == 2:
                    markup = types.InlineKeyboardMarkup()
                    item1 = [types.InlineKeyboardButton(m1, callback_data='4 rounds'),
                             types.InlineKeyboardButton(m2, callback_data='way3')]
                    markup.add(*item1)
                    await bot.send_message(user_id,
                                           f"Creature damages the player! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                           reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                elif text_number in [3, 4, 17, 35, 55, 82, 84, 104, 106, 107, 124, 133, 136, 150, 157, 165, 190, 206,
                                     215, 224, 243, 289, 295, 313, 341, 351, 366, 367, 375, 391]:
                    if text_number == 243 and sand243 == 1:
                        if random.randint(1, 6) in {4, 5, 6}:
                            change_1_data(user_id, 'Mastery', 'user_id', 1, multiplier=-1)
                            update_one_value(user_id, 'rounds243', 1)
                        change_1_data(user_id, 'sand243', 'user_id', 1)
                    markup = types.InlineKeyboardMarkup()
                    item1 = [types.InlineKeyboardButton(m1, callback_data='fight'),
                             types.InlineKeyboardButton(m2, callback_data='way3')]
                    markup.add(*item1)
                    await bot.send_message(user_id,
                                           f"Creature damages the player! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                           reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                elif text_number == 24:
                    enemy1_endurance = select_one_value(user_id, f'e_endurance_{text_number}_1', 'user_id')
                    enemy2_endurance = select_one_value(user_id, f'e_endurance_{text_number}_2', 'user_id')
                    if enemy1_endurance > 0 and enemy2_endurance > 0:
                        markup = types.InlineKeyboardMarkup(row_width=1)
                        item1 = [types.InlineKeyboardButton("Битися з першим аркадіанцем", callback_data='first_a'),
                                 types.InlineKeyboardButton("Битися з другим аркадіанцем", callback_data='second_a'),
                                 types.InlineKeyboardButton(m2, callback_data='way3')]
                        markup.add(*item1)
                        if player_attack > other_creature_attack:
                            await bot.send_message(user_id,
                                                   f"Creature damages the player! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                                   reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                        elif player_attack < other_creature_attack:
                            await bot.send_message(user_id,
                                                   f"Creature damages the player! Another creature also damages the player! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                                   reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                    elif enemy1_endurance <= 0 and enemy2_endurance > 0:
                        markup = types.InlineKeyboardMarkup(row_width=1)
                        item1 = [types.InlineKeyboardButton("Битися з другим аркадіанцем", callback_data='second_a'),
                                 types.InlineKeyboardButton(m2, callback_data='way2')]
                        markup.add(*item1)
                        if player_attack > other_creature_attack:
                            await bot.send_message(user_id,
                                                   f"Creature damages the player!  Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                                   reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                        elif player_attack < other_creature_attack:
                            await bot.send_message(user_id,
                                                   f"Creature damages the player! Another creature also damages the player! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                                   reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                    elif enemy1_endurance > 0 and enemy2_endurance <= 0:
                        markup = types.InlineKeyboardMarkup(row_width=1)
                        item1 = [types.InlineKeyboardButton("Битися з першим аркадіанцем", callback_data='first_a'),
                                 types.InlineKeyboardButton(m2, callback_data='way2')]
                        markup.add(*item1)
                        if player_attack > other_creature_attack:
                            await bot.send_message(user_id,
                                                   f"Creature damages the player! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                                   reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                        elif player_attack < other_creature_attack:
                            await bot.send_message(user_id,
                                                   f"Creature damages the player! Another creature also damages the player! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                                   reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                elif text_number == 113:
                    enemy1_endurance = select_one_value(user_id, f'e_endurance_{text_number}_1', 'user_id')
                    enemy2_endurance = select_one_value(user_id, f'e_endurance_{text_number}_2', 'user_id')
                    if enemy1_endurance > 0 and enemy2_endurance > 0:
                        markup = types.InlineKeyboardMarkup(row_width=1)
                        item1 = [types.InlineKeyboardButton("Битися з Грусом", callback_data='grus'),
                                 types.InlineKeyboardButton("Битися з Індусом", callback_data='indus'),
                                 types.InlineKeyboardButton(m2, callback_data='way3')]
                        markup.add(*item1)
                        if player_attack > other_creature_attack:
                            await bot.send_message(user_id,
                                                   f"Creature damages the player! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                                   reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                        elif player_attack < other_creature_attack:
                            await bot.send_message(user_id,
                                                   f"Creature damages the player! Another creature also damages the player! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                                   reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                    elif enemy1_endurance <= 0 and enemy2_endurance > 0:
                        markup = types.InlineKeyboardMarkup(row_width=1)
                        item1 = [types.InlineKeyboardButton("Битися з Індусом", callback_data='indus'),
                                 types.InlineKeyboardButton(m2, callback_data='way2')]
                        markup.add(*item1)
                        if player_attack > other_creature_attack:
                            await bot.send_message(user_id,
                                                   f"Creature damages the player!  Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                                   reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                        elif player_attack < other_creature_attack:
                            await bot.send_message(user_id,
                                                   f"Creature damages the player! Another creature also damages the player! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                                   reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                    elif enemy1_endurance > 0 and enemy2_endurance <= 0:
                        markup = types.InlineKeyboardMarkup(row_width=1)
                        item1 = [types.InlineKeyboardButton("Битися з Грусом", callback_data='grus'),
                                 types.InlineKeyboardButton(m2, callback_data='way2')]
                        markup.add(*item1)
                        if player_attack > other_creature_attack:
                            await bot.send_message(user_id,
                                                   f"Creature damages the player! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                                   reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                        elif player_attack < other_creature_attack:
                            await bot.send_message(user_id,
                                                   f"Creature damages the player! Another creature also damages the player! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                                   reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                elif text_number == 172:
                    enemy1_endurance = select_one_value(user_id, f'e_endurance_{text_number}_1', 'user_id')
                    enemy2_endurance = select_one_value(user_id, f'e_endurance_{text_number}_2', 'user_id')
                    if enemy1_endurance > 0 and enemy2_endurance > 0:
                        markup = types.InlineKeyboardMarkup(row_width=1)
                        item1 = [types.InlineKeyboardButton("Битися з першим стражником", callback_data='first_g'),
                                 types.InlineKeyboardButton("Битися з другим стражником", callback_data='second_g'),
                                 types.InlineKeyboardButton(m2, callback_data='way3')]
                        markup.add(*item1)
                        if player_attack > other_creature_attack:
                            await bot.send_message(user_id,
                                                   f"Creature damages the player! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                                   reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                        elif player_attack < other_creature_attack:
                            await bot.send_message(user_id,
                                                   f"Creature damages the player! Another creature also damages the player! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                                   reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                    elif enemy1_endurance <= 0 and enemy2_endurance > 0:
                        markup = types.InlineKeyboardMarkup(row_width=1)
                        item1 = [types.InlineKeyboardButton("Битися з другим стражником", callback_data='second_g'),
                                 types.InlineKeyboardButton(m2, callback_data='way2')]
                        markup.add(*item1)
                        if player_attack > other_creature_attack:
                            await bot.send_message(user_id,
                                                   f"Creature damages the player!  Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                                   reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                        elif player_attack < other_creature_attack:
                            await bot.send_message(user_id,
                                                   f"Creature damages the player! Another creature also damages the player! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                                   reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                    elif enemy1_endurance > 0 and enemy2_endurance <= 0:
                        markup = types.InlineKeyboardMarkup(row_width=1)
                        item1 = [types.InlineKeyboardButton("Битися з першим стражником", callback_data='first_g'),
                                 types.InlineKeyboardButton(m2, callback_data='way2')]
                        markup.add(*item1)
                        if player_attack > other_creature_attack:
                            await bot.send_message(user_id,
                                                   f"Creature damages the player! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                                   reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                        elif player_attack < other_creature_attack:
                            await bot.send_message(user_id,
                                                   f"Creature damages the player! Another creature also damages the player! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                                   reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                elif text_number == 234:
                    enemy1_endurance = select_one_value(user_id, f'e_endurance_{text_number}_1', 'user_id')
                    enemy2_endurance = select_one_value(user_id, f'e_endurance_{text_number}_2', 'user_id')
                    if enemy1_endurance > 0 and enemy2_endurance > 0:
                        markup = types.InlineKeyboardMarkup(row_width=1)
                        item1 = [types.InlineKeyboardButton("Битися з жителем півночі", callback_data='first_a_n'),
                                 types.InlineKeyboardButton("Битися з другим аркадіанцем", callback_data='second_a_2'),
                                 types.InlineKeyboardButton(m2, callback_data='way3')]
                        markup.add(*item1)
                        if player_attack > other_creature_attack:
                            await bot.send_message(user_id,
                                                   f"Creature damages the player! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                                   reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                        elif player_attack < other_creature_attack:
                            await bot.send_message(user_id,
                                                   f"Creature damages the player! Another creature also damages the player! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                                   reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                    elif enemy1_endurance <= 0 and enemy2_endurance > 0:
                        markup = types.InlineKeyboardMarkup(row_width=1)
                        item1 = [types.InlineKeyboardButton("Битися з другим аркадіанцем", callback_data='second_a_2'),
                                 types.InlineKeyboardButton(m2, callback_data='way2')]
                        markup.add(*item1)
                        if player_attack > other_creature_attack:
                            await bot.send_message(user_id,
                                                   f"Creature damages the player!  Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                                   reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                        elif player_attack < other_creature_attack:
                            await bot.send_message(user_id,
                                                   f"Creature damages the player! Another creature also damages the player! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                                   reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                    elif enemy1_endurance > 0 and enemy2_endurance <= 0:
                        markup = types.InlineKeyboardMarkup(row_width=1)
                        item1 = [types.InlineKeyboardButton("Битися з жителем півночі", callback_data='first_a_n'),
                                 types.InlineKeyboardButton(m2, callback_data='way2')]
                        markup.add(*item1)
                        if player_attack > other_creature_attack:
                            await bot.send_message(user_id,
                                                   f"Creature damages the player! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                                   reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                        elif player_attack < other_creature_attack:
                            await bot.send_message(user_id,
                                                   f"Creature damages the player! Another creature also damages the player! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                                   reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі

                elif text_number == 244:
                    if character.endurance > 4:
                        enemy1_endurance = select_one_value(user_id, f'e_endurance_{text_number}_1', 'user_id')
                        enemy2_endurance = select_one_value(user_id, f'e_endurance_{text_number}_2', 'user_id')
                        if enemy1_endurance > 0 and enemy2_endurance > 0:
                            markup = types.InlineKeyboardMarkup(row_width=1)
                            item1 = [types.InlineKeyboardButton("Перший громила", callback_data="first_h"),
                                     types.InlineKeyboardButton("Другий громила", callback_data="second_h"),
                                     types.InlineKeyboardButton(m2, callback_data='way3')]
                            markup.add(*item1)
                            if player_attack > other_creature_attack:
                                await bot.send_message(user_id,
                                                       f"Creature damages the player! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                                       reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                            elif player_attack < other_creature_attack:
                                await bot.send_message(user_id,
                                                       f"Creature damages the player! Another creature also damages the player! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                                       reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                        elif enemy1_endurance <= 0 and enemy2_endurance > 0:
                            markup = types.InlineKeyboardMarkup(row_width=1)
                            item1 = [types.InlineKeyboardButton("Другий громила", callback_data="second_h"),
                                     types.InlineKeyboardButton(m2, callback_data='way2')]
                            markup.add(*item1)
                            if player_attack > other_creature_attack:
                                await bot.send_message(user_id,
                                                       f"Creature damages the player!  Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                                       reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                            elif player_attack < other_creature_attack:
                                await bot.send_message(user_id,
                                                       f"Creature damages the player! Another creature also damages the player! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                                       reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                        elif enemy1_endurance > 0 and enemy2_endurance <= 0:
                            markup = types.InlineKeyboardMarkup(row_width=1)
                            item1 = [types.InlineKeyboardButton("Перший громила", callback_data="first_h"),
                                     types.InlineKeyboardButton(m2, callback_data='way2')]
                            markup.add(*item1)
                            if player_attack > other_creature_attack:
                                await bot.send_message(user_id,
                                                       f"Creature damages the player! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                                       reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                            elif player_attack < other_creature_attack:
                                await bot.send_message(user_id,
                                                       f"Creature damages the player! Another creature also damages the player! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                                       reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                    else:
                        update_one_value(user_id, 'Endurance', 4)
                        item1 = [types.InlineKeyboardButton('Go on', callback_data='337')]
                        markup.add(*item1)
                        await bot.send_message(user_id,
                                               'Бій завершено. Ваша Витривалість становить 4 бали. Ваші супротивники втікають.',
                                               reply_markup=markup, parse_mode='Markdown')
                elif text_number == 373:
                    markup = types.InlineKeyboardMarkup(row_width=2)
                    item1 = [types.InlineKeyboardButton(m1, callback_data='fight'),
                             types.InlineKeyboardButton(m2, callback_data='way3')]
                    markup.add(*item1)
                    if creature.endurance > 6:
                        await bot.send_message(user_id,
                                               f"Creature damages the player! Player endurance: {character.endurance}, Creature endurance: {creature.endurance - 6}",
                                               reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                    else:
                        await bot.send_message(user_id,
                                               f"Creature damages the player! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                               reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі


            else:
                markup = types.InlineKeyboardMarkup()
                if text_number == 2:
                    item1 = [types.InlineKeyboardButton(m1, callback_data='4 rounds')]
                    markup.add(*item1)
                    await bot.send_message(user_id,
                                           f"Creature damages the player! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                           reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                elif text_number in [3, 4, 17, 35, 55, 82, 84, 104, 106, 107, 124, 133, 136, 150, 157, 165, 190, 206,
                                     215, 224, 243, 289, 295, 313, 341, 351, 366, 367, 375, 391]:
                    item1 = [types.InlineKeyboardButton(m1, callback_data='fight')]
                    markup.add(*item1)
                    await bot.send_message(user_id,
                                           f"Creature damages the player! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                           reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                elif text_number == 24:
                    enemy1_endurance = select_one_value(user_id, f'e_endurance_{text_number}_1', 'user_id')
                    enemy2_endurance = select_one_value(user_id, f'e_endurance_{text_number}_2', 'user_id')
                    if enemy1_endurance > 0 and enemy2_endurance > 0:
                        markup = types.InlineKeyboardMarkup(row_width=1)
                        item1 = [types.InlineKeyboardButton("Битися з першим аркадіанцем", callback_data='first_a'),
                                 types.InlineKeyboardButton("Битися з другим аркадіанцем", callback_data='second_a'),
                                 types.InlineKeyboardButton(m2, callback_data='way3')]
                        markup.add(*item1)
                        if player_attack > other_creature_attack:
                            await bot.send_message(user_id,
                                                   f"Creature damages the player! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                                   reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                        elif player_attack < other_creature_attack:
                            await bot.send_message(user_id,
                                                   f"Creature damages the player! Another creature also damages the player! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                                   reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                    elif enemy1_endurance <= 0 and enemy2_endurance > 0:
                        markup = types.InlineKeyboardMarkup(row_width=1)
                        item1 = [types.InlineKeyboardButton("Битися з другим аркадіанцем", callback_data='second_a'),
                                 types.InlineKeyboardButton(m2, callback_data='way3')]
                        markup.add(*item1)
                        if player_attack > other_creature_attack:
                            await bot.send_message(user_id,
                                                   f"Creature damages the player! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                                   reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                        elif player_attack < other_creature_attack:
                            await bot.send_message(user_id,
                                                   f"Creature damages the player! Another creature also damages the player! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                                   reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                    elif enemy1_endurance > 0 and enemy2_endurance <= 0:
                        markup = types.InlineKeyboardMarkup(row_width=1)
                        item1 = [types.InlineKeyboardButton("Битися з першим аркадіанцем", callback_data='first_a'),
                                 types.InlineKeyboardButton(m2, callback_data='way3')]
                        markup.add(*item1)
                        if player_attack > other_creature_attack:
                            await bot.send_message(user_id,
                                                   f"Creature damages the player! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                                   reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                        elif player_attack < other_creature_attack:
                            await bot.send_message(user_id,
                                                   f"Creature damages the player! Another creature also damages the player! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                                   reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                elif text_number == 113:
                    enemy1_endurance = select_one_value(user_id, f'e_endurance_{text_number}_1', 'user_id')
                    enemy2_endurance = select_one_value(user_id, f'e_endurance_{text_number}_2', 'user_id')
                    if enemy1_endurance > 0 and enemy2_endurance > 0:
                        markup = types.InlineKeyboardMarkup(row_width=1)
                        item1 = [types.InlineKeyboardButton("Битися з Грусом", callback_data='grus'),
                                 types.InlineKeyboardButton("Битися з Індусом", callback_data='indus'),
                                 types.InlineKeyboardButton(m2, callback_data='way3')]
                        markup.add(*item1)
                        if player_attack > other_creature_attack:
                            await bot.send_message(user_id,
                                                   f"Creature damages the player! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                                   reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                        elif player_attack < other_creature_attack:
                            await bot.send_message(user_id,
                                                   f"Creature damages the player! Another creature also damages the player! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                                   reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                    elif enemy1_endurance <= 0 and enemy2_endurance > 0:
                        markup = types.InlineKeyboardMarkup(row_width=1)
                        item1 = [types.InlineKeyboardButton("Битися з Індусом", callback_data='indus'),
                                 types.InlineKeyboardButton(m2, callback_data='way3')]
                        markup.add(*item1)
                        if player_attack > other_creature_attack:
                            await bot.send_message(user_id,
                                                   f"Creature damages the player! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                                   reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                        elif player_attack < other_creature_attack:
                            await bot.send_message(user_id,
                                                   f"Creature damages the player! Another creature also damages the player! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                                   reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                    elif enemy1_endurance > 0 and enemy2_endurance <= 0:
                        markup = types.InlineKeyboardMarkup(row_width=1)
                        item1 = [types.InlineKeyboardButton("Битися з Грусом", callback_data='grus'),
                                 types.InlineKeyboardButton(m2, callback_data='way3')]
                        markup.add(*item1)
                        if player_attack > other_creature_attack:
                            await bot.send_message(user_id,
                                                   f"Creature damages the player! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                                   reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                        elif player_attack < other_creature_attack:
                            await bot.send_message(user_id,
                                                   f"Creature damages the player! Another creature also damages the player! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                                   reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                elif text_number == 172:
                    enemy1_endurance = select_one_value(user_id, f'e_endurance_{text_number}_1', 'user_id')
                    enemy2_endurance = select_one_value(user_id, f'e_endurance_{text_number}_2', 'user_id')
                    if enemy1_endurance > 0 and enemy2_endurance > 0:
                        markup = types.InlineKeyboardMarkup(row_width=1)
                        item1 = [types.InlineKeyboardButton("Битися з першим стражником", callback_data='first_g'),
                                 types.InlineKeyboardButton("Битися з другим стражником", callback_data='second_g'),
                                 types.InlineKeyboardButton(m2, callback_data='way3')]
                        markup.add(*item1)
                        if player_attack > other_creature_attack:
                            await bot.send_message(user_id,
                                                   f"Creature damages the player! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                                   reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                        elif player_attack < other_creature_attack:
                            await bot.send_message(user_id,
                                                   f"Creature damages the player! Another creature also damages the player! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                                   reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                    elif enemy1_endurance <= 0 and enemy2_endurance > 0:
                        markup = types.InlineKeyboardMarkup(row_width=1)
                        item1 = [types.InlineKeyboardButton("Битися з другим стражником", callback_data='second_g'),
                                 types.InlineKeyboardButton(m2, callback_data='way3')]
                        markup.add(*item1)
                        if player_attack > other_creature_attack:
                            await bot.send_message(user_id,
                                                   f"Creature damages the player! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                                   reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                        elif player_attack < other_creature_attack:
                            await bot.send_message(user_id,
                                                   f"Creature damages the player! Another creature also damages the player! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                                   reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                    elif enemy1_endurance > 0 and enemy2_endurance <= 0:
                        markup = types.InlineKeyboardMarkup(row_width=1)
                        item1 = [types.InlineKeyboardButton("Битися з першим стражником", callback_data='first_g'),
                                 types.InlineKeyboardButton(m2, callback_data='way3')]
                        markup.add(*item1)
                        if player_attack > other_creature_attack:
                            await bot.send_message(user_id,
                                                   f"Creature damages the player! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                                   reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                        elif player_attack < other_creature_attack:
                            await bot.send_message(user_id,
                                                   f"Creature damages the player! Another creature also damages the player! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                                   reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                elif text_number == 234:
                    enemy1_endurance = select_one_value(user_id, f'e_endurance_{text_number}_1', 'user_id')
                    enemy2_endurance = select_one_value(user_id, f'e_endurance_{text_number}_2', 'user_id')
                    if enemy1_endurance > 0 and enemy2_endurance > 0:
                        markup = types.InlineKeyboardMarkup(row_width=1)
                        item1 = [types.InlineKeyboardButton("Битися з жителем півночі", callback_data='first_a_n'),
                                 types.InlineKeyboardButton("Битися з другим аркадіанцем", callback_data='second_a_2'),
                                 types.InlineKeyboardButton(m2, callback_data='way3')]
                        markup.add(*item1)
                        if player_attack > other_creature_attack:
                            await bot.send_message(user_id,
                                                   f"Creature damages the player! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                                   reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                        elif player_attack < other_creature_attack:
                            await bot.send_message(user_id,
                                                   f"Creature damages the player! Another creature also damages the player! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                                   reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                    elif enemy1_endurance <= 0 and enemy2_endurance > 0:
                        markup = types.InlineKeyboardMarkup(row_width=1)
                        item1 = [types.InlineKeyboardButton("Битися з другим аркадіанцем", callback_data='second_a_2'),
                                 types.InlineKeyboardButton(m2, callback_data='way3')]
                        markup.add(*item1)
                        if player_attack > other_creature_attack:
                            await bot.send_message(user_id,
                                                   f"Creature damages the player! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                                   reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                        elif player_attack < other_creature_attack:
                            await bot.send_message(user_id,
                                                   f"Creature damages the player! Another creature also damages the player! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                                   reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                    elif enemy1_endurance > 0 and enemy2_endurance <= 0:
                        markup = types.InlineKeyboardMarkup(row_width=1)
                        item1 = [types.InlineKeyboardButton("Битися з жителем півночі", callback_data='first_a_n'),
                                 types.InlineKeyboardButton(m2, callback_data='way3')]
                        markup.add(*item1)
                        if player_attack > other_creature_attack:
                            await bot.send_message(user_id,
                                                   f"Creature damages the player! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                                   reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                        elif player_attack < other_creature_attack:
                            await bot.send_message(user_id,
                                                   f"Creature damages the player! Another creature also damages the player! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                                   reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі

                elif text_number == 244:
                    if character.endurance > 4:
                        enemy1_endurance = select_one_value(user_id, f'e_endurance_{text_number}_1', 'user_id')
                        enemy2_endurance = select_one_value(user_id, f'e_endurance_{text_number}_2', 'user_id')
                        if enemy1_endurance > 0 and enemy2_endurance > 0:
                            markup = types.InlineKeyboardMarkup(row_width=1)
                            item1 = [types.InlineKeyboardButton("Перший громила", callback_data="first_h"),
                                     types.InlineKeyboardButton("Другий громила", callback_data="second_h"),
                                     types.InlineKeyboardButton(m2, callback_data='way3')]
                            markup.add(*item1)
                            if player_attack > other_creature_attack:
                                await bot.send_message(user_id,
                                                       f"Creature damages the player! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                                       reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                            elif player_attack < other_creature_attack:
                                await bot.send_message(user_id,
                                                       f"Creature damages the player! Another creature also damages the player! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                                       reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                        elif enemy1_endurance <= 0 and enemy2_endurance > 0:
                            markup = types.InlineKeyboardMarkup(row_width=1)
                            item1 = [types.InlineKeyboardButton("Другий громила", callback_data="second_h"),
                                     types.InlineKeyboardButton(m2, callback_data='way3')]
                            markup.add(*item1)
                            if player_attack > other_creature_attack:
                                await bot.send_message(user_id,
                                                       f"Creature damages the player! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                                       reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                            elif player_attack < other_creature_attack:
                                await bot.send_message(user_id,
                                                       f"Creature damages the player! Another creature also damages the player! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                                       reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                        elif enemy1_endurance > 0 and enemy2_endurance <= 0:
                            markup = types.InlineKeyboardMarkup(row_width=1)
                            item1 = [types.InlineKeyboardButton("Перший громила", callback_data="first_h"),
                                     types.InlineKeyboardButton(m2, callback_data='way3')]
                            markup.add(*item1)
                            if player_attack > other_creature_attack:
                                await bot.send_message(user_id,
                                                       f"Creature damages the player! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                                       reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                            elif player_attack < other_creature_attack:
                                await bot.send_message(user_id,
                                                       f"Creature damages the player! Another creature also damages the player! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                                       reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                elif text_number == 373:
                    markup = types.InlineKeyboardMarkup(row_width=2)
                    item1 = [types.InlineKeyboardButton(m1, callback_data='fight')]
                    markup.add(*item1)
                    await bot.send_message(user_id,
                                           f"Creature damages the player! Player endurance: {character.endurance}, Creature endurance: {creature.endurance - 6}",
                                           reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі

        else:
            if text_number == 298:
                character.endurance = 0
                update_character_endurance(user_id, 'Endurance', character.endurance)
                await bot.send_message(user_id,
                                       "Ви пропустили удар, це означає, що птах врізався у вас і всією своєю вагою зіштовхнув з уступу.")  # бот повідомляє про програш
            else:
                await bot.send_message(user_id, "Ти програв! Починай спочатку.")  # бот повідомляє про програш
    else:
        # Both parry, start a new round
        markup = types.InlineKeyboardMarkup()
        item1 = [types.InlineKeyboardButton(m1, callback_data='4 rounds')]
        if text_number in [3, 4, 17, 35, 55, 82, 84, 104, 106, 107, 124, 133, 136, 150, 157, 165, 190, 206, 215, 224,
                           243, 289, 295, 298, 313, 341, 351, 366, 367, 373, 375, 391]:
            item1 = [types.InlineKeyboardButton(m1, callback_data='fight')]
        elif text_number == 24:
            enemy1_endurance = select_one_value(user_id, f'e_endurance_{text_number}_1', 'user_id')
            enemy2_endurance = select_one_value(user_id, f'e_endurance_{text_number}_2', 'user_id')
            if enemy1_endurance > 0 and enemy2_endurance > 0:
                item1 = [types.InlineKeyboardButton("Битися з першим аркадіанцем", callback_data='first_a'),
                         types.InlineKeyboardButton("Битися з другим аркадіанцем", callback_data='second_a')]
            elif enemy1_endurance >= 0 and enemy2_endurance > 0:
                item1 = [types.InlineKeyboardButton("Битися з другим аркадіанцем", callback_data='second_a')]
            elif enemy1_endurance > 0 and enemy2_endurance <= 0:
                item1 = [types.InlineKeyboardButton("Битися з першим аркадіанцем", callback_data='first_a')]

        elif text_number == 113:
            enemy1_endurance = select_one_value(user_id, f'e_endurance_{text_number}_1', 'user_id')
            enemy2_endurance = select_one_value(user_id, f'e_endurance_{text_number}_2', 'user_id')
            if enemy1_endurance > 0 and enemy2_endurance > 0:
                item1 = [types.InlineKeyboardButton("Битися з Грусом", callback_data='grus'),
                         types.InlineKeyboardButton("Битися з Індусом", callback_data='indus')]
            elif enemy1_endurance <= 0 and enemy2_endurance > 0:
                item1 = [types.InlineKeyboardButton("Битися з Індусом", callback_data='indus')]
            elif enemy1_endurance > 0 and enemy2_endurance <= 0:
                item1 = [types.InlineKeyboardButton("Битися з Грусом", callback_data='grus')]

        elif text_number == 172:
            enemy1_endurance = select_one_value(user_id, f'e_endurance_{text_number}_1', 'user_id')
            enemy2_endurance = select_one_value(user_id, f'e_endurance_{text_number}_2', 'user_id')
            if enemy1_endurance > 0 and enemy2_endurance > 0:
                item1 = [types.InlineKeyboardButton("Битися з першим стражником", callback_data='first_g'),
                         types.InlineKeyboardButton("Битися з другим стражником", callback_data='second_g')]
            elif enemy1_endurance >= 0 and enemy2_endurance > 0:
                item1 = [types.InlineKeyboardButton("Битися з другим стражником", callback_data='second_g')]
            elif enemy1_endurance > 0 and enemy2_endurance <= 0:
                item1 = [types.InlineKeyboardButton("Битися з першим стражником", callback_data='first_g')]
        elif text_number == 234:
            enemy1_endurance = select_one_value(user_id, f'e_endurance_{text_number}_1', 'user_id')
            enemy2_endurance = select_one_value(user_id, f'e_endurance_{text_number}_2', 'user_id')
            if enemy1_endurance > 0 and enemy2_endurance > 0:
                item1 = [types.InlineKeyboardButton("Битися з жителем півночі", callback_data='first_a_n'),
                         types.InlineKeyboardButton("Битися з другим аркадіанцем", callback_data='second_a_2')]
            elif enemy1_endurance >= 0 and enemy2_endurance > 0:
                item1 = [types.InlineKeyboardButton("Битися з другим аркадіанцем", callback_data='second_a_2')]
            elif enemy1_endurance > 0 and enemy2_endurance <= 0:
                item1 = [types.InlineKeyboardButton("Битися з жителем півночі", callback_data='first_a_n')]
        elif text_number == 244:
            enemy1_endurance = select_one_value(user_id, f'e_endurance_{text_number}_1', 'user_id')
            enemy2_endurance = select_one_value(user_id, f'e_endurance_{text_number}_2', 'user_id')
            if enemy1_endurance > 0 and enemy2_endurance > 0:
                item1 = [types.InlineKeyboardButton("Перший громила", callback_data="first_h"),
                         types.InlineKeyboardButton("Другий громила", callback_data="second_h")]
            elif enemy1_endurance <= 0 and enemy2_endurance > 0:
                item1 = [types.InlineKeyboardButton("Другий громила", callback_data="second_h")]
            elif enemy1_endurance > 0 and enemy2_endurance <= 0:
                item1 = [types.InlineKeyboardButton("Перший громила", callback_data="first_h")]

        markup.add(*item1)
        await bot.send_message(user_id, "Both parry, starting a new round.",
                               reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі


@dp.callback_query_handler(lambda c: c.data == 'way2')
async def process_callback_way2(callback_query: types.CallbackQuery):
    global counter
    user_id = callback_query.from_user.id
    print("way2")
    m1 = 'Наступний удар'
    text_number = select_one_value(callback_query.from_user.id, 'text_number', 'user_id')
    flag24 = select_one_value(callback_query.from_user.id, 'flag24', 'user_id')
    flag113 = select_one_value(callback_query.from_user.id, 'flag113', 'user_id')
    flag172 = select_one_value(callback_query.from_user.id, 'flag172', 'user_id')
    flag234 = select_one_value(callback_query.from_user.id, 'flag234', 'user_id')
    flag244 = select_one_value(callback_query.from_user.id, 'flag244', 'user_id')
    character_data = retrieve_character_data(callback_query.from_user.id)
    creature_data = None
    if text_number in [2, 3, 4, 17, 35, 55, 82, 84, 104, 106, 107, 124, 133, 136, 150, 157, 161, 165, 190, 206, 215,
                       224, 243, 289, 295, 298, 313, 341, 351, 366, 367, 373, 375, 391]:
        text_to_creature_data_mapping = {
            2: ('e_mastery_2', 'e_endurance_2'),
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
        creature_data = retrieve_creature_data(callback_query.from_user.id,
                                               *text_to_creature_data_mapping.get(text_number, ('', '')))

    elif text_number == 24 and flag24 in {1, 2}:
        columns_mapping = {
            1: (f'e_mastery_{text_number}_1', f'e_endurance_{text_number}_1'),
            2: (f'e_mastery_{text_number}_2', f'e_endurance_{text_number}_2'),
        }
        creature_data = retrieve_creature_data(callback_query.from_user.id, *columns_mapping[flag24])

    elif text_number == 113 and flag113 in {1, 2}:
        columns_mapping = {
            1: (f'e_mastery_{text_number}_1', f'e_endurance_{text_number}_1'),
            2: (f'e_mastery_{text_number}_2', f'e_endurance_{text_number}_2'),
        }
        creature_data = retrieve_creature_data(callback_query.from_user.id, *columns_mapping[flag113])

    elif text_number == 172 and flag172 in {1, 2}:
        columns_mapping = {
            1: (f'e_mastery_{text_number}_1', f'e_endurance_{text_number}_1'),
            2: (f'e_mastery_{text_number}_2', f'e_endurance_{text_number}_2'),
        }
        creature_data = retrieve_creature_data(callback_query.from_user.id, *columns_mapping[flag172])

    elif text_number == 234 and flag234 in {1, 2}:
        columns_mapping = {
            1: (f'e_mastery_{text_number}_1', f'e_endurance_{text_number}_1'),
            2: (f'e_mastery_{text_number}_2', f'e_endurance_{text_number}_2'),
        }
        creature_data = retrieve_creature_data(callback_query.from_user.id, *columns_mapping[flag234])

    elif text_number == 244 and flag244 in {1, 2}:
        columns_mapping = {
            1: (f'e_mastery_{text_number}_1', f'e_endurance_{text_number}_1'),
            2: (f'e_mastery_{text_number}_2', f'e_endurance_{text_number}_2'),
        }
        creature_data = retrieve_creature_data(callback_query.from_user.id, *columns_mapping[flag244])

    # if creature_data is not None:
    character = Character(mastery=character_data[0], endurance=character_data[1], luck=character_data[2])
    creature = Character(mastery=creature_data[0], endurance=creature_data[1], luck=creature_data[2])
    if character.luck > 0:  # якщо пощастило
        result = roll_dice_2()
        if result <= character.luck:
            creature.endurance -= 2
            if text_number in [2, 3, 4, 17, 35, 55, 82, 84, 104, 106, 107, 124, 133, 150, 157, 161, 165, 190, 206, 215,
                               224, 243, 289, 295, 298, 313, 341, 351, 366, 367, 373, 375, 391]:
                creature_endurance_mapping = {
                    2: 'e_endurance_2',
                    3: 'e_endurance_3',
                    4: 'e_endurance_4',
                    17: 'e_endurance_17',
                    35: 'e_endurance_35',
                    55: 'e_endurance_55',
                    82: 'e_endurance_82',
                    84: 'e_endurance_84',
                    104: 'e_endurance_104',
                    106: 'e_endurance_106',
                    107: 'e_endurance_107',
                    124: 'e_endurance_124',
                    133: 'e_endurance_133',
                    136: 'e_endurance_136',
                    150: 'e_endurance_150',
                    157: 'e_endurance_157',
                    161: 'e_endurance_161',
                    165: 'e_endurance_165',
                    190: 'e_endurance_190',
                    206: 'e_endurance_206',
                    215: 'e_endurance_215',
                    224: 'e_endurance_224',
                    243: 'e_endurance_243',
                    289: 'e_endurance_289',
                    295: 'e_endurance_295',
                    298: 'e_endurance_298',
                    313: 'e_endurance_313',
                    341: 'e_endurance_341',
                    351: 'e_endurance_351',
                    366: 'e_endurance_366',
                    367: 'e_endurance_367',
                    373: 'e_endurance_373',
                    375: 'e_endurance_375',
                    391: 'e_endurance_391',
                }
                update_character_endurance(callback_query.from_user.id, creature_endurance_mapping.get(text_number, ''),
                                           creature.endurance)
            elif text_number == 24 and flag24 in {1, 2}:
                column_name = f'e_endurance_{text_number}_{flag24}'
                update_character_endurance(callback_query.from_user.id, column_name, creature.endurance)

            elif text_number == 113 and flag113 in {1, 2}:
                column_name = f'e_endurance_{text_number}_{flag113}'
                update_character_endurance(callback_query.from_user.id, column_name, creature.endurance)

            elif text_number == 172 and flag172 in {1, 2}:
                column_name = f'e_endurance_{text_number}_{flag172}'
                update_character_endurance(callback_query.from_user.id, column_name, creature.endurance)

            elif text_number == 234 and flag234 in {1, 2}:
                column_name = f'e_endurance_{text_number}_{flag234}'
                update_character_endurance(callback_query.from_user.id, column_name, creature.endurance)

            elif text_number == 244 and flag244 in {1, 2}:
                column_name = f'e_endurance_{text_number}_{flag244}'
                update_character_endurance(callback_query.from_user.id, column_name, creature.endurance)

            if creature.endurance > 0:
                markup = types.InlineKeyboardMarkup(row_width=1)
                item1 = [types.InlineKeyboardButton(m1, callback_data='4 rounds')]
                if text_number in [3, 4, 17, 35, 55, 82, 84, 104, 106, 107, 124, 133, 136, 150, 157, 165, 190, 206, 215,
                                   224, 243, 289, 295, 298, 313, 341, 351, 366, 367, 375, 391]:
                    item1 = [types.InlineKeyboardButton(m1, callback_data='fight')]
                elif text_number == 24:
                    item1 = [types.InlineKeyboardButton("Битися з першим аркадіанцем", callback_data='first_a'),
                             types.InlineKeyboardButton("Битися з другим аркадіанцем", callback_data='second_a')]
                elif text_number == 113:
                    item1 = [types.InlineKeyboardButton("Битися з Грусом", callback_data='grus'),
                             types.InlineKeyboardButton("Битися з Індусом", callback_data='indus')]
                elif text_number == 172:
                    item1 = [types.InlineKeyboardButton("Битися з першим стражником", callback_data='first_g'),
                             types.InlineKeyboardButton("Битися з другим стражником", callback_data='second_g')]
                elif text_number == 234:
                    item1 = [types.InlineKeyboardButton("Битися з жителем півночі", callback_data='first_a_n'),
                             types.InlineKeyboardButton("Битися з другим аркадіанцем", callback_data='second_a_2')]
                elif text_number == 244:
                    item1 = [types.InlineKeyboardButton("Перший громила", callback_data="first_h"),
                             types.InlineKeyboardButton("Другий громила", callback_data="second_h")]
                markup.add(*item1)
                await bot.send_message(callback_query.from_user.id,
                                       f"You are lucky! Player damages the creature! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                       reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                if text_number == 373:
                    markup = types.InlineKeyboardMarkup(row_width=2)
                    if creature.endurance > 6:
                        item1 = [types.InlineKeyboardButton(m1, callback_data='4 rounds')]
                        markup.add(*item1)
                        await bot.send_message(user_id,
                                               f"Player damages the creature! Player endurance: {character.endurance}, Creature endurance: {creature.endurance - 6}",
                                               reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                    else:
                        mastery = select_one_value(user_id, 'e_mastery_373', 'user_id')
                        if creature.endurance == 6 and mastery == 7:
                            update_one_value(user_id, 'e_mastery_373', 6)
                            item1 = [types.InlineKeyboardButton(m1, callback_data='fight')]
                            markup.add(*item1)
                            await bot.send_message(user_id,
                                                   f"Першого аркадіанця переможено! Player endurance: {character.endurance}, Creature endurance: 0. Переходьте до бою з другим аркадіанцем.",
                                                   reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                        elif creature.endurance < 6 and mastery == 7:
                            update_one_value(user_id, 'e_endurance_373', 6)
                            update_one_value(user_id, 'e_mastery_373', 6)
                            item1 = [types.InlineKeyboardButton(m1, callback_data='fight')]
                            markup.add(*item1)
                            await bot.send_message(user_id,
                                                   f"Першого аркадіанця переможено! Player endurance: {character.endurance}, Creature endurance: 0. Переходьте до бою з другим аркадіанцем.",
                                                   reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                        elif creature.endurance < 6 and mastery == 6:
                            item1 = [types.InlineKeyboardButton(m1, callback_data='fight')]
                            markup.add(*item1)
                            await bot.send_message(user_id,
                                                   f"Player damages the creature! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                                   reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі

            else:
                markup = types.InlineKeyboardMarkup()
                if text_number == 2:
                    item1 = [types.InlineKeyboardButton('Go on', callback_data='263')]
                    markup.add(*item1)
                    await bot.send_message(callback_query.from_user.id, 'Ви перемогли його за чотири раунди.',
                                           reply_markup=markup, parse_mode='Markdown')
                elif text_number == 3:
                    item1 = [types.InlineKeyboardButton('Go on', callback_data='119')]
                    markup.add(*item1)
                    await bot.send_message(callback_query.from_user.id, 'The player wins!', reply_markup=markup,
                                           parse_mode='Markdown')
                elif text_number == 4:
                    item1 = [types.InlineKeyboardButton('Go on', callback_data='71')]
                    markup.add(*item1)
                    await bot.send_message(callback_query.from_user.id, 'The player wins!', reply_markup=markup,
                                           parse_mode='Markdown')
                elif text_number == 17:
                    item1 = [types.InlineKeyboardButton('Go on', callback_data='291')]
                    if counter >= 2:
                        item1 = [types.InlineKeyboardButton('Go on', callback_data='328')]
                    markup.add(*item1)
                    await bot.send_message(user_id, 'The player wins!', reply_markup=markup, parse_mode='Markdown')
                elif text_number == 24:
                    enemy1_endurance = select_one_value(user_id, f'e_endurance_{text_number}_1', 'user_id')
                    enemy2_endurance = select_one_value(user_id, f'e_endurance_{text_number}_2', 'user_id')
                    markup = types.InlineKeyboardMarkup(row_width=1)
                    if enemy1_endurance <= 0 and enemy2_endurance > 0:
                        item1 = [types.InlineKeyboardButton("Битися з другим аркадіанцем", callback_data='second_a')]
                        markup.add(*item1)
                        await bot.send_message(callback_query.from_user.id,
                                               f"Player damages the creature! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                               reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі

                    elif enemy1_endurance > 0 and enemy2_endurance <= 0:
                        item1 = [types.InlineKeyboardButton("Битися з першим аркадіанцем", callback_data='first_a')]
                        markup.add(*item1)
                        await bot.send_message(callback_query.from_user.id,
                                               f"Player damages the creature! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                               reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                    elif enemy1_endurance <= 0 and enemy2_endurance <= 0:
                        item1 = [types.InlineKeyboardButton("381", callback_data='381')]
                        markup.add(*item1)
                        await bot.send_message(user_id, 'The player wins!', reply_markup=markup, parse_mode='Markdown')
                elif text_number == 113:
                    enemy1_endurance = select_one_value(user_id, f'e_endurance_{text_number}_1', 'user_id')
                    enemy2_endurance = select_one_value(user_id, f'e_endurance_{text_number}_2', 'user_id')
                    markup = types.InlineKeyboardMarkup(row_width=1)
                    if enemy1_endurance <= 0 and enemy2_endurance > 0:
                        item1 = [types.InlineKeyboardButton("Битися з Індусом", callback_data='indus')]
                        markup.add(*item1)
                        await bot.send_message(callback_query.from_user.id,
                                               f"Player damages the creature! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                               reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі

                    elif enemy1_endurance > 0 and enemy2_endurance <= 0:
                        item1 = [types.InlineKeyboardButton("Битися з Грусом", callback_data='grus')]
                        markup.add(*item1)
                        await bot.send_message(callback_query.from_user.id,
                                               f"Player damages the creature! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                               reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                    elif enemy1_endurance <= 0 and enemy2_endurance <= 0:
                        item1 = [types.InlineKeyboardButton("9", callback_data='9')]
                        markup.add(*item1)
                        await bot.send_message(user_id, 'The player wins!', reply_markup=markup, parse_mode='Markdown')
                elif text_number == 35:
                    item1 = [types.InlineKeyboardButton('272', callback_data='272')]
                    markup.add(*item1)
                    await bot.send_message(user_id, 'The player wins!', reply_markup=markup, parse_mode='Markdown')
                elif text_number == 55:
                    item1 = [types.InlineKeyboardButton('251', callback_data='251')]
                    markup.add(*item1)
                    await bot.send_message(user_id, 'The player wins!', reply_markup=markup, parse_mode='Markdown')
                elif text_number == 82:
                    item1 = [types.InlineKeyboardButton('261', callback_data='261')]
                    markup.add(*item1)
                    await bot.send_message(user_id, 'The player wins!', reply_markup=markup, parse_mode='Markdown')
                elif text_number == 84:
                    item1 = [types.InlineKeyboardButton('Продовжити', callback_data='112')]
                    markup.add(*item1)
                    await bot.send_message(user_id,
                                           'The player wins! Під час бою перекинувся ящик і впав на блок кондиціювання повітря, який спочатку заіскрив, а потім спалахнув. Коли бій закінчено, вогонь уже палає на повну силу.',
                                           reply_markup=markup, parse_mode='Markdown')
                elif text_number == 104:
                    item1 = [types.InlineKeyboardButton('315', callback_data='315')]
                    markup.add(*item1)
                    await bot.send_message(user_id, 'The player wins!', reply_markup=markup, parse_mode='Markdown')
                elif text_number == 106:
                    item1 = [types.InlineKeyboardButton('54', callback_data='54')]
                    markup.add(*item1)
                    await bot.send_message(user_id, 'The player wins!', reply_markup=markup, parse_mode='Markdown')
                elif text_number == 107:
                    dogfight_107 = select_one_value(user_id, 'dogfight_107', 'user_id')
                    if dogfight_107 == 1:
                        change_1_data(user_id, 'Mastery', 'user_id', 1, multiplier=-1)
                    item1 = [types.InlineKeyboardButton('Перевірити Удачу', callback_data='check_luck_107')]
                    markup.add(*item1)
                    await bot.send_message(user_id, 'The player wins!', reply_markup=markup, parse_mode='Markdown')
                elif text_number == 124:
                    change_1_data(user_id, 'Mastery', 'user_id', 1)
                    item1 = [types.InlineKeyboardButton('151', callback_data='151')]
                    markup.add(*item1)
                    await bot.send_message(user_id, 'The player wins!', reply_markup=markup, parse_mode='Markdown')
                elif text_number == 133:
                    item1 = [types.InlineKeyboardButton('54', callback_data='54')]
                    markup.add(*item1)
                    await bot.send_message(user_id, 'The player wins!', reply_markup=markup, parse_mode='Markdown')
                elif text_number == 136:
                    item1 = [types.InlineKeyboardButton('268', callback_data='268')]
                    markup.add(*item1)
                    await bot.send_message(user_id, 'The player wins!', reply_markup=markup, parse_mode='Markdown')
                elif text_number == 150:
                    item1 = [types.InlineKeyboardButton('66', callback_data='66')]
                    markup.add(*item1)
                    await bot.send_message(user_id, 'The player wins!', reply_markup=markup, parse_mode='Markdown')
                elif text_number == 157:
                    item1 = [types.InlineKeyboardButton('Обшукати тіло', callback_data='12'),
                             types.InlineKeyboardButton('Піти', callback_data='124')]
                    markup.add(*item1)
                    await bot.send_message(user_id, 'The player wins!', reply_markup=markup, parse_mode='Markdown')
                elif text_number == 161:
                    item1 = [types.InlineKeyboardButton('135', callback_data='135')]
                    markup.add(*item1)
                    await bot.send_message(user_id, 'The player wins!', reply_markup=markup, parse_mode='Markdown')
                elif text_number == 165:
                    change_1_data(user_id, 'Mastery', 'user_id', 1)
                    item1 = [types.InlineKeyboardButton('336', callback_data='336')]
                    markup.add(*item1)
                    await bot.send_message(user_id, 'The player wins!', reply_markup=markup, parse_mode='Markdown')
                elif text_number == 172:
                    enemy1_endurance = select_one_value(user_id, f'e_endurance_{text_number}_1', 'user_id')
                    enemy2_endurance = select_one_value(user_id, f'e_endurance_{text_number}_2', 'user_id')
                    markup = types.InlineKeyboardMarkup(row_width=1)
                    if enemy1_endurance <= 0 and enemy2_endurance > 0:
                        item1 = [types.InlineKeyboardButton("Битися з другим стражником", callback_data='second_g')]
                        markup.add(*item1)
                        await bot.send_message(callback_query.from_user.id,
                                               f"Player damages the creature! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                               reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі

                    elif enemy1_endurance > 0 and enemy2_endurance <= 0:
                        item1 = [types.InlineKeyboardButton("Битися з першим стражником", callback_data='first_g')]
                        markup.add(*item1)
                        await bot.send_message(callback_query.from_user.id,
                                               f"Player damages the creature! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                               reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                    elif enemy1_endurance <= 0 and enemy2_endurance <= 0:
                        item1 = [types.InlineKeyboardButton("268", callback_data='268')]
                        markup.add(*item1)
                        await bot.send_message(user_id, 'The player wins!', reply_markup=markup, parse_mode='Markdown')
                elif text_number == 190:
                    change_1_data(user_id, 'Mastery', 'user_id', 1)
                    item1 = [types.InlineKeyboardButton('309', callback_data='309')]
                    markup.add(*item1)
                    await bot.send_message(user_id, 'The player wins!', reply_markup=markup, parse_mode='Markdown')
                elif text_number == 206:
                    update_one_value(user_id, 'sword', 1)
                    item1 = [types.InlineKeyboardButton('131', callback_data='131')]
                    markup.add(*item1)
                    await bot.send_message(user_id, 'Ви перемогли і берете собі його меч.', reply_markup=markup,
                                           parse_mode='Markdown')
                elif text_number == 215:
                    item1 = [types.InlineKeyboardButton('Взяти гранату', callback_data='take_grenade_215'),
                             types.InlineKeyboardButton('Не треба граната', callback_data='320')]
                    markup.add(*item1)
                    await bot.send_message(user_id, 'Ви виграєте! Можете взяти гранату.', reply_markup=markup,
                                           parse_mode='Markdown')
                elif text_number == 224:
                    item1 = [types.InlineKeyboardButton('Взяти меч', callback_data='take_sword_224'),
                             types.InlineKeyboardButton('Не треба меч', callback_data='336')]
                    markup.add(*item1)
                    await bot.send_message(user_id,
                                           'Ви виграєте! Можете взяти меч. Ви повинні негайно залишити космопорт.',
                                           reply_markup=markup, parse_mode='Markdown')
                elif text_number == 234:
                    enemy1_endurance = select_one_value(user_id, f'e_endurance_{text_number}_1', 'user_id')
                    enemy2_endurance = select_one_value(user_id, f'e_endurance_{text_number}_2', 'user_id')
                    markup = types.InlineKeyboardMarkup(row_width=1)
                    if enemy1_endurance <= 0 and enemy2_endurance > 0:
                        item1 = [types.InlineKeyboardButton("Битися з другим аркадіанцем", callback_data='second_a_2')]
                        markup.add(*item1)
                        await bot.send_message(user_id,
                                               f"Player damages the creature! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                               reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі

                    elif enemy1_endurance > 0 and enemy2_endurance <= 0:
                        item1 = [types.InlineKeyboardButton("Битися з жителем півночі", callback_data='first_a_n')]
                        markup.add(*item1)
                        await bot.send_message(user_id,
                                               f"Player damages the creature! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                               reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                    elif enemy1_endurance <= 0 and enemy2_endurance <= 0:
                        item1 = [types.InlineKeyboardButton("381", callback_data='381')]
                        markup.add(*item1)
                        await bot.send_message(user_id, 'The player wins!', reply_markup=markup, parse_mode='Markdown')
                elif text_number == 243:
                    item1 = [types.InlineKeyboardButton('189', callback_data='189')]
                    markup.add(*item1)
                    await bot.send_message(user_id, 'The player wins!', reply_markup=markup, parse_mode='Markdown')
                elif text_number == 244:
                    enemy1_endurance = select_one_value(user_id, f'e_endurance_{text_number}_1', 'user_id')
                    enemy2_endurance = select_one_value(user_id, f'e_endurance_{text_number}_2', 'user_id')
                    markup = types.InlineKeyboardMarkup(row_width=1)
                    if enemy1_endurance <= 0 and enemy2_endurance > 0:
                        item1 = [types.InlineKeyboardButton("Другий громила", callback_data="second_h")]
                        markup.add(*item1)
                        await bot.send_message(callback_query.from_user.id,
                                               f"Player damages the creature! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                               reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі

                    elif enemy1_endurance > 0 and enemy2_endurance <= 0:
                        item1 = [types.InlineKeyboardButton("Перший громила", callback_data="first_h")]
                        markup.add(*item1)
                        await bot.send_message(callback_query.from_user.id,
                                               f"Player damages the creature! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                               reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
                    elif enemy1_endurance <= 0 and enemy2_endurance <= 0:
                        item1 = [types.InlineKeyboardButton("337", callback_data='337')]
                        markup.add(*item1)
                        await bot.send_message(user_id, 'The player wins!', reply_markup=markup, parse_mode='Markdown')
                elif text_number == 289:
                    item1 = [types.InlineKeyboardButton('329', callback_data='329')]
                    markup.add(*item1)
                    await bot.send_message(user_id, 'The player wins!', reply_markup=markup, parse_mode='Markdown')

                elif text_number == 295:
                    e_endurance_295_1 = select_one_value(user_id, 'e_endurance_295_1', 'user_id')
                    e_endurance_295_2 = select_one_value(user_id, 'e_endurance_295_2', 'user_id')
                    e_endurance_295_3 = select_one_value(user_id, 'e_endurance_295_3', 'user_id')
                    e_endurance_295_4 = select_one_value(user_id, 'e_endurance_295_4', 'user_id')
                    item1 = [types.InlineKeyboardButton('До бою!', callback_data='fight')]
                    if e_endurance_295_1 > 0:
                        update_one_value(user_id, 'e_endurance_295_1', 0)
                        update_add_enemy(user_id, 7, 8, 'e_mastery_295', 'e_endurance_295')
                        markup.add(*item1)
                        await bot.send_message(user_id,
                                               'Ви перемогли першого аркадіанця! Далі на черзі другий аркадіанець.',
                                               reply_markup=markup, parse_mode='Markdown')
                    elif e_endurance_295_2 > 0:
                        update_one_value(user_id, 'e_endurance_295_2', 0)
                        update_add_enemy(user_id, 7, 6, 'e_mastery_295', 'e_endurance_295')
                        markup.add(*item1)
                        await bot.send_message(user_id,
                                               'Ви перемогли другого аркадіанця! Тепер доведеться битися з третім аркадіанцем.',
                                               reply_markup=markup, parse_mode='Markdown')
                    elif e_endurance_295_3 > 0:
                        update_one_value(user_id, 'e_endurance_295_3', 0)
                        update_add_enemy(user_id, 6, 6, 'e_mastery_295', 'e_endurance_295')
                        markup.add(*item1)
                        await bot.send_message(user_id,
                                               "Ви перемогли третього аркадіанця! До бою з четвертим аркадіанцем.",
                                               reply_markup=markup, parse_mode='Markdown')
                    elif e_endurance_295_4 > 0:
                        markup = types.InlineKeyboardMarkup(row_width=1)
                        update_one_value(user_id, 'e_endurance_295_4', 0)
                        sword = select_one_value(user_id, 'sword', 'user_id')
                        if not sword:
                            change_1_data(user_id, 'Mastery', 'user_id', 1)
                        item1 = [types.InlineKeyboardButton('Повернутися до кабіни відеофонів', callback_data='311'),
                                 types.InlineKeyboardButton(
                                     'Покинути клуб, відчуваючи, що вже привернули до себе забагато уваги',
                                     callback_data='252')]
                        markup.add(*item1)
                        await bot.send_message(user_id, 'The player wins!', reply_markup=markup, parse_mode='Markdown')

                elif text_number == 298:
                    item1 = [types.InlineKeyboardButton('40', callback_data='40')]
                    markup.add(*item1)
                    await bot.send_message(user_id, 'The player wins!', reply_markup=markup, parse_mode='Markdown')
                elif text_number == 313:
                    item1 = [types.InlineKeyboardButton('106', callback_data='106')]
                    markup.add(*item1)
                    await bot.send_message(user_id, 'The player wins!', reply_markup=markup, parse_mode='Markdown')
                elif text_number == 341:
                    item1 = [types.InlineKeyboardButton('54', callback_data='54')]
                    markup.add(*item1)
                    await bot.send_message(user_id, 'The player wins!', reply_markup=markup, parse_mode='Markdown')
                elif text_number == 351:
                    item1 = [types.InlineKeyboardButton('7', callback_data='7')]
                    markup.add(*item1)
                    await bot.send_message(user_id, 'The player wins!', reply_markup=markup, parse_mode='Markdown')

                elif text_number == 366:
                    e_endurance_366_1 = select_one_value(user_id, 'e_endurance_366_1', 'user_id')
                    e_endurance_366_2 = select_one_value(user_id, 'e_endurance_366_2', 'user_id')
                    e_endurance_366_3 = select_one_value(user_id, 'e_endurance_366_3', 'user_id')
                    e_endurance_366_4 = select_one_value(user_id, 'e_endurance_366_4', 'user_id')
                    item1 = [types.InlineKeyboardButton('До бою!', callback_data='fight')]
                    if e_endurance_366_1 > 0:
                        update_one_value(user_id, 'e_endurance_366_1', 0)
                        update_add_enemy(user_id, 7, 8, 'e_mastery_366', 'e_endurance_366')
                        markup.add(*item1)
                        await bot.send_message(user_id,
                                               'Ви перемогли аркадіанця, жителя півночі! Далі на черзі перший аркадіанець, житель півдня.',
                                               reply_markup=markup, parse_mode='Markdown')
                    elif e_endurance_366_2 > 0:
                        update_one_value(user_id, 'e_endurance_366_2', 0)
                        update_add_enemy(user_id, 7, 6, 'e_mastery_366', 'e_endurance_366')
                        markup.add(*item1)
                        await bot.send_message(user_id,
                                               'Ви перемогли першого аркадіанця, жителя півдня! Тепер доведеться битися з другим аркадіанцем, жителем півдня.',
                                               reply_markup=markup, parse_mode='Markdown')
                    elif e_endurance_366_3 > 0:
                        update_one_value(user_id, 'e_endurance_366_3', 0)
                        update_add_enemy(user_id, 6, 6, 'e_mastery_366', 'e_endurance_366')
                        markup.add(*item1)
                        await bot.send_message(user_id,
                                               "Ви перемогли другого аркадіанця, жителя півдня! До бою з п'яним аркадіанцем, жителем півдня.",
                                               reply_markup=markup, parse_mode='Markdown')
                    elif e_endurance_366_4 > 0:
                        update_one_value(user_id, 'e_endurance_366_4', 0)
                        item1 = [types.InlineKeyboardButton('Go on', callback_data='125')]
                        markup.add(*item1)
                        await bot.send_message(user_id, 'The player wins!', reply_markup=markup,
                                               parse_mode='Markdown')


                elif text_number == 367:
                    item1 = [types.InlineKeyboardButton('Взяти меч', callback_data='take_sword_367'),
                             types.InlineKeyboardButton('Не треба меч', callback_data='336')]
                    markup.add(*item1)
                    await bot.send_message(user_id,
                                           'Ви виграєте! Можете взяти меч. Ви повинні негайно залишити космопорт.',
                                           reply_markup=markup, parse_mode='Markdown')
                elif text_number == 373:
                    item1 = [types.InlineKeyboardButton('285', callback_data='285')]
                    markup.add(*item1)
                    await bot.send_message(user_id, 'The player wins!', reply_markup=markup, parse_mode='Markdown')

                elif text_number == 375:
                    item1 = [types.InlineKeyboardButton('159', callback_data='159')]
                    markup.add(*item1)
                    await bot.send_message(user_id, 'The player wins!', reply_markup=markup, parse_mode='Markdown')

                elif text_number == 391:
                    item1 = [types.InlineKeyboardButton('269', callback_data='269')]
                    markup.add(*item1)
                    await bot.send_message(user_id, 'The player wins!', reply_markup=markup, parse_mode='Markdown')
        else:
            creature.endurance += 1
            if text_number in [2, 3, 4, 17, 35, 55, 82, 84, 104, 106, 107, 124, 133, 136, 150, 157, 161, 165, 190, 206,
                               215, 224, 243, 289, 295, 298, 313, 341, 351, 366, 367, 373, 375, 391]:
                creature_endurance_mapping = {
                    2: 'e_endurance_2',
                    3: 'e_endurance_3',
                    4: 'e_endurance_4',
                    17: 'e_endurance_17',
                    35: 'e_endurance_35',
                    55: 'e_endurance_55',
                    82: 'e_endurance_82',
                    84: 'e_endurance_84',
                    104: 'e_endurance_104',
                    106: 'e_endurance_106',
                    107: 'e_endurance_107',
                    124: 'e_endurance_124',
                    133: 'e_endurance_133',
                    136: 'e_endurance_136',
                    150: 'e_endurance_150',
                    157: 'e_endurance_157',
                    161: 'e_endurance_161',
                    165: 'e_endurance_165',
                    190: 'e_endurance_190',
                    206: 'e_endurance_206',
                    215: 'e_endurance_215',
                    224: 'e_endurance_224',
                    243: 'e_endurance_243',
                    289: 'e_endurance_289',
                    295: 'e_endurance_295',
                    313: 'e_endurance_313',
                    341: 'e_endurance_341',
                    351: 'e_endurance_351',
                    366: 'e_endurance_366',
                    367: 'e_endurance_367',
                    373: 'e_endurance_373',
                    375: 'e_endurance_375',
                    391: 'e_endurance_391',
                }
                update_character_endurance(callback_query.from_user.id, creature_endurance_mapping.get(text_number, ''),
                                           creature.endurance)

            elif text_number == 24 and flag24 in {1, 2}:
                column_name = f'e_endurance_{text_number}_{flag24}'
                update_character_endurance(callback_query.from_user.id, column_name, creature.endurance)
            elif text_number == 113 and flag113 in {1, 2}:
                column_name = f'e_endurance_{text_number}_{flag113}'
                update_character_endurance(callback_query.from_user.id, column_name, creature.endurance)
            elif text_number == 172 and flag172 in {1, 2}:
                column_name = f'e_endurance_{text_number}_{flag172}'
                update_character_endurance(callback_query.from_user.id, column_name, creature.endurance)
            elif text_number == 234 and flag234 in {1, 2}:
                column_name = f'e_endurance_{text_number}_{flag234}'
                update_character_endurance(callback_query.from_user.id, column_name, creature.endurance)
            elif text_number == 244 and flag244 in {1, 2}:
                column_name = f'e_endurance_{text_number}_{flag244}'
                update_character_endurance(callback_query.from_user.id, column_name, creature.endurance)

            markup = types.InlineKeyboardMarkup(row_width=1)
            item1 = [types.InlineKeyboardButton(m1, callback_data='4 rounds')]
            if text_number == 24:
                enemy1_endurance = select_one_value(user_id, f'e_endurance_{text_number}_1', 'user_id')
                enemy2_endurance = select_one_value(user_id, f'e_endurance_{text_number}_2', 'user_id')
                if enemy1_endurance > 0 and enemy2_endurance > 0:
                    item1 = [types.InlineKeyboardButton("Битися з першим аркадіанцем", callback_data='first_a'),
                             types.InlineKeyboardButton("Битися з другим аркадіанцем", callback_data='second_a')]
                elif enemy1_endurance <= 0 and enemy2_endurance > 0:
                    item1 = [types.InlineKeyboardButton("Битися з другим аркадіанцем", callback_data='second_a')]
                elif enemy1_endurance > 0 and enemy2_endurance <= 0:
                    item1 = [types.InlineKeyboardButton("Битися з першим аркадіанцем", callback_data='first_a')]

            elif text_number == 113:
                enemy1_endurance = select_one_value(user_id, f'e_endurance_{text_number}_1', 'user_id')
                enemy2_endurance = select_one_value(user_id, f'e_endurance_{text_number}_2', 'user_id')

                if enemy1_endurance > 0 and enemy2_endurance > 0:
                    item1 = [types.InlineKeyboardButton("Битися з Грусом", callback_data='grus'),
                             types.InlineKeyboardButton("Битися з Індусом", callback_data='indus')]
                elif enemy1_endurance <= 0 and enemy2_endurance > 0:
                    item1 = [types.InlineKeyboardButton("Битися з Індусом", callback_data='indus')]
                elif enemy1_endurance > 0 and enemy2_endurance <= 0:
                    item1 = [types.InlineKeyboardButton("Битися з Грусом", callback_data='grus')]

            elif text_number == 172:
                enemy1_endurance = select_one_value(user_id, f'e_endurance_{text_number}_1', 'user_id')
                enemy2_endurance = select_one_value(user_id, f'e_endurance_{text_number}_2', 'user_id')

                if enemy1_endurance > 0 and enemy2_endurance > 0:
                    item1 = [types.InlineKeyboardButton("Битися з першим стражником", callback_data='first_g'),
                             types.InlineKeyboardButton("Битися з другим стражником", callback_data='second_g')]
                elif enemy1_endurance <= 0 and enemy2_endurance > 0:
                    item1 = [types.InlineKeyboardButton("Битися з другим стражником", callback_data='second_g')]
                elif enemy1_endurance > 0 and enemy2_endurance <= 0:
                    item1 = [types.InlineKeyboardButton("Битися з першим стражником", callback_data='first_g')]
            elif text_number == 234:
                enemy1_endurance = select_one_value(user_id, f'e_endurance_{text_number}_1', 'user_id')
                enemy2_endurance = select_one_value(user_id, f'e_endurance_{text_number}_2', 'user_id')

                if enemy1_endurance > 0 and enemy2_endurance > 0:
                    item1 = [types.InlineKeyboardButton("Битися з жителем півночі", callback_data='first_a_n'),
                             types.InlineKeyboardButton("Битися з другим аркадіанцем", callback_data='second_a_2')]
                elif enemy1_endurance <= 0 and enemy2_endurance > 0:
                    item1 = [types.InlineKeyboardButton("Битися з другим аркадіанцем", callback_data='second_a_2')]
                elif enemy1_endurance > 0 and enemy2_endurance <= 0:
                    item1 = [types.InlineKeyboardButton("Битися з жителем півночі", callback_data='first_a_n')]
            elif text_number == 244:
                enemy1_endurance = select_one_value(user_id, f'e_endurance_{text_number}_1', 'user_id')
                enemy2_endurance = select_one_value(user_id, f'e_endurance_{text_number}_2', 'user_id')

                if enemy1_endurance > 0 and enemy2_endurance > 0:
                    item1 = [types.InlineKeyboardButton("Перший громила", callback_data="first_h"),
                             types.InlineKeyboardButton("Другий громила", callback_data="second_h")]
                elif enemy1_endurance <= 0 and enemy2_endurance > 0:
                    item1 = [types.InlineKeyboardButton("Другий громила", callback_data="second_h")]
                elif enemy1_endurance > 0 and enemy2_endurance <= 0:
                    item1 = [types.InlineKeyboardButton("Перший громила", callback_data="first_h")]
            markup.add(*item1)
            await bot.send_message(callback_query.from_user.id,
                                   f"You are unlucky! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                   reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
        character.luck -= 1
        update_luck(callback_query.from_user.id, 'Luck', character.luck)

    else:
        markup = types.InlineKeyboardMarkup()
        item1 = [types.InlineKeyboardButton(m1, callback_data='4 rounds')]
        if text_number in [3, 4, 17, 35, 55, 82, 84, 104, 106, 107, 124, 133, 136, 150, 157, 161, 165, 190, 206, 215,
                           224, 243, 289, 295, 298, 313, 341, 351, 366, 367, 373, 375, 391]:
            item1 = [types.InlineKeyboardButton(m1, callback_data='fight')]
        elif text_number == 24:
            enemy1_endurance = select_one_value(user_id, f'e_endurance_{text_number}_1', 'user_id')
            enemy2_endurance = select_one_value(user_id, f'e_endurance_{text_number}_2', 'user_id')
            if enemy1_endurance > 0 and enemy2_endurance > 0:
                item1 = [types.InlineKeyboardButton("Битися з першим аркадіанцем", callback_data='first_a'),
                         types.InlineKeyboardButton("Битися з другим аркадіанцем", callback_data='second_a')]
            elif enemy1_endurance <= 0 and enemy2_endurance > 0:
                item1 = [types.InlineKeyboardButton("Битися з другим аркадіанцем", callback_data='second_a')]
            elif enemy1_endurance > 0 and enemy2_endurance <= 0:
                item1 = [types.InlineKeyboardButton("Битися з першим аркадіанцем", callback_data='first_a')]
        elif text_number == 113:
            enemy1_endurance = select_one_value(user_id, f'e_endurance_{text_number}_1', 'user_id')
            enemy2_endurance = select_one_value(user_id, f'e_endurance_{text_number}_2', 'user_id')
            if enemy1_endurance > 0 and enemy2_endurance > 0:
                item1 = [types.InlineKeyboardButton("Битися з Грусом", callback_data='grus'),
                         types.InlineKeyboardButton("Битися з Індусом", callback_data='indus')]
            elif enemy1_endurance <= 0 and enemy2_endurance > 0:
                item1 = [types.InlineKeyboardButton("Битися з Індусом", callback_data='indus')]
            elif enemy1_endurance > 0 and enemy2_endurance <= 0:
                item1 = [types.InlineKeyboardButton("Битися з Грусом", callback_data='grus')]
        elif text_number == 172:
            enemy1_endurance = select_one_value(user_id, f'e_endurance_{text_number}_1', 'user_id')
            enemy2_endurance = select_one_value(user_id, f'e_endurance_{text_number}_2', 'user_id')
            if enemy1_endurance > 0 and enemy2_endurance > 0:
                item1 = [types.InlineKeyboardButton("Битися з першим стражником", callback_data='first_g'),
                         types.InlineKeyboardButton("Битися з другим стражником", callback_data='second_g')]
            elif enemy1_endurance <= 0 and enemy2_endurance > 0:
                item1 = [types.InlineKeyboardButton("Битися з другим стражником", callback_data='second_g')]
            elif enemy1_endurance > 0 and enemy2_endurance <= 0:
                item1 = [types.InlineKeyboardButton("Битися з першим стражником", callback_data='first_g')]
        elif text_number == 234:
            enemy1_endurance = select_one_value(user_id, f'e_endurance_{text_number}_1', 'user_id')
            enemy2_endurance = select_one_value(user_id, f'e_endurance_{text_number}_2', 'user_id')
            if enemy1_endurance > 0 and enemy2_endurance > 0:
                item1 = [types.InlineKeyboardButton("Битися з жителем півночі", callback_data='first_a_n'),
                         types.InlineKeyboardButton("Битися з другим аркадіанцем", callback_data='second_a_2')]
            elif enemy1_endurance <= 0 and enemy2_endurance > 0:
                item1 = [types.InlineKeyboardButton("Битися з другим аркадіанцем", callback_data='second_a_2')]
            elif enemy1_endurance > 0 and enemy2_endurance <= 0:
                item1 = [types.InlineKeyboardButton("Битися з жителем півночі", callback_data='first_a_n')]
        elif text_number == 244:
            enemy1_endurance = select_one_value(user_id, f'e_endurance_{text_number}_1', 'user_id')
            enemy2_endurance = select_one_value(user_id, f'e_endurance_{text_number}_2', 'user_id')
            if enemy1_endurance > 0 and enemy2_endurance > 0:
                item1 = [types.InlineKeyboardButton("Перший громила", callback_data="first_h"),
                         types.InlineKeyboardButton("Другий громила", callback_data="second_h")]
            elif enemy1_endurance <= 0 and enemy2_endurance > 0:
                item1 = [types.InlineKeyboardButton("Другий громила", callback_data="second_h")]
            elif enemy1_endurance > 0 and enemy2_endurance <= 0:
                item1 = [types.InlineKeyboardButton("Перший громила", callback_data="first_h")]
        markup.add(*item1)
        await bot.send_message(callback_query.from_user.id, "You don't have any luck!",
                               reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == 'way3')
async def process_callback_way3(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    text_number = select_one_value(user_id, 'text_number', 'user_id')
    flag24 = select_one_value(user_id, 'flag24', 'user_id')
    flag113 = select_one_value(user_id, 'flag113', 'user_id')
    flag172 = select_one_value(user_id, 'flag172', 'user_id')
    flag234 = select_one_value(user_id, 'flag234', 'user_id')
    flag244 = select_one_value(user_id, 'flag244', 'user_id')
    m1 = 'Наступний удар'
    character_data = retrieve_character_data(user_id)
    text_to_creature_data_mapping = {
        2: ('e_mastery_2', 'e_endurance_2'),
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
        243: ('e_mastery_243', 'e_endurance_243'),
        289: ('e_mastery_289', 'e_endurance_289'),
        295: ('e_mastery_295', 'e_endurance_295'),
        313: ('e_mastery_313', 'e_endurance_313'),
        341: ('e_mastery_341', 'e_endurance_341'),
        351: ('e_mastery_351', 'e_endurance_351'),
        366: ('e_mastery_366', 'e_endurance_366'),
        367: ('e_mastery_367', 'e_endurance_367'),
        373: ('e_mastery_373', 'e_endurance_373'),
        375: ('e_mastery_375', 'e_endurance_375'),
        391: ('e_mastery_391', 'e_endurance_391'),
    }

    creature_data = retrieve_creature_data(callback_query.from_user.id,
                                           *text_to_creature_data_mapping.get(text_number, ('', '')))

    if text_number == 24 and flag24 in {1, 2}:
        columns_mapping = {
            1: (f'e_mastery_{text_number}_1', f'e_endurance_{text_number}_1'),
            2: (f'e_mastery_{text_number}_2', f'e_endurance_{text_number}_2'),
        }
        creature_data = retrieve_creature_data(user_id, *columns_mapping[flag24])

    elif text_number == 113 and flag113 in {1, 2}:
        columns_mapping = {
            1: (f'e_mastery_{text_number}_1', f'e_endurance_{text_number}_1'),
            2: (f'e_mastery_{text_number}_2', f'e_endurance_{text_number}_2'),
        }
        creature_data = retrieve_creature_data(user_id, *columns_mapping[flag113])

    elif text_number == 172 and flag172 in {1, 2}:
        columns_mapping = {
            1: (f'e_mastery_{text_number}_1', f'e_endurance_{text_number}_1'),
            2: (f'e_mastery_{text_number}_2', f'e_endurance_{text_number}_2'),
        }
        creature_data = retrieve_creature_data(user_id, *columns_mapping[flag172])

    elif text_number == 234 and flag234 in {1, 2}:
        columns_mapping = {
            1: (f'e_mastery_{text_number}_1', f'e_endurance_{text_number}_1'),
            2: (f'e_mastery_{text_number}_2', f'e_endurance_{text_number}_2'),
        }
        creature_data = retrieve_creature_data(user_id, *columns_mapping[flag234])

    elif text_number == 244 and flag244 in {1, 2}:
        columns_mapping = {
            1: (f'e_mastery_{text_number}_1', f'e_endurance_{text_number}_1'),
            2: (f'e_mastery_{text_number}_2', f'e_endurance_{text_number}_2'),
        }
        creature_data = retrieve_creature_data(user_id, *columns_mapping[flag244])

    character = Character(mastery=character_data[0], endurance=character_data[1], luck=character_data[2])
    creature = Character(mastery=creature_data[0], endurance=creature_data[1], luck=creature_data[2])
    if character.luck > 0:
        result = roll_dice_2()
        if result <= character.luck:
            character.endurance += 1
            update_character_endurance(user_id, 'Endurance', character.endurance)
            markup = types.InlineKeyboardMarkup()
            item1 = [types.InlineKeyboardButton(m1, callback_data='4 rounds')]
            markup.add(*item1)
            await bot.send_message(callback_query.from_user.id,
                                   f"You are lucky! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                   reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
        else:
            character.endurance -= 1
            update_character_endurance(callback_query.from_user.id, 'Endurance', character.endurance)
            if character.endurance > 0:
                markup = types.InlineKeyboardMarkup()
                if text_number == 2:
                    item1 = [types.InlineKeyboardButton(m1, callback_data='4 rounds')]
                elif text_number in [3, 4, 17, 24, 35, 55, 82, 84, 104, 106, 107, 113, 124, 133, 136, 150, 157, 161,
                                     165, 172, 190, 206, 215, 234, 243, 244, 289, 295, 313, 341, 351, 366, 367, 373,
                                     375, 391]:
                    item1 = [types.InlineKeyboardButton(m1, callback_data='fight')]
                markup.add(*item1)
                await bot.send_message(callback_query.from_user.id,
                                       f"You are unlucky! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                       reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
            else:
                await bot.send_message(callback_query.from_user.id,
                                       "Ти програв! Починай спочатку.")  # бот повідомляє про результат
            if text_number == 244 and character.endurance <= 4:
                update_one_value(user_id, 'Endurance', 4)
                item1 = [types.InlineKeyboardButton('Go on', callback_data='337')]
                markup.add(*item1)
                await bot.send_message(user_id,
                                       'Бій завершено. Ваша Витривалість становить 4 бали. Ваші супротивники втікають.',
                                       reply_markup=markup, parse_mode='Markdown')

        character.luck -= 1
        update_luck(callback_query.from_user.id, 'Luck', character.luck)
    else:
        markup = types.InlineKeyboardMarkup()
        item1 = [types.InlineKeyboardButton(m1, callback_data='4 rounds')]
        if text_number in [3, 4, 17, 35, 55, 82, 84, 104, 106, 107, 124, 133, 136, 150, 157, 161, 165, 190, 206, 215,
                           243, 289, 295, 313, 341, 351, 366, 367, 373, 375, 391]:
            item1 = [types.InlineKeyboardButton(m1, callback_data='fight')]
        elif text_number == 24:
            enemy1_endurance = select_one_value(user_id, f'e_endurance_{text_number}_1', 'user_id')
            enemy2_endurance = select_one_value(user_id, f'e_endurance_{text_number}_2', 'user_id')
            if enemy1_endurance > 0 and enemy2_endurance > 0:
                item1 = [types.InlineKeyboardButton("Битися з першим аркадіанцем", callback_data='first_a'),
                         types.InlineKeyboardButton("Битися з другим аркадіанцем", callback_data='second_a')]
            elif enemy1_endurance <= 0 and enemy2_endurance > 0:
                item1 = [types.InlineKeyboardButton("Битися з другим аркадіанцем", callback_data='second_a')]
            elif enemy1_endurance > 0 and enemy2_endurance <= 0:
                item1 = [types.InlineKeyboardButton("Битися з першим аркадіанцем", callback_data='first_a')]
        elif text_number == 113:
            enemy1_endurance = select_one_value(user_id, f'e_endurance_{text_number}_1', 'user_id')
            enemy2_endurance = select_one_value(user_id, f'e_endurance_{text_number}_2', 'user_id')
            if enemy1_endurance > 0 and enemy2_endurance > 0:
                item1 = [types.InlineKeyboardButton("Битися з Грусом", callback_data='grus'),
                         types.InlineKeyboardButton("Битися з Індусом", callback_data='indus')]
            elif enemy1_endurance <= 0 and enemy2_endurance > 0:
                item1 = [types.InlineKeyboardButton("Битися з Індусом", callback_data='indus')]
            elif enemy1_endurance > 0 and enemy2_endurance <= 0:
                item1 = [types.InlineKeyboardButton("Битися з Грусом", callback_data='grus')]
        elif text_number == 172:
            enemy1_endurance = select_one_value(user_id, f'e_endurance_{text_number}_1', 'user_id')
            enemy2_endurance = select_one_value(user_id, f'e_endurance_{text_number}_2', 'user_id')
            if enemy1_endurance > 0 and enemy2_endurance > 0:
                item1 = [types.InlineKeyboardButton("Битися з першим стражником", callback_data='first_g'),
                         types.InlineKeyboardButton("Битися з другим стражником", callback_data='second_g')]
            elif enemy1_endurance <= 0 and enemy2_endurance > 0:
                item1 = [types.InlineKeyboardButton("Битися з другим стражником", callback_data='second_g')]
            elif enemy1_endurance > 0 and enemy2_endurance <= 0:
                item1 = [types.InlineKeyboardButton("Битися з першим стражником", callback_data='first_g')]
        elif text_number == 234:
            enemy1_endurance = select_one_value(user_id, f'e_endurance_{text_number}_1', 'user_id')
            enemy2_endurance = select_one_value(user_id, f'e_endurance_{text_number}_2', 'user_id')
            if enemy1_endurance > 0 and enemy2_endurance > 0:
                item1 = [types.InlineKeyboardButton("Битися з жителем півночі", callback_data='first_a_n'),
                         types.InlineKeyboardButton("Битися з другим аркадіанцем", callback_data='second_a_2')]
            elif enemy1_endurance <= 0 and enemy2_endurance > 0:
                item1 = [types.InlineKeyboardButton("Битися з другим аркадіанцем", callback_data='second_a_2')]
            elif enemy1_endurance > 0 and enemy2_endurance <= 0:
                item1 = [types.InlineKeyboardButton("Битися з жителем півночі", callback_data='first_a_n')]
        elif text_number == 244:
            enemy1_endurance = select_one_value(user_id, f'e_endurance_{text_number}_1', 'user_id')
            enemy2_endurance = select_one_value(user_id, f'e_endurance_{text_number}_2', 'user_id')
            if enemy1_endurance > 0 and enemy2_endurance > 0:
                item1 = [types.InlineKeyboardButton("Перший громила", callback_data="first_h"),
                         types.InlineKeyboardButton("Другий громила", callback_data="second_h")]
            elif enemy1_endurance <= 0 and enemy2_endurance > 0:
                item1 = [types.InlineKeyboardButton("Другий громила", callback_data="second_h")]
            elif enemy1_endurance > 0 and enemy2_endurance <= 0:
                item1 = [types.InlineKeyboardButton("Перший громила", callback_data="first_h")]
        markup.add(*item1)
        await bot.send_message(user_id, "You don't have any luck!",
                               reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
    await callback_query.answer()


# async def send_continue(message):
#     m1 = 'Шлях 1'
#     m2 = 'Шлях 2'
#
#
#     markup = types.InlineKeyboardMarkup(row_width=2)
#     item1 = [types.InlineKeyboardButton(m1, callback_data='way1'),
#              types.InlineKeyboardButton(m2, callback_data='way2')]
#     markup.add(*item1)
#     await bot.send_message(message.chat.id, text.text_1, reply_markup=markup)  # бот дає переклад
#     # text_for_callmessage = f"⭐\n{value_eng}\n⭐"
#
#     # number_row = number
#     # print(f"Scenario {level}")
#     return m1, m2


async def send_periodic_messages(bot, user_ids):
    print('Bot entered the sending loop')
    while True:
        user_ids = get_values_if_conditions('user_id', 'Mastery')
        if user_ids:
            for user_id in user_ids:
                try:
                    pass
                    # await bot.send_message(user_id, f'Час тиснути <b>"{name_button2}"</b>.')
                except Exception as e:
                    logging.error(f"Failed to send message to user {user_id}: {e}")
        await asyncio.sleep(20)  # Send messages every 20 seconds


async def on_startup(dp):
    while True:
        user_ids = get_values_if_conditions('user_id', 'Mastery')
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

# async def read_time_data(number):
#     time_now = time.time()
#     word_id, user_id, eng_word, ua_word, transcription, digit, check_date, level, score, column1, column2 = get_one_row(
#         number)
#     odds = time_now - digit
#     return word_id, user_id, eng_word, ua_word, transcription, time_now, digit, check_date, odds, level, score, column1, column2

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
