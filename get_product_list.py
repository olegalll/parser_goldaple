"""
TODO: написать парсер для каждой карточки
TODO: создать базу для карточек
TODO: настроить получение картинок
CHECK: проверить можно ли подучать даты и способы доставки товара через API
"""

import json

from api_requests import get_cnt_pages_list, download_options, delete_options
import db

# Функция для получения содержимого списка продуктов
def get_content_list(name_json):
    with open(name_json, 'r') as f:
        data = json.load(f)
    
    products_list = []
    for product in data['data']['products']:
        product_info = {
            'itemId': product['itemId'],
            'mainVariantItemId': product['mainVariantItemId'],
            'brand': product['brand'],
            'name': product['name'],
            'actual_amount': product['price']['actual']['amount'] if product['price']['actual'] is not None else None,
            'old_amount': product['price']['old']['amount'] if product['price']['old'] is not None else None,
            'link': f'https://goldapple.ru{product["url"]}'
        }
        products_list.append(product_info)
    return products_list


def main():
    connection = db.connection()
    db.check_table_list_products(connection)


    # total_pages = get_cnt_pages_list() / 24
    total_pages = 1
    name_json = 'jsons/response.json'

    for page_num in range(1, total_pages + 1):
        download_options(name_json, page_num)
        products_list = get_content_list(name_json)
        db.save_list_products(connection, products_list)
        # delete_options(name_json)

    db.close_connection(connection)




if __name__ == '__main__':

    main()

