import os
import db
import time
import shutil
import aiohttp
import tarfile
import asyncio
import logging
import paramiko
import alarm_bot
from PIL import Image
from io import BytesIO
from tqdm import tqdm
from config import server, username, password
from change_images.image_processor import ImageProcessor

# Добавляем декоратор для измерения времени выполнения функций
def log_time_async(func):
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        result = await func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = (end_time - start_time) * 100  # Время в сотых долях секунды
        logger.info(f'{func.__name__} выполнена за {elapsed_time:.2f} сотых секунды')
        return result
    return wrapper

# Для синхронных функций аналогичный декоратор, но без async/await
def log_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = (end_time - start_time) * 100  # Время в сотых долях секунды
        logger.info(f'{func.__name__} выполнена за {elapsed_time:.2f} сотых секунды')
        return result
    return wrapper

# Настройка логгера
logging.basicConfig(encoding='utf-8', filename='images.log', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@log_time_async
async def download_image(image_url, localpath, image_processor):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(image_url) as response:
                if response.status == 200:
                    image_data = await response.read()
                    img = Image.open(BytesIO(image_data))
                    img = image_processor.check_and_change_image_size(img)
                    format = img.format if img.format else 'webp'  # Если формат не определен, используем webp по умолчанию
                    extension = f'.{format.lower()}'
                    if not os.path.splitext(localpath)[1]:  # Если в localpath нет расширения файла
                        localpath += extension  # Добавляем расширение файла в соответствии с форматом изображения
                    img.save(localpath, format, quality=100)  # Сохраняем в исходном формате
                    return extension  # Возвращаем расширение файла
                else:
                    logger.error(f'Failed to download image. HTTP status code: {response.status}')
                    return None
    except Exception as e:
        logger.error(f'Error in download_image: {e}')
        return None

@log_time_async
async def save_images(chunk, connection):
    try:
        logger.info('Starting save_images')
        images_data = db.get_old_link(chunk, connection)
        if not images_data:
            logger.info('No images to save')
            return None
        localpaths = []
        remotepaths = []
        image_processor = ImageProcessor()
        for image in images_data:
            base_localpath = f'images_goldapple/{image["article"]}/{str(image["image_id"])}'
            localpath_dir = os.path.join('images_goldapple', str(image['article']))
            os.makedirs(localpath_dir, exist_ok=True)
            extension = await download_image(image['old_link'], base_localpath, image_processor)  # Получаем расширение файла из download_image
            if extension:
                localpath = f'{base_localpath}{extension}'  # Формируем полный путь с расширением
                localpaths.append(localpath)
                remotepath = f'http://{server}/{localpath}'
                remotepaths.append(remotepath)
                logger.info(f"NEW IMAGE ID: {image['image_id']} ({remotepath})")
                db.update_image(connection, image['image_id'], remotepath)
        connection.commit()
        logger.info('Finished saving images')
        return localpaths
    except Exception as e:
        logger.error(f'Error in save_images: {e}')
        return None

@log_time
def connect_sftp_server(server, username, password):
    try:
        logger.info('Starting connect_sftp_server')
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(server, username=username, password=password)
        sftp = ssh.open_sftp()
        logger.info('Connected to SFTP server')
        return ssh, sftp
    except Exception as e:
        logger.error(f'Error in connect_sftp_server: {e}')
        return None, None

@log_time
def create_remote_directory(sftp, remote_directory):
    try:
        logger.info(f'Starting create_remote_directory for {remote_directory}')
        dirs = remote_directory.split('/')
        path = '/'
        for directory in dirs:
            if directory:
                path = os.path.join(path, directory)
                try:
                    sftp.stat(path)
                except FileNotFoundError:
                    sftp.mkdir(path)
        logger.info(f'Remote directory created: {remote_directory}')
    except Exception as e:
        logger.error(f'Error in create_remote_directory: {e}')

@log_time
def tar_files(source_folder, output_tar):
    try:
        # logger.info(f'Starting tar_files for {source_folder}')
        with tarfile.open(output_tar, "w") as tar:
            tar.add(source_folder, arcname=os.path.basename(source_folder))
        logger.info(f'Tar file created: {output_tar}')
    except Exception as e:
        logger.error(f'Error in tar_files: {e}')

@log_time
def clear_directory(directory):
    try:
        # logger.info(f'Starting clear_directory for {directory}')
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                logger.error(f'Failed to delete {file_path}. Reason: {e}')
        logger.info(f'Cleared directory: {directory}')
    except Exception as e:
        logger.error(f'Error in clear_directory: {e}')

@log_time
def upload_images(ssh, sftp, localpaths):
    try:
        logger.info('Starting upload_images')
        output_tar = 'images_goldapple.tar'
        tar_files('images_goldapple', output_tar)
        remote_tar_dir = '/var/www/html/files/'
        remote_tar = remote_tar_dir + output_tar
        create_remote_directory(sftp, remote_tar_dir)
        # Передача файла на удаленный сервер
        try:
            sftp.put(output_tar, remote_tar)
            logger.info(f"Файл {output_tar} успешно передан на сервер в {remote_tar}.")
        except Exception as e:
            logger.error(f"Ошибка при передаче файла {output_tar}: {e}")

        # Команда для распаковки и удаления архива
        untar_and_remove_command = f'tar -xf {remote_tar} -C {remote_tar_dir} && rm {remote_tar}'
        logger.info(f"Сформирована команда для выполнения: {untar_and_remove_command}")

        # Выполнение команды на удаленном сервере
        try:
            stdin, stdout, stderr = ssh.exec_command(untar_and_remove_command)
            logger.info(f"Команда выполнена на сервере: {untar_and_remove_command}")
        except Exception as e:
            logger.error(f"Ошибка выполнения команды на сервере: {e}")

        # Чтение и логгирование вывода команды
        try:
            stdout_output = stdout.read().decode()
            if stdout_output:
                logger.info(f"Вывод команды: {stdout_output}")
                pass
        except Exception as e:
            logger.error(f"Ошибка чтения stdout: {e}")

        try:
            stderr_output = stderr.read().decode()
            if stderr_output:
                logger.warning(f"Ошибки выполнения команды: {stderr_output}")
        except Exception as e:
            logger.error(f"Ошибка чтения stderr: {e}")
        logger.info("STDOUT:")
        logger.info(stdout_output)
        logger.info("STDERR:")
        logger.info(stderr_output)
        os.remove(output_tar)
        clear_directory('images_goldapple')
        logger.info('Finished upload_images')
    except Exception as e:
        logger.error(f'Error in upload_images: {e}')

@log_time
def close_sftp_server(ssh, sftp):
    try:
        logger.info('Closing SFTP and SSH connections')
        sftp.close()
        ssh.close()
    except Exception as e:
        logger.error(f'Error in close_sftp_server: {e}')


@log_time_async
async def upload_images_to_server(connection, article_list=None):
    articles = db.get_old_link_articles(connection, article_list)

    if articles is None:
        logger.error("Не могу собрать изображения")
        exit(1)
    if not articles:
        logger.error("Отсутствуют незакачанные изображения")
        exit(1)

    chunk_size = 5
    chunks = [articles[i:i + chunk_size] for i in range(0, len(articles), chunk_size)]
    pbar = tqdm(total=len(articles), ncols=90)

    retry_attempts = 3

    ssh = None
    sftp = None
    n = 0

    for chunk in chunks:
        localpaths = await save_images(chunk, connection)
        if not localpaths:
            n+=1
            print(f'No images to upload: {n}')
            # break
            continue
        for attempt in range(retry_attempts):
            try:
                ssh, sftp = connect_sftp_server(server, username, password)
                if ssh and sftp:
                    create_remote_directory(sftp, '/var/www/html/files/')
                    upload_images(ssh, sftp, localpaths)
                    close_sftp_server(ssh, sftp)
                    break
            except (paramiko.SSHException, EOFError) as e:
                logger.error(f'Error in upload_images_to_server: {e}. Attempt {attempt + 1} of {retry_attempts}')
                time.sleep(2)
        else:
            logger.error('Failed to connect to the server after several attempts.')
            break
        pbar.update(chunk_size)
    pbar.close()

    if ssh and sftp:
        close_sftp_server(ssh, sftp)
    clear_directory('images_goldapple')


if __name__ == "__main__":
    try:
        logger.info('Starting main program')
        connection = db.connection()
        asyncio.run(upload_images_to_server(connection))
        # asyncio.run(alarm_bot.send_message())
        input('Программа завершила работу, нажмите ENTER')
        logger.info('Finished main program')
    except Exception as e:
        logger.error(f'Error in main program: {e}')
