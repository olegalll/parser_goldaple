from PIL import Image
import io
import paramiko
import os

from config import server, username, password

import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Добавляем параметр delay=True
file_handler = RotatingFileHandler('app.log', maxBytes=1024*1024*5, backupCount=5, encoding='utf-8', delay=True)
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

console_handler = logging.StreamHandler()
console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(console_formatter)
logger.addHandler(console_handler)

# Настройка логгирования с добавлением времени события
logging.basicConfig(filename='app.log', filemode='a', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO, encoding='utf-8')

def is_folder_processed(folder_id):
    with open('app.log', 'r', encoding='utf-8') as log_file:
        log_contents = log_file.read()
        # Проверяем, содержится ли идентификатор папки в логе
        if folder_id in log_contents:
            return True
    return False

def is_image_processed(image_path):
    with open('app.log', 'r', encoding='utf-8') as log_file:
        for line in log_file:
            if image_path in line and "было изменено" in line:
                return True
    return False

def resize_image_if_needed(image_path, sftp):
    # Проверяем, было ли изображение изменено ранее
    if is_image_processed(image_path):
        logger.info(f"Изображение {image_path} было изменено ранее.")
        return  # Пропускаем обработку, если изображение уже было изменено

    try:
        with sftp.open(image_path, 'rb') as file:
            img_data = file.read()
        img = Image.open(io.BytesIO(img_data))

        if img.width < 1000 or img.height < 1000:
            new_width, new_height = calculate_new_dimensions(img.width, img.height)
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

            img_byte_arr = io.BytesIO()
            img_format = determine_image_format(image_path)
            img.save(img_byte_arr, format=img_format)
            img_byte_arr = img_byte_arr.getvalue()

            with sftp.open(image_path, 'wb') as file:
                file.write(img_byte_arr)
            logger.info(f"Изображение {image_path} было изменено.")
        else:
            logger.info(f"Изображение {image_path} было изменено и не требует изменений.")
    except Exception as e:
        logger.error(f"Ошибка при обработке изображения {image_path}: {e}")

def calculate_new_dimensions(width, height):
    if width < height:
        new_width = 1000
        new_height = int((new_width / width) * height)
    else:
        new_height = 1000
        new_width = int((new_height / height) * width)
    return new_width, new_height

def determine_image_format(image_path):
    file_extension = os.path.splitext(image_path)[1].lower()
    return {
        '.jpg': 'JPEG',
        '.jpeg': 'JPEG',
        '.png': 'PNG',
        '.gif': 'GIF',
        '.webp': 'WEBP'
    }.get(file_extension, 'PNG')  # Default to PNG if unknown

def reconnect_sftp():
    global sftp, ssh
    try:
        sftp.close()
    except Exception as e:
        logger.error(f"Ошибка при закрытии SFTP соединения: {e}")
    try:
        ssh.close()
    except Exception as e:
        logger.error(f"Ошибка при закрытии SSH соединения: {e}")
    try:
        ssh.connect(server, username=username, password=password, timeout=10)
        sftp = ssh.open_sftp()
    except Exception as e:
        logger.error(f"Ошибка при переподключении: {e}")


# Изменение вызова process_directory и is_folder_processed для использования списка обработанных папок
def process_directory(directory, sftp_param, processed_folders):
    global sftp
    try:
        for entry in sftp_param.listdir_attr(directory):
            path = f"{directory}/{entry.filename}"
            if entry.longname.startswith('d'):
                folder_id = entry.filename
                if is_folder_processed(folder_id, processed_folders):
                    logger.info(f"Папка {folder_id} уже обработана. Пропускаем...")
                    continue
                process_directory(path, sftp_param, processed_folders)
            else:
                if path.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
                    resize_image_if_needed(path, sftp_param)
    except (OSError, paramiko.ssh_exception.SSHException) as e:
        if str(e) == 'Socket is closed' or isinstance(e, paramiko.ssh_exception.SSHException):
            logger.error("Соединение было закрыто. Попытка переподключения...")
            reconnect_sftp()
            process_directory(directory, sftp)
        else:
            raise


def extract_folder_ids_from_log(log_file_path):
    folder_ids = set()
    with open(log_file_path, 'r', encoding='utf-8') as log_file:
        for line in log_file:
            parts = line.split('/')
            if len(parts) > 5:  # Убедимся, что строка содержит путь к файлу
                folder_id = parts[5]  # Идентификатор папки находится после пятого слеша
                folder_ids.add(folder_id)
    return folder_ids

def is_folder_processed(folder_id, processed_folders):
    return folder_id in processed_folders





ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(server, username=username, password=password)
logger.info("Соединение с сервером установлено.")

sftp = ssh.open_sftp()
processed_folders = extract_folder_ids_from_log('app.log')
process_directory('/var/www/html/files/images_goldapple/', sftp, processed_folders)

sftp.close()
ssh.close() 