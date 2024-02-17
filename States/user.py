from aiogram.dispatcher.filters.state import State, StatesGroup


class registration(StatesGroup):
    MASTERY = State()
    ENDURANCE = State()
    LUCK = State()


class add_word(StatesGroup):
    word = State()


class nextmessage(StatesGroup):
    message1 = State()
