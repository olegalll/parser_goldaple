"""
Получили артикул и описание. Далее нужно получить характеристики

TODO: создать базу для карточек
TODO: настроить получение картинок
TODO: настроить отправку сообщений в телеграм

"""
import time
from tqdm import tqdm
import pandas as pd
import glob
import asyncio
import json
import re
import os
import sys


import db
import alarm_bot
from api_requests import get_detials_json
from request_wrapper import RequestWrapper

def find_item(details_json_getted, text):
    # Пытаемся найти элемент с заданным текстом в details_json_getted
    try:
        item = next(x for x in details_json_getted if x.get('text') == text)
    except StopIteration:
        # Если такой элемент не найден, выводим сообщение об ошибке и возвращаем None
        # print(f"{text} не найдено")
        return None

    return item

def get_country(product_description):
    item = find_item(product_description, "Дополнительная информация")
    if item is None:
        return None

    # Извлекаем подстроку 'content' из найденного элемента
    add_info = item.get('content', '')

    # Использование регулярного выражения для поиска подстроки
    match = re.search(r'страна происхождения<br>(.*?)<br><br>', add_info)

    if match:
        country = match.group(1)
        return country
    else:
        # print("Страна происхождения не найдена")
        return None

def get_description(product_description):
    item = find_item(product_description, "описание")
    if item is None:
        return None

    # Извлекаем подстроку 'subtitle' из найденного элемента
    add_info_article = item.get('subtitle', '')
    # Удаляем 'артикул: ' из строки, чтобы получить только номер артикула
    article = add_info_article.replace('артикул: ', '')

    # Извлекаем подстроку 'content' из найденного элемента
    add_info_description = item.get('content', '')
    # Заменяем теги <br> и символы \n на символы новой строки
    description = add_info_description.replace('<br>', '\n').replace('\\n', '\n')
    application = get_application(product_description)
    description_application = description + '\n' + application

    # Извлекаем подстроку 'attributes' из найденного элемента
    characteristics = item.get('attributes', [])

    # Возвращаем номер артикула и описание
    return article, description_application, characteristics


def get_application(product_description):
    item = find_item(product_description, "применение")
    if item is None:
        return ''
    
    # Извлекаем подстроку 'content' из найденного элемента
    add_info_application = item.get('content', '')
    # Заменяем теги <br> и символы \n на символы новой строки
    application = add_info_application.replace('<br>', '\n').replace('\\n', '\n')
    return application

def get_compound(product_description):
    item = find_item(product_description, "состав")
    if item is None:
        return None
    
    # Извлекаем подстроку 'content' из найденного элемента
    add_info_compound = item.get('content', '')
    # Заменяем теги <br> и символы \n на символы новой строки
    compound = add_info_compound.replace('<br>', '\n').replace('\\n', '\n')
    return compound

def get_product_card(product_description):
    product_type = product_description['productType']
    brand = product_description['brand']
    name = product_description['name']

    return product_type, brand, name

def get_colors(product_description):
    if 'colors' in product_description:
        product_description = product_description['colors']['options']
        colors = []
        for color in product_description:
            colors.append(color['text'])
        colors = ', '.join(colors)
        return colors
    else:
        return None



# Функция для получения содержимого списка продуктов
def get_content_details(details_json):
    product_details = []
    try:
        data_json = details_json['productCard']['data']
    except KeyError:
        # print('get_content_details: Не удалось получить данные о продукте')
        data_json = {}

    # Получаем данные о продукте
    product_type, brand, name = get_product_card(data_json) # Название модели 1, бренд и название модели 2
    article, description_application, characteristics = get_description(data_json['productDescription']) # Артикул, описание+применение и характеристики
    country = get_country(data_json['productDescription']) # Страна происхождения
    colors = get_colors(data_json['attributes']) # Цвета
    compound = get_compound(data_json['productDescription']) # Состав

    product_details = {
        'product_type': product_type,
        'brand': brand,
        'name': name,
        'article': article,
        'description_application': description_application,
        'country': country,
        'colors': colors,
        'compound': compound
    }
    # Добавляем каждую характеристику в product_details
    for characteristic in characteristics:
        key = characteristic.get('key')
        value = characteristic.get('value')
        if key and value:
            product_details[key] = value
    return product_details

def parsing_product_details(links, connection):
    start_time = time.time()  # Запоминаем время начала выполнения цикла
    

    for link in tqdm(links):
        # Получаем JSON с информацией о продукте
        details_json = get_detials_json(link)
        
        product_details = get_content_details(details_json)
        # print(product_details)
        db.save_details_products(connection, product_details)

        #TODO: Написать функцию db.save_details_products(connection, product_details)
        #TODO: Написать функцию get_link_images(product_details)
        #TODO: Написать функцию save_images(product_details)




def remove_existing_articles(links_df, db_articles):
    # Удаление строк, в которых 'itemId' присутствует в 'db_articles'
    return links_df[~links_df['itemId'].isin(db_articles)]

def get_links():
    # Получить список всех Excel файлов в директории
    all_files = glob.glob("./result/*.xlsx")
    links = set()
    itemIds = set()

    for filename in all_files:
        # Игнорировать файлы, начинающиеся на "~$"
        if os.path.basename(filename).startswith("~$"):
            continue

        try:
            df = pd.read_excel(filename)
            links.update(df["link"].dropna().unique())
            itemIds.update(df["itemId"].dropna().unique())
        except Exception as e:
            print(f"Error reading file {filename}: {e}")

    # Преобразование списка в DataFrame
    links_df = pd.DataFrame(list(zip(links, itemIds)), columns=['link', 'itemId'])

    # Преобразование 'itemId' в строку
    links_df['itemId'] = links_df['itemId'].astype(str)

    return links_df

def main():
    connection = db.connection()
    
    links_df = get_links()
    db_articles = db.get_all_articles(connection)
    
    links_df = remove_existing_articles(links_df, db_articles)
    
    # Получение списка ссылок после удаления существующих статей
    links = links_df['link']
    
    parsing_product_details(links, connection)

    # Закрываем коннект к базе данных
    db.close_connection(connection)
    asyncio.run(alarm_bot.send_message())


if __name__ == '__main__':
    main()