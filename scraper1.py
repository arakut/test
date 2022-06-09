import json
import requests



def get_data():

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36',
    }

    url = 'https://api.kfc.com/api/store/v2/store.get_restaurants?showClosed=true'
    response = requests.get(url, headers=headers)
    data = response.json().get('searchResults')

    result_list = []
    count = 0

    while count!=len(data):
        for item in data:
            store = item.get('storePublic')

            if store.get('title').get('ru') == None:
                name = ''
            else:
                name = store.get('title').get('ru')

            if store.get('contacts').get('streetAddress').get('ru')==None:
                adress = ''
            else:
                adress = store.get('contacts').get('streetAddress').get('ru')

            if store.get('contacts').get('coordinates').get('geometry').get('coordinates')==None:
                latlon = ''
            else:
                latlon = store.get('contacts').get('coordinates').get('geometry').get('coordinates')

            if store.get('contacts').get('phoneNumber') == None:
                phones = ''
            else:
                phones = store.get('contacts').get('phoneNumber')

            if store.get('openingHours').get('regular').get('startTimeLocal') == None:
                start_working_hours = ['closed']
            else:
                start_working_hours = store.get('openingHours').get('regular').get('startTimeLocal')[:-3]

            if store.get('openingHours').get('regular').get('endTimeLocal') == None:
                end_working_hours = ['closed']
            else:
                end_working_hours = store.get('openingHours').get('regular').get('endTimeLocal')[:-3]

            result_list.append(
                {
                    'adress': ' '.join(adress.split()[1:]),
                    'latlon': latlon,
                    'name': name,
                    'phones': [phones],
                    'working_hours': 'closed' if end_working_hours==start_working_hours else [f'пн-пт {start_working_hours} до {end_working_hours}']
                },
            )
            count += 1
    with open('site1.json', 'w', encoding='utf-8') as file:
        json.dump(result_list, file, indent=4, ensure_ascii=False)


def main():
    get_data()

if __name__ == '__main__':
    main()