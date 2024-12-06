import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import db
import json

# Устанавливаем соединение с базой данных
connection = db.connection()

images = db.get_new_links(connection)
with open('images.json', 'w', encoding='utf-8') as file:
    json.dump(images, file, ensure_ascii=False, indent=4)
print(f"Сохранил информацию о {len(images)} изображений")
