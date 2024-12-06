import os
import json
from tqdm import tqdm
from PIL import Image
from image_processor import ImageProcessor

def process_images(processor, images, processed_results, image_path, results_file_path):
    """Процесс обработки изображений."""
    results = []
    pbar = tqdm(total=len(images), ncols=90)

    for idx, image in enumerate(images):
        pbar.update()
        img_path = f'{image_path}{image["new_link"].split("images_goldapple")[-1]}'

        # Проверяем, было ли изображение уже обработано
        if image['new_link'] in processed_results:
            continue  # Пропускаем изображение, если оно уже было обработано

        # Создаем запись для текущего изображения
        result = {
            'new_link': image["new_link"],
            'image_path': img_path,
            'found': False,
            'changed': False
        }

        # Проверяем, существует ли файл
        if os.path.isfile(img_path):
            result['found'] = True
            try:
                with Image.open(img_path) as img:
                    # Проверяем размеры изображения
                    width, height = img.size

                    # Сохраняем исходные размеры для сравнения
                    original_width, original_height = width, height
                    original_file_size = os.path.getsize(img_path)

                    # Если изображение не соответствует минимальным размерам, увеличиваем его
                    if width < processor.min_width or height < processor.min_height:
                        # Пропорциональное увеличение
                        img = processor.check_and_change_image_size(img)
                        width, height = img.size  # обновляем размеры после изменения
                        result['changed'] = True

                    # Если размер файла больше 10 МБ, сжимаем изображение
                    if os.path.getsize(img_path) > processor.max_file_size:
                        print(f"Снижаю качество изображения {img_path}")
                        img = processor.compress_image(img, processor.max_file_size, 85)  # Начнем с 85% качества
                        result['changed'] = True

                    # Проверяем, изменилось ли изображение
                    if result['changed']:
                        # Сохраняем изображение только если оно изменилось
                        img.save(img_path)
                        print(f"Изображение сохранено: {img_path}")

            # except ValueError as e:
            finally:
                pass
                # print(f"Ошибка при обработке изображения {img_path}: {e}")

        else:
            result['found'] = False
            # print(f"Изображение не найдено: {img_path}")

        # Добавляем результат в список
        results.append(result)

        # Сохраняем результаты каждые 100 изображений
        if (idx + 1) % 100 == 0 or (idx + 1) == len(images):
            with open(results_file_path, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=4)

    pbar.close()
    return results

def load_processed_results(results_file_path):
    """Загружаем уже обработанные результаты из файла, если он существует."""
    if os.path.exists(results_file_path):
        with open(results_file_path, 'r', encoding='utf-8') as f:
            processed_results = json.load(f)
        return {result['new_link']: result for result in processed_results}
    return {}

def load_images(json_file_path):
    """Загружаем данные из JSON файла."""
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Файл {json_file_path} не найден.")
        return []

# Пример использования класса и функции
if __name__ == "__main__":
    # image_path = '/var/www/html/files/images_goldapple'
    image_path = os.path.join(os.path.dirname(__file__), '../images_goldapple')

    json_file_path = os.path.join(os.path.dirname(__file__), 'images.json')
    results_file_path = os.path.join(os.path.dirname(__file__), 'image_processing_results.json')

    processed_results = load_processed_results(results_file_path)
    images = load_images(json_file_path)

    processor = ImageProcessor()
    process_images(processor, images, processed_results, image_path, results_file_path)
