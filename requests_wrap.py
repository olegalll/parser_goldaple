import requests
from bs4 import BeautifulSoup
from list_api_request_options import headers, cookies, params




def load_html(page_url):
    response = requests.get(page_url, headers=headers, cookies=cookies, params=params)
    soup = BeautifulSoup(response.text, 'lxml')
    return soup
