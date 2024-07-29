# PARSER_GOLDAPPLE
test 

### Требования
Python 3.8+
Установленные библиотеки:
requests
beautifulsoup4
pandas

### Установка
Клонируйте репозиторий:
```
git clone https://github.com/ErrrMAK/parser_goldaple.git
cd PARSER_GOLDAPLE
```

Создайте и активируйте виртуальное окружение:
```
python -m venv venv
venv\Scripts\activate
```

Установите зависимости:
```
pip install -r requirements.txt
```

### Запуск
Убедитесь, что вы настроили файл config.py исходя из config.py.dist.
```
python get_product_list.py - парсинг ассортимента товаров
python get_product_details.py - парсинг данных из карточки товара
python upload_images_to_server.py - вспомогательный скрипт для сохранения картинок на сервер
```

