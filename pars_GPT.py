import requests
from bs4 import BeautifulSoup

def get_cambridge_definition(word):
    base_url = 'https://dictionary.cambridge.org/dictionary/english/'
    url = f'{base_url}{word}'

    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for successful response (status code 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract the definition from the webpage (adjust the CSS selector as per the site's structure)
        definition = soup.select_one('.def').get_text().strip()
        return definition
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
        return None

# Test the function with a word
word = str(input('Веедіть слово: '))
definition = get_cambridge_definition(word)
if definition:
    print(f"Definition of '{word}': {definition}")
else:
    print(f"Definition of '{word}' not found.")
