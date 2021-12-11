# -*- coding: utf-8 -*-
import time
from steam_community_market import Market, AppID
from bs4 import BeautifulSoup as bs
import requests
#from multiprocessing import Pool
import vk_api

token = '946104a1a4140405cb3993215b68e7ccae7ac3e90b695becd1dbc45688ee25bbe063e38e6eef7bf4569a3'
vk_session = vk_api.VkApi(token=token)

def send_msg(message):
    global vk_session
    vk_session.method('messages.send', {'user_id': '254896650', 'message': message, 'random_id':0 })
    vk_session.method('messages.send', {'user_id': '245210027', 'message': message, 'random_id': 0})


def parse_sticker(name):
    url=name.replace('(','%28').replace(')','%29').replace('|','%7C').replace(' ','+').replace(' ','+')
    url=f'https://steamcommunity.com/market/search?category_730_ItemSet%5B%5D=any&category_730_ProPlayer%5B%5D=any&category_730_StickerCapsule%5B%5D=any&category_730_TournamentTeam%5B%5D=any&category_730_Weapon%5B%5D=any&appid=730&q=Sticker+%7C+{url}'
    req=requests.get(url)
    soup = bs(req.text, 'html.parser')
    div=soup.find('div',class_='market_listing_row market_recent_listing_row market_listing_searchresult')
    div_1=div.find('div',class_='market_listing_price_listings_block')
    div_2=div_1.find('div',class_='market_listing_right_cell market_listing_their_price')
    span=div_2.find('span',class_='market_table_value normal_price')
    price=span.find('span',class_='normal_price').text
    #print(url)
    #print(price)
    return (price.replace('$','').replace(' USD',''))
def parse_weapons(name,color,rare,start):
    if start>=45:
        pass
    else:
        url = f'https://steamcommunity.com/market/listings/730/{name}%20%7C%20{color}%20%28{rare}%29/render/?query=&start={start}&count={45-start}&country=RU&language=english&currency=1'
        data = requests.get(url).json()
        i=start
        check=1
        try:
            x=data['assets']['730']['2'].values()
        except:
            check=0
            #print(data)
        if check==1:
            try:
                market = Market("USD")
                item = f"{name} | {color} ({rare})".replace('%20', ' ')
                print(item)
                lowest_price = float(market.get_lowest_price(item, AppID.CSGO))
                print(f'{item} -- lowest_price: {lowest_price} * 1.2 = {lowest_price*1.2}')
                for skin in data['assets']['730']['2'].values():
                    i += 1
                    try:
                        cur_price=round(float(list(data['listinginfo'].values())[i-start-1]['converted_price']) *0.01147962409941, 2)
                        print(f'Cur price: {cur_price}')
                        if lowest_price*1.2>=cur_price:
                            #print(url)
                            if skin['descriptions'][-1]['value'] != ' ':
                                desc = skin['descriptions'][-1]
                                if desc['value'] != ' ':
                                    value = desc['value'].split('<br>')[2]
                                    sticks = (value[value.find(': ') + 2:value.find('<')]).split(', ')
                                    print(f"[FIND] {i + 1}: {url[:url.find('/render/')]}\n{sticks}\n")
                                    total_price_stick = 0
                                    for sticker in sticks:
                                        total_price_stick += float(parse_sticker(sticker))
                                        time.sleep(10)
                                    total_price_stick = round(total_price_stick, 2)
                                    print(lowest_price,cur_price)
                                    if total_price_stick>=6.8:
                                        send_msg(f"Оружие: {item}\nСтикеры: {sticks}\nОбщая цена стикеров: {total_price_stick} $\nМинимальная цена оружия: {lowest_price} $\nЦена данного предложения: {cur_price} $\nПорядковый номер: {i}\n{url[:url.find('/render/')]}\n")
                                        print('Сообщение отправлено')
                                    #cur_list.append([item, url[:url.find('/render/')], lowest_price, cur_price, total_price_stick, i])

                    except Exception as ex:
                        print(f'error  ---  {ex}')
                        time.sleep(50)
                        parse_weapons(name, color, rare, i)
            except:
                print('ERROR FUCKED LIBRARY STEAM_COMMUNITY_MARKET')
                time.sleep(60)
                parse_weapons(name, color, rare, i)
        else:
            time.sleep(120)
            parse_weapons(name,color,rare,i)

def recorder(record):
    name=record[1]
    color=record[3]
    rare=record[2]
    print(f'{record[0]} Weapon {name} -- {rare} -- {color}')
    name_url=name.replace(' ','%20')
    color_url=color.replace(' ','%20')
    rare_url = rare.replace(' ', '%20')
    parse_weapons(name_url,color_url, rare_url,0)

def main_parse():
    import sqlite3
    conn = sqlite3.connect('steam.db')
    cur = conn.cursor()
    cur.execute("""SELECT * from weapons""")
    records=cur.fetchall()
    list_good=[]
    for rec in records:
        recorder(rec)

if __name__ == '__main__':
    print(main_parse())