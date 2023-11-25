import json
import os
import requests
from bs4 import BeautifulSoup


list = []

def get_info1():
    
    i = 1
    while(i<2):

        page = f'&page={i}'
        url = f'https://www.olx.ua/uk/nedvizhimost/kvartiry/dolgosrochnaya-arenda-kvartir/kiev/?search%5Bfilter_float_price%3Ato%5D=10000&search%5Bfilter_enum_number_of_rooms_string%5D%5B0%5D=odnokomnatnye&search%5Bfilter_enum_number_of_rooms_string%5D%5B1%5D=dvuhkomnatnye&search%5Bdistrict_id%5D=17&{page}'



        headers = {
            "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36 OPR/89.0.4447.64"
        }
        r = requests.get(url=url, headers=headers)
        with open(f"page{i}.html", "w") as file:
            file.write(r.text)
        with open(f"page{i}.html") as file:
                info = file.read()

        soup = BeautifulSoup(info, "lxml")

    
        for room in soup.find_all('div', class_ = 'css-1sw7q4x'):
            try:
                title = room.find('div', class_='css-u2ayx9').find('h6', class_='css-16v5mdi er34gjf0').text
                link = 'https://www.olx.ua' + room.find('a').get('href')
                price = room.find('div', class_='css-u2ayx9').find('p', class_='css-10b0gli er34gjf0').text


            except:
                pass
            list.append({
                'title' : title,
                'link' : link,
                'price' : price
            })
        i+=1

def get_info_description():



    for room in list:
        i=1
        headers = {
            "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36 OPR/89.0.4447.64"
        }
        r = requests.get(url=room['link'], headers=headers)

        info = r.text
        
        soup = BeautifulSoup(info, "lxml")


        room['additional_info'] = soup.find('div', class_='css-1t507yq er34gjf0').text



def dump():
    with open('list.json', 'w') as file:
        json.dump(list, file, ensure_ascii=False, indent=4)


def main():
    get_info1()
    get_info_description()
    dump()

if __name__ == '__main__':
    main()
