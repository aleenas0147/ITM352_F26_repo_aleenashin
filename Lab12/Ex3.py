import requests
from bs4 import BeautifulSoup

html = requests.get("https://shidler.hawaii.edu/itm/people").text
soup = BeautifulSoup(html, 'html.parser')
print(soup.prettify()[:500])
cards = soup.find_all('article')
print(len(cards))
print(cards[0].prettify())
import re
for card in cards:
    name = card.find('h2').get_text(strip=True)
    match = re.search(r'[\w.-]+@[\w.-]+', card.get_text())
    email = match.group() if match else 'N/A'
    print(name, '-', email)