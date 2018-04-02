import requests
from bs4 import BeautifulSoup

req = requests.get('https://www.melon.com/chart/index.htm')
html = req.text

soup = BeautifulSoup(html, 'html.parser')

my_titles = soup.select(
    'span > a'
    )

i = 0

for title in my_titles:
    if title.text == "마마무":
        print(f"{title.text}의 {my_titles[i-1].text}의 순위는 {i//2}이다.")
    i = i + 1