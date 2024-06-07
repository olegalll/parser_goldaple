import sqlite3
import re

def clean_key(key):
    # Заменяем пробелы на подчеркивания
    key = key.replace(" ", "_")
    # Удаляем все символы, которые не являются буквами, цифрами или подчеркиваниями
    key = re.sub(r'\W+', '', key)
    return key


def connection():
# Создаем подключение к базе данных (файл database.db будет создан)
    connection = sqlite3.connect('database/goldapple.db')
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

def get_all_articles(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT article FROM details_products")
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

def save_details_products(connection, product_details):
    # Очищаем ключи словаря
    product_details = {clean_key(key): value for key, value in product_details.items()}

    cursor = connection.cursor()

    # Получаем текущие столбцы в таблице
    cursor.execute('PRAGMA table_info(details_products)')
    columns_in_table = [info[1] for info in cursor.fetchall()]

    # Определяем новые столбцы
    new_columns = [col for col in product_details.keys() if col not in columns_in_table]

    # Добавляем новые столбцы в таблицу
    for col in new_columns:
        try:
            cursor.execute(f'ALTER TABLE details_products ADD COLUMN {col} TEXT')
        except sqlite3.OperationalError as e:
            # print(f"Failed to add column {col} to table: {e}")
            continue

    # Подготовка данных для вставки
    placeholders = ', '.join(['?'] * len(product_details))
    columns = ', '.join(product_details.keys())
    values = tuple(product_details.values())

    # SQL запрос для вставки данных
    query = f"INSERT INTO details_products ({columns}) VALUES ({placeholders})"

    try:
        cursor.execute(query, values)
        connection.commit()
        # print("Record inserted successfully.")
    except sqlite3.Error as error:
        # print("Failed to insert data into sqlite table", error)
        pass

    finally:
        if cursor:
            cursor.close()


def create_table_details():
    connection = sqlite3.connect('database/goldapple.db')
    cursor = connection.cursor()
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS details_products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_type TEXT,
            brand TEXT,
            name TEXT,
            article TEXT,
            description_application TEXT,
            country TEXT,
            colors TEXT,
            compound TEXT
        )
    ''')
    connection.commit()
    connection.close()

def main():
    connection = sqlite3.connect('database/goldapple.db')

    connection.close()

if __name__ == '__main__':
    main()