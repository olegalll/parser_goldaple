import requests
import json
import os


# Импортируем данные для запросов к API
from list_api_request_cnt_pages import url as pages_url, headers as pages_headers, cookies as pages_cookies, payload as pages_payload
from list_api_request_options import url as options_url, headers as options_headers, cookies as options_cookies, payload as options_payload

# Функция для получения количества страниц с продуктами
def get_cnt_pages_list():
    r = requests.post(pages_url, headers=pages_headers, cookies=pages_cookies, json=pages_payload)
    response_data = r.json()['data']['productsCount']
    return response_data

# Функция для отправки запроса к API с определенной страницей
def download_options(name_json, page=1):
    options_payload['pageNumber'] = page
    r = requests.post(options_url, headers=options_headers, cookies=options_cookies, json=options_payload)
    data = r.json()
    with open(name_json, 'w') as f:
        json.dump(data, f)

# Функция для получения содержимого списка продуктов
def get_content_list(name_json):
    with open(name_json, 'r') as f:
        data = json.load(f)
    
    products = []
    for product in data['data']['products']:
        product_info = {
            'itemId': product['itemId'],
            'brand': product['brand'],
            'name': product['name'],
            'actual_amount': product['price']['actual']['amount'] if product['price']['actual'] is not None else None,
            'old_amount': product['price']['old']['amount'] if product['price']['old'] is not None else None
        }
        products.append(product_info)
    return products



def delete_options(name_json):
    if os.path.exists('response.json'):
        os.remove('response.json')


def main():
    # total_pages = get_cnt_pages_list() / 24
    total_pages = 2
    name_json = 'response.json'

    for page_num in range(1, total_pages + 1):
        # download_options(name_json, page_num)
        get_content_list(name_json)
    # TODO: добавить сохранение в базу данных
        # delete_options(name_json)




    # TODO: написать парсер для каждой карточки

if __name__ == '__main__':
    
    main()

