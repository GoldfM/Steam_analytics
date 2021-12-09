import time

from bs4 import BeautifulSoup as bs
import requests
from multiprocessing import Pool
def parse_weapons(name,color,rare,count):
    url = f'https://steamcommunity.com/market/listings/730/{name}%20%7C%20{color}%20%28{rare}%29/render/?query=&start=0&count={count}&country=RU&language=english&currency=1'
    data = requests.get(url).json()

    i=0
    for skin in data['assets']['730']['2'].values():
        i+=1
        if skin['descriptions'][-1]['value']!=' ':
            desc = skin['descriptions'][-1]
            if desc['value']!=' ':
                value = desc['value'].split('<br>')[2]
                print(f"[FIND] {i}: {url[:url.find('/render/')]}\n{value[value.find(': ') + 2:value.find('<')]}\n\n")
        else:
            print(f'{i} HAVE NOT STICKERS')
    '''except:
        print(url)
        if count==5:
            pass
        else:
            parse_weapons(name,color,rare,count-20)'''
def recorder(record):
    time.sleep(1)
    name=record[1]
    color=record[3]
    rare=record[2]
    print(f'{record[0]} Weapon {name} -- {rare} -- {color}')
    name_url=name.replace(' ','%20')
    color_url=color.replace(' ','%20')
    rare_url = rare.replace(' ', '%20')
    parse_weapons(name_url,color_url, rare_url,45)


def main_parse():
    import sqlite3
    conn = sqlite3.connect('steam.db')
    cur = conn.cursor()
    cur.execute("""SELECT * from weapons""")
    records=cur.fetchall()
    for rec in records:
        recorder(rec)
    '''with Pool(2) as pool:
        pool.map(recorder, records)'''
if __name__ == '__main__':
    main_parse()