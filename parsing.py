import time
from steam_community_market import Market, AppID
from bs4 import BeautifulSoup as bs
import requests
#from multiprocessing import Pool
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
def parse_weapons(name,color,rare,index):
    count=[45,45,30,10][index]
    url = f'https://steamcommunity.com/market/listings/730/{name}%20%7C%20{color}%20%28{rare}%29/render/?query=&start=0&count={count}&country=RU&language=english&currency=1'
    data = requests.get(url).json()
    i=-1
    cur_list=[]
    try:
        for skin in data['assets']['730']['2'].values():
            i+=1
            if skin['descriptions'][-1]['value']!=' ':
                desc = skin['descriptions'][-1]
                if desc['value']!=' ':
                    value = desc['value'].split('<br>')[2]
                    sticks=(value[value.find(': ') + 2:value.find('<')]).split(', ')
                    print(f"[FIND] {i+1}: {url[:url.find('/render/')]}\n{sticks}\n")
                    total_price_stick=0
                    for sticker in sticks:
                        total_price_stick+=float(parse_sticker(sticker))
                        time.sleep(5)
                    market = Market("USD")
                    item = f"{name} | {color} ({rare})".replace('%20',' ')
                    lowest_price=market.get_lowest_price(item, AppID.CSGO)
                    cur_price=data['listinginfo'].values()
                    cur_price=round(list(cur_price)[i]['converted_price']*0.01147962409941,2)
                    cur_list.append([item,url[:url.find('/render/')],lowest_price,cur_price,total_price_stick,i])


            else:
                pass
    except:
        print('Error  --  ', url)
        if index==3:
            time.sleep(30)
        else:
            time.sleep(60)
            cur_list=parse_weapons(name,color,rare,index+1)
    return cur_list

def recorder(record):
    name=record[1]
    color=record[3]
    rare=record[2]
    print(f'{record[0]} Weapon {name} -- {rare} -- {color}')
    name_url=name.replace(' ','%20')
    color_url=color.replace(' ','%20')
    rare_url = rare.replace(' ', '%20')
    return(parse_weapons(name_url,color_url, rare_url,0))


def main_parse():
    import sqlite3
    conn = sqlite3.connect('steam.db')
    cur = conn.cursor()
    cur.execute("""SELECT * from weapons""")
    records=cur.fetchall()
    list_good=[]
    for rec in records:
        list_good.append(recorder(rec))
    return (list_good)
if __name__ == '__main__':
    main_parse()