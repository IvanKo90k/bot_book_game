# Сукупний бот
# 1. Сервер.
# 2. Приймати від клієнта слова, які він хоче вивчити.
# 3. Панда.
# 4. Клієнт тисне спочатку на переклад. Розібратися з цією проблемою.
# 5. Реалізувати можливість надання клієнту переліку слів у форматі Excel за його запитом
# 6. Пропонувати 3000 слів до вивчення + дати можливість клієнту з цих слів обирати потрібні саме йому
# 7. Якщо клієнт натиснув "Дай мені слово" замість "Я знаю", то має бути відкат рівня?

import telebot
import bot8
import pandas as pd
import requests

# api_url = 'https://api.telegram.org/bot{6278513334:AAF4IKJsO6hiYtchRfERBrKdqG-clygvho0}/getUpdates'
# response = requests.get(api_url, timeout=60)


def run():
    while True:
        # print(1)
        bot8.welcome()
        bot8.lalala()
        # bot8.process_user_words()


run()