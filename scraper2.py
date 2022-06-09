import re
import json
from bs4 import BeautifulSoup
import requests


### Основной сайт, откуда берется вся информация
url = 'https://www.ziko.pl/lokalizator/'

### Даем понять сайту, что мы не бот
headers ={
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36',
}

with open('index2.html') as file:
    info_hours = file.read()

soup_hours = BeautifulSoup(info_hours, 'lxml')


## Отправляем запрос на сайт при помощи библиотеки requests
req1 = requests.get(url, headers)

## Сохраняем копию сайта, чтобы работать с ним локально
with open ('index2.html', 'w', encoding='utf-8') as file:
    file.write(req1.text)


def get_data():
    '''Функция для получения всех нужным нам данных с сайта с последующей записью в Json-формат'''

    ### Открываем локальную копию сайта
    with open ('index2.html', encoding='utf-8') as file:
        src = file.read()

    ### Создаем объект класса BeautifulSoup для парсинга ссылок карточек магазинов
    soup = BeautifulSoup(src, 'lxml')
    shops = soup.find('tbody').find_all('tr')

    ### Получаем ссылки всех карточек магазинов
    shops_url = []
    data_results = []
    for shop in shops:
        shop_url = 'https://www.ziko.pl' + shop.find('td', class_='mp-table-access').find('div', class_='morepharmacy').find('a').get('href')
        shops_url.append(shop_url)

    counter = 1
    ### Основной цикл, который парсит всю информацию с карточки магазина
    for item in shops_url:
        req = requests.get(item, headers)
        item_name = '-'.join(item.split('/')[-4:])
        ### Сохранение карточек магазинов
        with open(f'data/{item_name}.html', 'w', encoding='utf-8') as file:
            file.write(req.text)

        ### Чтение файла для дальнейшего парсинга адреса, координат, наименования магазина, телефона
        with open(f'data/{item_name}.html') as file:
            src = file.read()

        ### Чтение файла для дальнейшего парсинга часов работы
        with open('index2.html') as file:
            info_hours = file.read()

        ### Создаем объект класса BeautifulSoup для парсинга необходимых данных, кроме часов работы
        soup = BeautifulSoup(src, 'lxml')

        ### Парсим нужную информации из блоков html кода
        shop_data = soup.find('div', class_= 'leftdetailsbox')
        coords_shop = soup.find('div', class_='coordinates')

        ### Создаем объект класса BeautifulSoup для парсинга часов работы
        soup_hours = BeautifulSoup(info_hours, 'lxml')
        info_work = soup_hours.find('td', class_='mp-table-hours').find_all('span')
        info_adress = soup_hours.find('td', class_='mp-table-address').next_element.text

        working_hours = []
        for item in range(len(info_work)):
            info_work[item] = info_work[item].text.replace('sobota','sob').replace('niedziela handlowa','nie').replace('niedziela niehandlowa','nied nieh')

        while len(info_work)!=0:
            working_hours.append(info_work[0]+info_work[1])
            info_work.remove(info_work[0])
            info_work.remove(info_work[0])

        ### Получение нужных данных
        adress = soup_hours.find('td', class_='mp-table-address').next_element.text
        latlon = [*reversed(sorted(coords_shop.text.split())[:2])]
        name = ' '.join(shop_data.find_next().text.split()[-2:])
        phones = shop_data.find('a').text.split(',')

        # Дополнительный словарь с адресами и часами рабоы
        info_work_hours = {
            info_adress:working_hours
        }
        working_hours = info_work_hours.get(adress)

        ### Создание словаря нужных данных для дальнейшей записи в json-файл

        data_results.append(
            {
                'address': adress,
                'latlon': latlon,
                'name': name.strip(),
                'phones': phones,
                'working_hours': working_hours
            }
        )
        print(f'[+] Обработано магазинов {counter} из {len(shops_url)}')
        counter += 1
        ### Запись собранных данных в json-файл
    with open('site2.json', 'w', encoding='utf-8') as file:
        json.dump(data_results, file, indent=4, ensure_ascii=False)






# info_adress = soup_hours.find_all('td', class_='mp-table-address')
# adresses = [adress.next_element.text for adress in info_adress]

# info_names = soup_hours.find_all('div', class_='mp-list-icons-wrapper')
# names = [name.previous.text.strip() for name in info_names]

# phones_info = soup_hours.find_all('td', class_='mp-table-hours')
# phones = [phone.previous_element.previous_element.previous_element.text.strip()[5:] for phone in phones_info]

# info_work = soup_hours.find_all('td', class_='mp-table-hours')
#
# working_hours = []
# for item in info_work:
#     elem = item.find_all('span')
#
#     for item in range(len(elem)):
#         elem[item] = elem[item].text.replace('sobota', 'sob').replace('niedziela handlowa', 'nie').replace('niedziela niehandlowa', 'nied nieh')
#
#     work = []
#     while len(elem) != 0:
#         work.append(elem[0] + elem[1])
#         elem.remove(elem[0])
#         elem.remove(elem[0])
#     working_hours.append(work)

def main():
    get_data()

if __name__ == '__main__':
    main()