import os
from PIL import Image

class ImageProcessor:
    def __init__(self, max_file_size=10 * 1024 * 1024, min_width=700, min_height=900):
        self.max_file_size = max_file_size
        self.min_width = min_width
        self.min_height = min_height

    def resize_image(self, img, target_width, target_height):
        """Функция для изменения размера изображения с сохранением пропорций."""
        img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
        return img

    def compress_image(self, img, max_size, quality):
        """Функция для сжатия изображения до нужного размера."""
        img.save("temp_image.webp", quality=quality)
        while os.path.getsize("temp_image.webp") > max_size:
            quality -= 5  # Понижаем качество сжатия
            img.save("temp_image.webp", quality=quality)
        return img

    def calculate_new_dimensions(self, width, height):
        """Вычисляет новые размеры изображения с сохранением пропорций."""
        # Вычисляем коэффициент масштабирования
        scale_factor = max(self.min_width / width, self.min_height / height)

        # Вычисляем новые размеры
        new_width = max(self.min_width, int(width * scale_factor))
        new_height = max(self.min_height, int(height * scale_factor))

        return new_width, new_height

    def check_and_change_image_size(self, img):
        width, height = img.size
        # Если изображение не соответствует минимальным размерам, увеличиваем его
        if width < self.min_width or height < self.min_height:
            # Пропорциональное увеличение
            new_width, new_height = self.calculate_new_dimensions(width, height)
            img = self.resize_image(img, new_width, new_height)
        return img

    def check_and_change_image_memory_size(self, img, img_path):
        change = False
        # Если размер файла больше 10 МБ, сжимаем изображение
        if os.path.getsize(img_path) > self.max_file_size:
            print(f"Снижаю качество изображения {img_path}")
            img = self.compress_image(img, self.max_file_size, 85)  # Начнем с 85% качества
            change = True
        return img, change
