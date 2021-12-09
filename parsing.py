url='https://steamcommunity.com/market/listings/730/Tec-9%20%7C%20Hades%20%28Battle-Scarred%29'
from bs4 import BeautifulSoup as bs
import requests
print(url)
'''
page = requests.get(url)
text=page.text
with open('page.html','w',encoding="utf-8") as f:
    f.write(text)'''

import requests


data = requests.get('https://steamcommunity.com/market/listings/730/P2000%20%7C%20Coach%20Class%20%28Minimal%20Wear%29/render/?query=&start=0&count=10&country=RU&language=english&currency=1').json()
print('\n\n\n\n\n\n\n=======================================')
for skin in data['assets']['730']['2'].values():
    if len(skin['descriptions'])==7:
        desc=skin['descriptions'][6]
        value=desc['value'].split('<br>')[2]
        print(f"[FIND] {value[value.find(': ')+2:value.find('<')]}")
    else:
        print("This weapon don't have stickers(")

