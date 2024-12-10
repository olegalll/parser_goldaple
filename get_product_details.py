import re
import os
import time
import alarm_bot
import glob
import json
import asyncio
import pandas as pd
import db
from tqdm import tqdm
from api_requests import get_details_json
from upload_images_to_server import upload_images_to_server

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

def get_colors(product_description):
    colors = []
    articles = []
    urls = []
    for value in product_description['variants']:
        color = value['attributesValue'].get('colors', None)
        article = value.get('itemId', product_description.get('itemId'))
        url = value.get('url', product_description.get('url'))
        
        colors.append(color)
        articles.append(article)
        urls.append(url)

    return colors, articles, urls


def get_product_card(product_description):
    product_type = product_description['productType']
    brand = product_description['brand']
    name = product_description['name']

    return product_type, brand, name



# Функция для получения содержимого списка продуктов
def save_content_details(connection, details_json,  link):
    product_details = []
    
    # Путь к файлу, в который будет сохранен JSON
    file_path = 'jsons/details.json'
    
    # Сохранение details_json в файл
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(details_json, file, ensure_ascii=False, indent=4)

    if 'productCard' in details_json:
        data_json = details_json['productCard']['data']

        # # Получаем данные о продукте
        colors, articles, urls = get_colors(data_json)  # Цвета
        product_type, brand, name = get_product_card(data_json) # Название модели 1, бренд и название модели 2
        item_id, description_application, characteristics = get_description(data_json['productDescription']) # Артикул, описание+применение и характеристики
        country = get_country(data_json['productDescription']) # Страна происхождения
        compound = get_compound(data_json['productDescription'])  # Состав
        
        product_details_list = []
        
        for article, color, url in zip(articles, colors, urls):
            
            product_details = {
                'article': article,
                'item_id': item_id,
                'link': 'https://goldapple.ru'+url,  # Ссылка на продукт
                'product_type': product_type,
                'brand': brand,
                'name': name,
                'description_application': description_application,
                'country': country,
                'color': color,  # Добавляем цвет как элемент списка
                'compound': compound
            }
        
            # Добавляем каждую характеристику в product_details
            for characteristic in characteristics:
                key = characteristic.get('key')
                value = characteristic.get('value')
                if key and value:
                    product_details[key] = value
        
            product_details_list.append(product_details)
        db.save_details_products(connection, product_details_list)
        # Получаем ссылки на изображения
        save_image_old_links(connection, details_json, articles)
    else:
        print(f"Key 'productCard' not found in JSON data for link: {link}")



def save_image_old_links(connection, details_json, articles):
    images_list = get_image_old_links(details_json, articles)

    db.save_images_old_links(connection, images_list)


def get_image_old_links(details_json, articles):
    images_links = []
    try:
        for article in articles:

            product_description = [
                variant for variant in details_json['productCard']['data']['variants']
                if variant.get('itemId') == article
            ]
            
            
            for variant in product_description:
                for url_dict in variant['imageUrls']:
                    images_links.append({
                        'article': article,
                        'old_link': url_dict["url"].replace("${format}", "webp").replace("${screen}", "fullhd")
                    })
    except KeyError:
        return []
    
    return images_links

def parsing_product_details(links_list, connection):
    for link in tqdm(links_list, ncols=90):
        time.sleep(1)
        
        # Получаем JSON с информацией о продукте
        details_json = get_details_json(link)
        if not details_json:
            continue
        # Получаем данные о продукте 
        save_content_details(connection, details_json, link)

def remove_existing_articles(links_list, db_articles):
    # Фильтрация списка, удаляя элементы, присутствующие в 'db_articles'
    filtered_links = [link for link in links_list if link not in db_articles]
    return filtered_links

def get_links(exists_articles=None):
    # Получить список всех Excel файлов в директории
    all_files = glob.glob("./result/*.xlsx")
    links_articles = {}  # Список для хранения ссылок

    for filename in all_files:
        # Игнорировать файлы, начинающиеся на "~$"
        if os.path.basename(filename).startswith("~$") or os.path.basename(filename).startswith(".~"):
            continue

        try:
            df = pd.read_excel(filename)
            # Добавление ссылок в список, игнорируя NaN значения

            for index, row in df.iterrows():
                link = row["link_x"]
                article = row["article"]
                if exists_articles and article in exists_articles:
                    continue
                elif article not in links_articles:
                    links_articles[article] = link
        except Exception as e:
            print(f"Error reading file {filename}: {e}")

    links = []
    articles = []
    for key, val in links_articles.items():
        if val not in links:
            links.append(val)
        if key not in articles:
            articles.append(key)
    links = list(set(links))
    articles = list(set(articles))

    return links, articles

def main():
    connection = db.connection()
    # db.delete_rows_with_null_new_link(connection)

    # Если нужно пересобрать заново все детали закомментировать иначе будет поиск только для новых артикулов, которых нет в базе
    exists_articles_with_details_and_images = db.get_exists_article_details(connection)
    print(f"Exists articles {len(exists_articles_with_details_and_images)}")

    links_list, articles_list = get_links(exists_articles_with_details_and_images)
    print(f"New links {len(links_list)}")
    print(f"New articles {len(articles_list)}")

    parsing_product_details(links_list, connection)
    # asyncio.run(upload_images_to_server(connection, articles_list))

    # Закрываем коннект к базе данных
    db.close_connection(connection)
    # asyncio.run(alarm_bot.send_message())


if __name__ == '__main__':
    main()