import sqlite3


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
                itemId INTEGER PRIMARY KEY,
                mainVariantItemId INTEGER,
                brand TEXT,
                name TEXT,
                actual_amount INTEGER,
                old_amount INTEGER,
                link TEXT
            )
        ''')
        print("Таблица 'list_products' создана.")


def save_list_products(connection, products_list):
    cursor = connection.cursor()
    for product in products_list:
        cursor.execute('''
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
        ''', product)
    connection.commit()
