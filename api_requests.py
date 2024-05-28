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


def delete_options(name_json):
    if os.path.exists(name_json):
        os.remove(name_json)
