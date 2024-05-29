import requests
import json
import os


# Импортируем данные для запросов к API
from request_wrapper import RequestWrapper
from payload_builder import PayloadBuilder

# Функция для получения количества страниц с продуктами
def get_cnt_pages_list():
    response = RequestWrapper.post_filters(url='https://goldapple.ru/front/api/catalog/filters')
    response_data = response['data']['productsCount']
    return response_data

# Функция для отправки запроса к API с определенной страницей
def download_options(name_json, page=1):
    payload = PayloadBuilder().set_category(1000000003).set_page_number(page).set_filters().get_payload()
    request = RequestWrapper(payload)
    response = request.post_options(url='https://goldapple.ru/front/api/catalog/filters')
    with open(name_json, 'w') as f:
        json.dump(response, f)


def delete_options(name_json):
    if os.path.exists(name_json):
        os.remove(name_json)
