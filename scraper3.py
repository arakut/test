import json
import re

from bs4 import BeautifulSoup
import requests



# url = 'https://monomax.by/map'
#
# headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36'
#     }
#
# req = requests.get(url, headers)
# src = req.text
# # print(src)

# with open('index3.html', 'w', encoding='utf-8') as file:
#     file.write(src)


def get_data():
    data = []

    with open('index3.html', encoding='utf-8') as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')
    all = soup.find_all(class_='shop')
    coords = soup.find(text=re.compile('Placemark')).split()
    latlon = []
    for item in coords:
        if '53.' in item:
            latlon.append((item))
        elif '27.' in item:
            latlon.append((item))

    box = []
    for elem in range(len(latlon)):
        while len(box)!=10:
            box.append((latlon[elem]+' '+latlon[elem+1]))
            latlon.remove(latlon[0])
            latlon.remove(latlon[0])


    count = 1
    for shop in all:
        adress = shop.find(class_='name').text
        phone = shop.find(class_='phone').text
        phone = re.sub("\(*\)*\ *","", phone)
        data.append(
            {
                'adress':adress,
                'latlon': box[count],
                'name':'Мономах',
                'phones': phone.split(),
            }
        )
        count+=1
    with open('site3.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def main():
    get_data()

if __name__ == '__main__':
    main()