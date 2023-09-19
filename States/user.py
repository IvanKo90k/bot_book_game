from aiogram.dispatcher.filters.state import State, StatesGroup


class registration(StatesGroup):
    eng_word = State()
    ua_word = State()


class add_word(StatesGroup):
    word = State()

class nextmessage(StatesGroup):
    message1 = State()