import requests
from bs4 import BeautifulSoup
import re

# word = str(input('Введіть слово: '))

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'}

def phonetic_transcription(word):
    page = requests.get(
    url=f'https://www.oxfordlearnersdictionaries.com/definition/english/{word}',
    headers=headers).text

    soup = BeautifulSoup(page, 'lxml')

    section = soup.find('span', class_='phon')


    if section:
        phonetic_transcription = re.findall(r'/(.*?)/', section.text)
        if phonetic_transcription:
            phonetic_transcription = f'/{phonetic_transcription[0]}/'
            print(phonetic_transcription)
            return phonetic_transcription
        else:
            print("No phonetic transcription found.")
    else:
        print("Word not found in the dictionary.")

# url=f'https://www.oxfordlearnersdictionaries.com/definition/english/lion?q={word}',