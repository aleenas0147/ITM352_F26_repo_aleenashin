import requests
from bs4 import BeautifulSoup

url = "https://www.hicentral.com/hawaii-mortgage-rates.php"
html = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}).text
soup = BeautifulSoup(html, 'html.parser')

bank = ''
for row in soup.find('table').find_all('tr')[1:]:   # skip header row
    cells = row.find_all('td')
    if len(cells) < 5:
        continue
    b = cells[0].find('b')
    if b:
        bank = b.get_text(strip=True)
    term, rate, points, apr = [c.get_text(strip=True) for c in cells[1:5]]
    print(f"{bank}: {term} | Rate {rate} | Points {points} | APR {apr}")