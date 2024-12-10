import os
import re
import sqlite3
import pandas as pd

def clean_key(key):
    # Заменяем пробелы на подчеркивания
    key = key.replace(" ", "_")
    # Удаляем все символы, которые не являются буквами, цифрами или подчеркиваниями
    key = re.sub(r'\W+', '', key)
    return key

def connection():
# Создаем подключение к базе данных (файл database.db будет создан)
    db_path = os.path.join(os.path.dirname(__file__), 'database', 'goldapple.db')
    connection = sqlite3.connect(db_path)
    return connection

def close_connection(connection):  
    connection.close()

def check_table_list_products(connection):
    cursor = connection.cursor()
    
    # Проверка и создание таблицы
    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='list_products'")
    if not cursor.fetchone():
        cursor.execute(f'''
            CREATE TABLE list_products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                itemId INTEGER,
                mainVariantItemId INTEGER,
                brand TEXT,
                name TEXT,
                actual_amount INTEGER,
                old_amount INTEGER,
                link TEXT
            )
        ''')
        print("Таблица 'list_products' создана.")

def create_table_details(connection):
    cursor = connection.cursor()
    
    cursor.execute(f'''
        CREATE TABLE details_products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            article INTEGER,
            item_id INTEGER,
            link TEXT,
            product_type TEXT,
            brand TEXT,
            name TEXT,
            description_application TEXT,
            country TEXT,
            color TEXT, 
            compound TEXT
        )
    ''')
    print("Таблица 'details_products' создана.")

def get_all_links(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT link FROM details_products")
    data = cursor.fetchall()
    return [item[0] for item in data]

def get_details(item_id, connection):
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM details_products WHERE article={item_id}")
    row = cursor.fetchone()
    
    if row is None:
        return None

    # Получить имена столбцов из курсора
    column_names = [column[0] for column in cursor.description]

    # Создать словарь, где ключи - это имена столбцов, а значения - это значения из строки
    details = dict(zip(column_names, row))

    return details


def get_details_and_new_link_by_article(connection):
    cursor = connection.cursor()
    query = """
        SELECT 
        GROUP_CONCAT(i.new_link, ';') as images,
            d.*
        FROM details_products d
        LEFT JOIN images i
            ON d.article = i.article
        GROUP BY d.article
        """
    try:
        cursor.execute(query)
        result = cursor.fetchall()  # Получаем все строки данных
        headers = [column[0] for column in cursor.description]  # Получаем заголовки столбцов
        if result is None:
            return [], []  # Возвращаем пустые списки, если результат запроса None
        else:
            return headers, [list(row) for row in result]  # Возвращаем заголовки и данные
    except sqlite3.Error as e:
        print(f"Произошла ошибка при получении данных: {e}")
        return [], []  # Возвращаем пустые списки в случае ошибки

def save_list_products(connection, products_list):
    cursor = connection.cursor()
    cursor.executemany('''
        INSERT INTO list_products (
                    itemId,
                    mainVariantItemId, 
                    brand, 
                    name, 
                    actual_amount, 
                    old_amount, 
                    link)
        VALUES (
                    :itemId,
                    :mainVariantItemId, 
                    :brand, 
                    :name, 
                    :actual_amount, 
                    :old_amount, 
                    :link)
    ''', products_list)
    connection.commit()


def get_link(item_id, connection):
    cursor = connection.cursor()
    cursor.execute(f"SELECT link FROM list_products WHERE itemId={item_id}")
    return cursor.fetchone()[0]

def save_details_products(connection, products_list):
    # Создаем курсор для выполнения операций с базой данных
    cursor = connection.cursor()

    # Итерируемся по списку продуктов
    for product_details in products_list:
        # Очищаем ключи в деталях продукта
        cleaned_product_details = {clean_key(key): value for key, value in product_details.items()}

        # Получаем информацию о колонках в таблице details_products
        cursor.execute('PRAGMA table_info(details_products)')
        columns_in_table = [info[1] for info in cursor.fetchall()]

        # Определяем, какие колонки нужно добавить в таблицу
        new_columns = [col for col in cleaned_product_details.keys() if col not in columns_in_table]

        # Добавляем новые колонки в таблицу, если они есть
        for col in new_columns:
            try:
                cursor.execute(f'ALTER TABLE details_products ADD COLUMN {col} TEXT')
            except sqlite3.OperationalError as e:
                # Пропускаем ошибку, если колонка уже существует
                continue

        # Проверяем, предоставлен ли уникальный идентификатор 'article'
        article = cleaned_product_details.get('article')
        if article:
            # Проверяем, существует ли уже запись с таким идентификатором
            cursor.execute("SELECT COUNT(*) FROM details_products WHERE article = ?", (article,))
            exists = cursor.fetchone()[0] > 0

            if exists:
                # Обновляем существующую запись
                update_set = ', '.join([f"{key} = ?" for key in cleaned_product_details.keys()])
                values = tuple(cleaned_product_details.values()) + (article,)
                cursor.execute(f"UPDATE details_products SET {update_set} WHERE article = ?", values)
            else:
                # Добавляем новую запись, если она не существует
                placeholders = ', '.join(['?'] * len(cleaned_product_details))
                columns = ', '.join(cleaned_product_details.keys())
                values = tuple(cleaned_product_details.values())
                query = f"INSERT INTO details_products ({columns}) VALUES ({placeholders})"
                cursor.execute(query, values)
        else:
            # Выводим ошибку, если уникальный идентификатор не найден
            print("Error: Unique identifier 'article' not found in product details.")

        # Фиксируем изменения в базе данных
        connection.commit()

    # Закрываем курсор
    cursor.close()


def get_images_by_id(connection, article):
    cursor = connection.cursor()
    query = '''
    SELECT *
    FROM images
    WHERE article = ?
    '''
    try:
        cursor.execute(query, (article,))
        data = cursor.fetchone()
    except sqlite3.Error as e:
        print(f"Произошла ошибка при получении данных: {e}")
        data = None  # Устанавливаем data в None в случае ошибки

    return data

def delete_duplicates_images(connection):
    cursor = connection.cursor()
    cursor.execute('''
    -- Найти все дубликаты по полям article и old_link
        WITH duplicates AS (
            SELECT article, old_link
            FROM images
            GROUP BY article, old_link
            HAVING COUNT(*) > 1
        )
    -- Удалить дубликаты, у которых new_link is NULL
        DELETE FROM images
        WHERE (article, old_link) IN (SELECT article, old_link FROM duplicates)
        AND new_link IS NULL;
        ''')

    connection.commit()
    cursor.close()

def get_exists_article_details(connection):
    cursor = connection.cursor()
    query = """SELECT DISTINCT dp.article
                FROM details_products dp
                WHERE 
                dp.article NOT IN 
                    (SELECT DISTINCT i.article FROM images i WHERE i.new_link IS NULL) 
                AND 
                dp.article IN 
                    (SELECT DISTINCT i2.article FROM images i2 WHERE i2.new_link IS NOT NULL);"""
    try:
        cursor.execute(query)
        data = cursor.fetchall()
        data = [row[0] for row in data]
    except sqlite3.Error as e:
        print(f"Произошла ошибка при получении данных: {e}")
        data = None  # Устанавливаем data в None в случае ошибки
    cursor.close()
    return data


def check_and_create_images_table(connection):
    cursor = connection.cursor()
    # Проверяем наличие таблицы 'images'
    cursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='images' ''')
    # Если таблицы нет, count(name) вернет 0
    if cursor.fetchone()[0] == 0:
        # Создаем таблицу 'images'
        cursor.execute('''
            CREATE TABLE images (
                image_id INTEGER PRIMARY KEY,
                article INTEGER,
                old_link TEXT,
                new_link TEXT
            )
        ''')
        print("Таблица 'images' создана.")
    else:
        print("Таблица 'images' уже существует.")

def delete_images_table(connection):
    cursor = connection.cursor()
    # Проверяем наличие таблицы 'images'
    cursor.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='images'")
    if cursor.fetchone()[0] == 1:  # Если таблица существует
        # Удаляем таблицу 'images'
        cursor.execute("DROP TABLE images")
        print("Таблица 'images' удалена.")
    else:
        print("Таблица 'images' не существует.")

def delete_details_table(connection):
    cursor = connection.cursor()
    # Проверяем наличие таблицы 'images'
    cursor.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='details_products'")
    if cursor.fetchone()[0] == 1:  # Если таблица существует
        # Удаляем таблицу 'images'
        cursor.execute("DROP TABLE details_products")
        print("Таблица 'details_products' удалена.")
    else:
        print("Таблица 'details_products' не существует.")

def save_images_old_links(connection, images_list):
    cursor = connection.cursor()
    for image in images_list:

        cursor.execute("SELECT COUNT(*) FROM images WHERE article = ? AND old_link = ?", (image["article"], image["old_link"]))
        exists = cursor.fetchone()[0]

        if not exists > 0:
            cursor.execute('''
                INSERT INTO images (
                            article,
                            old_link)
                VALUES (?, ?)
            ''', (image["article"], image["old_link"]))
        # else:
        #     print(f"COUNT FIND IMAGES {exists}")
    connection.commit()


def get_cnt_images_null(connection):
    cursor = connection.cursor()
    query = """
        SELECT 
            COUNT(DISTINCT article)
        FROM images
        WHERE new_link is NULL
        """
    try:
        cursor.execute(query)
        result = cursor.fetchone()[0]  # Получаем одну строку данных
    except sqlite3.Error as e:
        print(f"get_cnt_images: {e}")
    return result

def get_old_link_articles(connection, article_list=None):
    connection.row_factory = sqlite3.Row  # Устанавливаем row_factory для соединения
    cursor = connection.cursor()
    if article_list:
        query = f"""
            SELECT DISTINCT article, old_link
            FROM images
            WHERE new_link IS NULL and article IN (
        {','.join([str(art) for art in article_list])}
        )
        """
    else:
        query = """
            SELECT DISTINCT article, old_link
            FROM images
            WHERE new_link IS NULL
        """
    try:
        cursor.execute(query)
        data = cursor.fetchall()
        print({row["article"]: dict(row) for row in data})
        data = [row["article"] for row in data]
    except sqlite3.Error as e:
        print(f"Произошла ошибка при получении данных: {e}")
        data = None  # Устанавливаем data в None в случае ошибки
    return data


def get_old_link(articles, connection):
    if not articles:
        return None
    connection.row_factory = sqlite3.Row  # Устанавливаем row_factory для соединения
    cursor = connection.cursor()

    query = f"""
        SELECT *
        FROM images
        WHERE article IN (
        {','.join([str(art) for art in articles])}
        )
    """
    try:
        cursor.execute(query)
        data = cursor.fetchall()
        data = [dict(row) for row in data] # Преобразуем каждый элемент sqlite3.Row в стандартный словарь
    except sqlite3.Error as e:
        print(f"Произошла ошибка при получении данных: {e}")
        data = None  # Устанавливаем data в None в случае ошибки
    return data

def update_image(connection, image_id, remotepaths):
    cursor = connection.cursor()
    query = """
        UPDATE images
        SET new_link=?
        WHERE image_id = ?
        """
    try:
        cursor.execute(query, (remotepaths, image_id))
    except sqlite3.Error as e:
        print(f"Произошла ошибка в update_image: {e}")

def delete_images_table(connection):
    cursor = connection.cursor()
    # Проверяем наличие таблицы 'images'
    cursor.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='images'")
    if cursor.fetchone()[0] == 1:  # Если таблица существует
        # Удаляем таблицу 'images'
        cursor.execute("DROP TABLE images")
        print("Таблица 'images' удалена.")
    else:
        print("Таблица 'images' не существует.")

def clear_details_table(connection):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM details_products")
    connection.commit() 

import sqlite3

def get_new_links(connection):
    connection.row_factory = sqlite3.Row  # Устанавливаем row_factory для соединения
    cursor = connection.cursor()
    query = """
        SELECT *
        FROM images
        WHERE new_link IS NOT NULL;
    """
    try:
        cursor.execute(query)
        data = cursor.fetchall()
        data = [dict(row) for row in data] # Преобразуем каждый элемент sqlite3.Row в стандартный словарь
    except sqlite3.Error as e:
        print(f"Произошла ошибка при получении данных: {e}")
        data = None  # Устанавливаем data в None в случае ошибки
    return data

def delete_rows_with_null_new_link(connection):
    connection.row_factory = sqlite3.Row  # Устанавливаем row_factory для соединения
    cursor = connection.cursor()
    query = """
        DELETE FROM images
        WHERE new_link IS NULL
    """
    try:
        cursor.execute(query)
        connection.commit()
        print("Строки с new_link IS NULL успешно удалены.")
    except sqlite3.Error as e:
        print(f"Произошла ошибка при удалении данных: {e}")
        connection.rollback()  # Откатываем изменения в случае ошибки

def main():
    db_path = os.path.join(os.path.dirname(__file__), 'database', 'goldapple.db')
    connection = sqlite3.connect(db_path)
    images_list = pd.read_excel('old_links6.xlsx')['article','images'].tolist()
    save_images_old_links(connection, images_list)
    connection.close()

if __name__ == '__main__':
    main()
