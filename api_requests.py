import os

# Импортируем данные для запросов к API
from request_wrapper import RequestWrapper
from payload_builder import PayloadBuilder

# Функция для получения количества страниц с продуктами
def get_cnt_pages_list(category_id, amount_min=22, amount_max=4053):
    payload = PayloadBuilder().set_category(category_id).set_filters(amount_min, amount_max).get_payload()
    wrapper = RequestWrapper(payload)
    response = wrapper.post_filters()
    response_data = response['data']['productsCount']
    return response_data

# Функция для получения списка продуктов
def download_list(category_id, page=1, amount_min=22, amount_max=4053):
    payload = PayloadBuilder().set_category(category_id).set_page_number(page).set_filters(amount_min, amount_max).get_payload()
    request = RequestWrapper(payload)
    response = request.post_options()
    return response

# Функция для получения даты доставки
def get_item(item_id: str):
    payload = PayloadBuilder().set_item(item_id).get_payload()
    request = RequestWrapper(payload)
    response = request.post_item()
    response_dict = {option['name']: option['dateInfo'] for option in response['data']['options']}

    courier = response_dict.get('курьер', None)
    store_pickup = response_dict.get('самовывоз из магазина', None)

    return courier, store_pickup

def get_details_json(url):
    request = RequestWrapper()
    
    response = request.get_details(url)
    
    # # Сохраняем ответ в файл JSON
    # with open('jsons/detail_json.json', 'w', encoding='utf-8') as f:
    #     json.dump(response, f, indent=4, ensure_ascii=False)
    return response


def delete_options(name_json):
    if os.path.exists(name_json):
        os.remove(name_json)


if __name__ == '__main__':
    item = get_item('19000003031')
    print(item)
    print('Done')