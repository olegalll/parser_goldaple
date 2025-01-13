import os
import time
import logging
import warnings
import pandas as pd
import db
from tqdm import tqdm
from api_requests import get_cnt_pages_list, download_list

warnings.filterwarnings("ignore", category=FutureWarning)
# Настройка логирования
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Функция для получения содержимого списка продуктов
def get_content_list(list, category_id = None):
    data = list
    if not data:
        logging.error('get_content_list: No data received')
        return []
    products_list = []
    for product in data['data']['products']:
        # courier, store_pickup = get_item(product['itemId']) # Закомментировал, так отказались из-за скорости работы
        courier, store_pickup = None, None
        in_stock = product['inStock']
        if not in_stock:
            logging.info(f"NOT IN STOCK: https://goldapple.ru{product['url']} ({product['itemId']})")
            continue
        product_info = {
            'article': product['itemId'],
            'item_id': product['mainVariantItemId'],
            'brand': product['brand'],
            'name': product['name'],
            'actual_amount': product['price']['actual']['amount'] if product['price']['actual'] is not None else None,
            'old_amount': product['price']['old']['amount'] if product['price']['old'] is not None else None,
            'link': f'https://goldapple.ru{product["url"]}',
            'courier': courier,
            'store_pickup': store_pickup, # TODO: удалить,
            'category_id': {
                "id": category["id"],
                "название": category["название"],
                "category_id": category["category_id"]
            }
        }
        products_list.append(product_info)
        # logging.info(f'get_content_list: {product_info["article"]} - {product_info["name"]} - {product_info["actual_amount"]} - {product_info["old_amount"]} - {product_info["link"]}')

    return products_list

def clean_for_excel(text):
    if not isinstance(text, str):
        return text
    return ''.join(char for char in text if char == '\t' or char == '\n' or char == '\r' or 0x20 <= ord(char) <= 0x7E or ord(char) > 0x7F)

def save_df_to_excel(path_xlsx, df):
    # Проверяем, существует ли папка 'result'
    if not os.path.exists('result'):
        # Если нет, создаем ее
        os.makedirs('result')

    # Очищаем DataFrame от недопустимых символов
    # for col in df.columns:
    #     if df[col].dtype == object:  # Если столбец содержит строки
    #         df[col] = df[col].apply(clean_for_excel)

    # Максимальное количество гиперссылок на лист Excel
    MAX_URLS = 65530
    url_count = 0  # Счётчик гиперссылок

    # Очищаем строки и обрабатываем гиперссылки
    for col in df.columns:
        if df[col].dtype == object:  # Если столбец содержит строки
            new_column = []
            for value in df[col]:
                # Если это строка, проверяем, является ли она ссылкой
                if isinstance(value, str) and (value.startswith("http://") or value.startswith("https://")):
                    url_count += 1
                    if url_count > MAX_URLS:
                        # Преобразуем ссылки в текст после превышения лимита
                        new_column.append(f"'{value}")
                    else:
                        new_column.append(value)
                else:
                    # Очищаем обычные строки
                    new_column.append(clean_for_excel(value))
            # Обновляем столбец
            df[col] = new_column

    # Теперь мы можем безопасно сохранить наш DataFrame в файл Excel
    df.to_excel(path_xlsx, index=False)


def main(category):
    category_id = category["category_id"]
    connection = db.connection()
    
    # При достижении 500й страницы сайт перестает отдавать товары. Поэтому парсим отсортированный по цене список с заданными динамическими лимитами.
    # Минимальная и максимальная цена по-умолчанию
    amount_min = category.get("amount_min", 22)
    amount_max = category.get("amount_max", 4053)
    # Получаем количество страниц с продуктами всего
    total_items = get_cnt_pages_list(category, amount_min, amount_max)
    print(f"\nCategory: {category}\n{total_items}")
    total_pages = total_items // 24

    df = pd.DataFrame()
    df_list = []

    start_time = time.time()  # Запоминаем время начала выполнения цикла
    page_num = 1

    # for _ in tqdm(range(1, 2 + 1), ncols=90): 
    for _ in tqdm(range(page_num, total_pages + 1), ncols=90):
        
        logging.info(f'Start processing page {page_num}')
        list = download_list(category, page_num, amount_min, amount_max)
        if not list:
            logging.error(f'No data received for page {page_num}')
        time.sleep(1)
        products_list = get_content_list(list, category_id)
        if not products_list:
            logging.error(f'No products received for page {page_num}')
        df_list.append(pd.DataFrame(products_list))
        
        page_num += 1
        # Изменяем минимальную цену для следующей страницы
        if page_num % 500 == 0 and products_list:
            amount_min = products_list[-1]['actual_amount']  # Обновляем минимальную цену
            page_num = 1

    # Фильтруем пустые или состоящие только из NaN DataFrame из df_list
    df_list = [df for df in df_list if not df.empty and not df.isna().all().all()]
    # Объединяем все оставшиеся DataFrame в один
    df = pd.concat(df_list, ignore_index=True).drop_duplicates(subset=['article'], keep='last')

    # Получаем данные из базы данных
    details_columns, details_data = db.get_details_and_new_link_by_article(connection)
    details = pd.DataFrame(details_data, columns=details_columns)
    details['article'] = details['article'].astype(str)
    # Объединяем products_data_df и details
    products_data_df = pd.merge(df, details, on='article', how='left')

    end_time = time.time()  # Запоминаем время окончания выполнения цикла
    logging.info(f'Total time for processing {total_pages} pages: {end_time - start_time} seconds')

    db.close_connection(connection)
    return products_data_df

# Хардкод TODO: сделать по-красоте... когда-нибудь
categories = [
    {"id": 3, "название": "Волосы", "category_id": 1000000006},
    {"id": 4, "название": "Азиатская косметика", "category_id": 1000000010, "amount_min": 342, "amount_max": 4278, "original_link": "https://goldapple.ru/azija?calculatedprices=342-4278"},
    {"id": 5, "название": "Для дома", "category_id": 1000008202, "amount_min": 377, "amount_max": 4052, "special_filters":
        [{
            "values": [1000023411, 1000023412, 1000142833, 1000142836, 1000024638, 1000023413, 1000004439, 1000142838, 1000142878, 1000142885, 1000142890, 1000142904],
            "id": "63568a97bf461b4b2bde3b1b",
            "type": "categoryType",
            "name": "Categories",
            "key": "categories"
        },],
     "original_link": "https://goldapple.ru/dlja-doma?calculatedprices=377-4052&categories=1000023411,1000023412,1000142833,1000142836,1000024638,1000023413,1000004439,1000142838,1000142878,1000142885,1000142890,1000142904"
     },
    {"id": 6, "название": "Ногти", "category_id": 1000000021, "amount_min": 159, "amount_max": 4084, "original_link": "https://goldapple.ru/makijazh/nogti?calculatedprices=159-4084"},
    {"id": 7, "название": "Натуральная косметика", "category_id": 1000000012, "amount_min": 252, "amount_max": 4114, "original_link": "https://goldapple.ru/organika?calculatedprices=252-4114"},
    {"id": 8, "название": "Спортивное питание", "category_id": 1000134381, "amount_min": 262, "amount_max": 3955, "original_link": "https://goldapple.ru/figura-mechty/sportivnoe-pitanie?calculatedprices=262-3955"},
    {"id": 9, "название": "Уход для тела", "category_id": 1000134371, "amount_min": 268, "amount_max": 3985, "original_link": "https://goldapple.ru/figura-mechty/uhod-dlja-tela?calculatedprices=268-3985"},
    {"id": 1, "название": "Красота", "category_id": 1000000003},
    {"id": 2, "название": "Уход", "category_id": 1000000004},
]

if __name__ == '__main__':
    name_path = input('Введите название будущей таблицы и нажмите ENTER \n')
    path_xlsx = f'result/{name_path}.xlsx'
    combined_df = pd.DataFrame()
    n=0
    for category in categories:
        print(f'Спарсено категорий {n} из {len(categories)}')
        n+=1
        category_id = category['category_id']
        category_df = main(category)
        combined_df = pd.concat([combined_df, category_df], ignore_index=True)
    print('Сохранение данных в файл...')
    # Удаляем дубликаты
    combined_df = combined_df.drop_duplicates(subset=['article'], keep='last')
    
    save_df_to_excel(path_xlsx, combined_df)

    input('Данные сохранены в файл. Нажмите ENTER для выхода')

#  pyinstaller .\get_product_list.py --onefile
