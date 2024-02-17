from loader import dp, types, bot
import Functions.DB
from dice import Character, create_character, battle
import random

# Character creation
# character = create_character()
# creature_mastery = int(input('Enter mastery: '))
# creature_endurance = int(input('Enter endurance: '))
# creature = Character(creature_mastery, creature_endurance, 0)  # You can specify the creature's stats
#
# print(f"Character Mastery: {character.mastery}")
# print(f"Character Endurance: {character.endurance}")
# print(f"Character Luck: {character.luck}")
#
# print("\nLet the battle begin!\n")
# battle(character, creature)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    global flag_first_client, id_for_start
    id_for_start = message.from_user.id
    print("Користувач {0.first_name} натиснув start".format(message.from_user))
    count_rows_with_value = Functions.DB.count_rows_with_value(message.from_user.id)
    if count_rows_with_value > 0:
        await message.answer('Радий тебе бачити.')
        # await Functions.Functions.send_random_sticker(bot, id_for_start, stickers_start)
    else:
        flag_first_client = True
        # await Functions.Functions.send_random_sticker(bot, id_for_start, stickers_start)
        markup = types.InlineKeyboardMarkup(row_width=2)
        item4 = [types.InlineKeyboardButton("Так", callback_data='yes_helper'),
                 types.InlineKeyboardButton("Ні", callback_data='no_helper')]
        markup.add(*item4)
        await bot.send_message(message.chat.id,
                               'Дозволю собі припустити, що ти бажаєш покращити свою англійську. Хочеш, щоб я був твоїм помічником?',
                               reply_markup=markup)
