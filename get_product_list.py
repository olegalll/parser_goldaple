"""
"""

import os
import pandas as pd
import logging
import time
from tqdm import tqdm



from api_requests import get_cnt_pages_list, download_list
import db

# Настройка логирования
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Функция для получения содержимого списка продуктов
def get_content_list(list, connection):
    data = list
    
    products_list = []
    for product in data['data']['products']:
        # courier, store_pickup = get_item(product['itemId']) # Закомментировал, так отказались из-за скорости работы
        courier, store_pickup = None, None
        product_info = {
            'itemId': product['itemId'],
            'mainVariantItemId': product['mainVariantItemId'],
            'brand': product['brand'],
            'name': product['name'],
            'actual_amount': product['price']['actual']['amount'] if product['price']['actual'] is not None else None,
            'old_amount': product['price']['old']['amount'] if product['price']['old'] is not None else None,
            'link': f'https://goldapple.ru{product["url"]}',
            'courier': courier,
            'store_pickup': store_pickup, # TODO: удалить
            'image_link': None
        }
        details = db.get_details(product['itemId'], connection)
        if details is not None:
            product_info.update(details)
        products_list.append(product_info)
        

    return products_list


def save_df_to_excel(df):
    # Проверяем, существует ли папка 'result'
    if not os.path.exists('result'):
        # Если нет, создаем ее
        os.makedirs('result')

    # Теперь мы можем безопасно сохранить наш DataFrame в файл Excel
    df.to_excel('result/products.xlsx', index=False)


def main():
    connection = db.connection()

    # Получаем количество страниц с продуктами
    total_pages = get_cnt_pages_list() // 24
    # total_pages = 5

    # Создаем пустой DataFrame
    df = pd.DataFrame()

    start_time = time.time()  # Запоминаем время начала выполнения цикла
    for page_num in tqdm(range(1, total_pages + 1)): 
        logging.info(f'Start processing page {page_num}')
        list = download_list(page_num)
        time.sleep(1)
        products_list = get_content_list(list, connection)
        df = pd.concat([df, pd.DataFrame(products_list)], ignore_index=True)
        df = df.drop_duplicates(subset=['itemId'], keep='last')
        logging.info(f'Finished processing page {page_num}')

    end_time = time.time()  # Запоминаем время окончания выполнения цикла
    logging.info(f'Total time for processing {total_pages} pages: {end_time - start_time} seconds')


    # Вызываем функцию для сохранения DataFrame в файл Excel
    save_df_to_excel(df)

    db.close_connection(connection)



if __name__ == '__main__':
    main()

#  pyinstaller .\get_product_list.py --onefile
