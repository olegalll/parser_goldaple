from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from lxml import html
import time 
import logging
from urllib.parse import urlencode


from list_api_request_options import headers, cookies, params


def browser_open(): 
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('log-level=3')  # Игнорирует предупреждения и сообщения ниже уровня ERROR
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument("--remote-allow-origins=*")
    chrome_options.add_argument("--use-fake-ui-for-media-stream")  # Использовать фиктивные медиа-устройства
    chrome_options.add_argument("--disable-default-apps") 
    chrome_options.add_argument("--no-first-run")


    driver = webdriver.Chrome(options=chrome_options)
    return driver

def load_html(driver, page_url):
    try:
        # Открыть новую вкладку и переключиться на неё
        driver.execute_script("window.open('');")
        time.sleep(1)  # небольшая задержка для устойчивости
        driver.switch_to.window(driver.window_handles[-1])
        # Добавление параметров в URL, если они предоставлены
        if params:
            query_string = urlencode(params)
            page_url += '?' + query_string

        driver.get(page_url)
        
                # Установка заголовков и cookies, если они предоставлены
        if headers:
            for header, value in headers.items():
                driver.execute_script(f'document.setRequestHeader("{header}", "{value}");')
        if cookies:
            for cookie_name, cookie_value in cookies.items():
                driver.add_cookie({'name': cookie_name, 'value': cookie_value})

        # Загрузка и парсинг HTML
        time.sleep(3)  # Пауза, чтобы дать странице загрузиться
        source_code = driver.page_source
        tree = html.fromstring(source_code)
    except Exception as e:
        logging.error(f"load_html: {e}")
        tree = None

    # Закрыть текущую вкладку и вернуться к предыдущей (если она есть)
    driver.close()
    if len(driver.window_handles) > 0:
        driver.switch_to.window(driver.window_handles[-1])

    return tree


def browser_close(driver):
    driver.quit()

