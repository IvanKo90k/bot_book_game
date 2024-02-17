import random
from loader import dp, types, bot
import Functions.DB, Functions.Functions
# from Handlers.User import number_text
import asyncio


def roll_dice_2():
    return random.randint(1, 6) + random.randint(1, 6)


# async def battle(bot, message, character, creature):
#     m1, m2 = 'Наступний удар', 'Випробувати Удачу'
#
#     # Step 1: Roll dice for creature's attack
#     creature_attack = roll_dice_2() + creature.mastery
#
#     # Step 2: Roll dice for player's attack
#     player_attack = roll_dice_2() + character.mastery
#
#     # Step 3: Compare attack values
#     if player_attack > creature_attack:
#         # Player damages the creature
#         creature.endurance -= 2
#         indx = Functions.DB.count_rows_in_database()
#         Functions.DB.update_endurance(creature.endurance, indx)
#         if character.luck > 0:
#             markup = types.InlineKeyboardMarkup(row_width=2)
#             item1 = [types.InlineKeyboardButton(m1, callback_data='way1'),
#                      types.InlineKeyboardButton(m2, callback_data='way2')]
#             markup.add(*item1)
#             await bot.send_message(message.chat.id,
#                                    f"Player damages the creature! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
#                                    reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
#         else:
#             markup = types.InlineKeyboardMarkup()
#             item1 = [types.InlineKeyboardButton(m1, callback_data='way1')]
#             markup.add(*item1)
#             await bot.send_message(message.chat.id,
#                                    f"Player damages the creature! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
#                                    reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
#     elif creature_attack > player_attack:
#         # Creature damages the player
#         character.endurance -= 2
#         Functions.DB.update_endurance(character.endurance, 1)
#         if character.luck > 0:
#             markup = types.InlineKeyboardMarkup()
#             item1 = [types.InlineKeyboardButton(m1, callback_data='way1'),
#                      types.InlineKeyboardButton(m2, callback_data='way3')]
#             markup.add(*item1)
#             await bot.send_message(message.chat.id,
#                                    f"Creature damages the player! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
#                                    reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
#         else:
#             markup = types.InlineKeyboardMarkup()
#             item1 = [types.InlineKeyboardButton(m1, callback_data='way1')]
#             markup.add(*item1)
#             await bot.send_message(message.chat.id,
#                                    f"Creature damages the player! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
#                                    reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
#     else:
#         # Both parry, start a new round
#         markup = types.InlineKeyboardMarkup()
#         item1 = [types.InlineKeyboardButton(m1, callback_data='way1')]
#         markup.add(*item1)
#         await bot.send_message(message.chat.id, "Both parry, starting a new round.",
#                                reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі


# @dp.callback_query_handler(lambda c: c.data == 'way1')
# async def process_callback_way1(callback_query: types.CallbackQuery):
#     m1, m2 = 'Наступний удар', 'Випробувати Удачу'
#     indx = Functions.DB.count_rows_in_database()
#     character_data, creature_data = Functions.DB.retrieve_character_data_id(
#         1), Functions.DB.retrieve_character_data_id(indx)
#     character = Functions.Functions.Character(mastery=character_data[0], endurance=character_data[1],
#                                               luck=character_data[2])
#     creature = Functions.Functions.Character(mastery=creature_data[0], endurance=creature_data[1],
#                                              luck=creature_data[2])
#
#     if character.endurance > 0 and creature.endurance > 0:
#         # Step 1: Roll dice for creature's attack
#         creature_attack = roll_dice_2() + creature.mastery
#
#         # Step 2: Roll dice for player's attack
#         player_attack = roll_dice_2() + character.mastery
#
#         # Step 3: Compare attack values
#         if player_attack > creature_attack:
#             # Player damages the creature
#             creature.endurance -= 2
#             Functions.DB.update_endurance(creature.endurance, indx)
#             if creature.endurance > 0:
#                 if character.luck > 0:
#                     markup = types.InlineKeyboardMarkup(row_width=2)
#                     item1 = [types.InlineKeyboardButton(m1, callback_data='way1'),
#                              types.InlineKeyboardButton(m2, callback_data='way2')]
#                     markup.add(*item1)
#                     await bot.send_message(callback_query.from_user.id,
#                                            f"Player damages the creature! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
#                                            reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
#                 else:
#                     markup = types.InlineKeyboardMarkup()
#                     item1 = [types.InlineKeyboardButton(m1, callback_data='way1')]
#                     markup.add(*item1)
#                     await bot.send_message(callback_query.from_user.id,
#                                            f"Player damages the creature! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
#                                            reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
#             else:
#                 await bot.send_message(callback_query.from_user.id, "The player wins!")  # бот повідомляє про результат
#         elif creature_attack > player_attack:
#             # Creature damages the player
#             character.endurance -= 2
#             Functions.DB.update_endurance(character.endurance, 1)
#             if character.endurance > 0:
#                 if character.luck > 0:
#                     markup = types.InlineKeyboardMarkup(row_width=2)
#                     item1 = [types.InlineKeyboardButton(m1, callback_data='way1'),
#                              types.InlineKeyboardButton(m2, callback_data='way3')]
#                     markup.add(*item1)
#                     await bot.send_message(callback_query.from_user.id,
#                                            f"Creature damages the player! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
#                                            reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
#                 else:
#                     markup = types.InlineKeyboardMarkup()
#                     item1 = [types.InlineKeyboardButton(m1, callback_data='way1')]
#                     markup.add(*item1)
#                     await bot.send_message(callback_query.from_user.id,
#                                            f"Creature damages the player! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
#                                            reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
#             else:
#                 await bot.send_message(callback_query.from_user.id,
#                                        "The creature wins!")  # бот повідомляє про результат
#         else:
#             # Both parry, start a new round
#             markup = types.InlineKeyboardMarkup()
#             item1 = [types.InlineKeyboardButton(m1, callback_data='way1')]
#             markup.add(*item1)
#             await bot.send_message(callback_query.from_user.id, "Both parry, starting a new round.",
#                                    reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
#     await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == 'way2.0')
async def process_callback_way2(callback_query: types.CallbackQuery):
    # global number_text
    print("Зайшли в Удачу")
    m1 = 'Наступний удар'
    character_data = Functions.DB.retrieve_character_data_id(1)
    creature_data = Functions.DB.retrieve_creature_data(callback_query.from_user.id, 'e_mastery_2', 'e_endurance_2')
    character = Functions.Functions.Character(mastery=character_data[0], endurance=character_data[1],
                                              luck=character_data[2])
    creature = Functions.Functions.Character(mastery=creature_data[0], endurance=creature_data[1],
                                             luck=creature_data[2])
    if character.luck > 0:
        result = roll_dice_2()
        if result <= character.luck:
            creature.endurance -= 2
            Functions.DB.update_character_endurance(callback_query.from_user.id, 'e_endurance_2', creature.endurance)
            if creature.endurance > 0:
                markup = types.InlineKeyboardMarkup()
                item1 = [types.InlineKeyboardButton(m1, callback_data='4 rounds')]
                markup.add(*item1)
                await bot.send_message(callback_query.from_user.id,
                                       f"You are lucky! Player damages the creature! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                       reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
            else:
                # if number_text != 2:
                await bot.send_message(callback_query.from_user.id, "The player wins!")  # бот повідомляє про результат
        else:
            creature.endurance += 1
            Functions.DB.update_character_endurance(callback_query.from_user.id, 'e_endurance_2', creature.endurance)
            markup = types.InlineKeyboardMarkup()
            item1 = [types.InlineKeyboardButton(m1, callback_data='4 rounds')]
            markup.add(*item1)
            await bot.send_message(callback_query.from_user.id,
                                   f"You are unlucky! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                   reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
        character.luck -= 1
        Functions.DB.update_luck(callback_query.from_user.id, 'Luck', character.luck)
    else:
        markup = types.InlineKeyboardMarkup()
        item1 = [types.InlineKeyboardButton(m1, callback_data='4 rounds')]
        markup.add(*item1)
        await bot.send_message(callback_query.from_user.id, "You don't have any luck!",
                               reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == 'way3')
async def process_callback_way3(callback_query: types.CallbackQuery):
    # global number_text
    m1 = 'Наступний удар'
    character_data = Functions.DB.retrieve_character_data_id(1)
    creature_data = Functions.DB.retrieve_creature_data(callback_query.from_user.id, 'e_mastery_2', 'e_endurance_2')
    character = Functions.Functions.Character(mastery=character_data[0], endurance=character_data[1],
                                              luck=character_data[2])
    creature = Functions.Functions.Character(mastery=creature_data[0], endurance=creature_data[1],
                                             luck=creature_data[2])
    if character.luck > 0:
        result = roll_dice_2()
        if result <= character.luck:
            character.endurance += 1
            Functions.DB.update_character_endurance(callback_query.from_user.id, 'Endurance', character.endurance)
            markup = types.InlineKeyboardMarkup()
            item1 = [types.InlineKeyboardButton(m1, callback_data='4 rounds')]
            markup.add(*item1)
            await bot.send_message(callback_query.from_user.id,
                                   f"You are lucky! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                   reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
        else:
            character.endurance -= 1
            Functions.DB.update_character_endurance(callback_query.from_user.id, 'Endurance', character.endurance)
            if character.endurance > 0:
                markup = types.InlineKeyboardMarkup()
                item1 = [types.InlineKeyboardButton(m1, callback_data='4 rounds')]
                markup.add(*item1)
                await bot.send_message(callback_query.from_user.id,
                                       f"You are unlucky! Player endurance: {character.endurance}, Creature endurance: {creature.endurance}",
                                       reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
            else:
                # if number_text != 2:
                await bot.send_message(callback_query.from_user.id,
                                       "The creature wins!")  # бот повідомляє про результат
        character.luck -= 1
        Functions.DB.update_luck(callback_query.from_user.id, 'Luck', character.luck)
    else:
        markup = types.InlineKeyboardMarkup()
        item1 = [types.InlineKeyboardButton(m1, callback_data='4 rounds')]
        markup.add(*item1)
        await bot.send_message(callback_query.from_user.id, "You don't have any luck!",
                               reply_markup=markup)  # бот повідомляє про результат і питає, що робити далі
    await callback_query.answer()
