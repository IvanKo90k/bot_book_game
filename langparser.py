import requests
from bs4 import BeautifulSoup

word = str(input('Введіть слово: '))

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'}

page = requests.get(
    url=f'https://context.reverso.net/%D0%BF%D0%B5%D1%80%D0%B5%D0%BA%D0%BB%D0%B0%D0%B4/%D1%83%D0%BA%D1%80%D0%B0%D1%97%D0%BD%D1%81%D1%8C%D0%BA%D0%B0-%D0%B0%D0%BD%D0%B3%D0%BB%D1%96%D0%B9%D1%81%D1%8C%D0%BA%D0%B0/{word}',
    headers=headers).text
# page = requests.get(
#     url=f'https://context.reverso.net/%D0%BF%D0%B5%D1%80%D0%B5%D0%BA%D0%BB%D0%B0%D0%B4/%D0%B0%D0%BD%D0%B3%D0%BB%D1%96%D0%B9%D1%81%D1%8C%D0%BA%D0%B0-%D1%83%D0%BA%D1%80%D0%B0%D1%97%D0%BD%D1%81%D1%8C%D0%BA%D0%B0/{word}',
#     headers=headers).text

soup = BeautifulSoup(page, 'lxml')

# section = soup.find('section', id='examples-content')

# divs = section.find_all('div', class_='example')
divs = soup.find_all('div', class_='example')
example_sentences = []

for div in divs:
    content = div.find('div', class_='trg ltr').text.strip()
    if 'lion' in content.lower():
        example_sentences.append(content)
    # example_sentences.append(content)
print(example_sentences, len(example_sentences))
