import requests
from bs4 import BeautifulSoup
import csv


def get_soup(url):
    r = requests.get(url)
    return BeautifulSoup(r.text, 'lxml')

def get_content_list(url):
    # Get the BeautifulSoup object for the given url
    soup = get_soup(url)
    urls = []
    # Find all 'article' tags in the soup
    articles = soup.find_all('article')
# TODO: добавить пагинацию страницы
    
    # For each article, get the 'data-scroll-id' attribute
    scroll_ids = [article.get('data-scroll-id') for article in articles]
    # For each article, find all 'meta' tags with itemprop='name' and get their 'content' attribute
    full_name = [[meta.get('content') for meta in article.find_all('meta', itemprop='name')] for article in articles]
    # For each article, find the 'a' tag and get its 'href' attribute
    product_paths = [article.find('a').get('href') if article.find('a') else None for article in articles]
    # For each article, find the 'div' tags with specific 'data-test-id' attributes and get their text content
    prices = [(int(article.find('div', {'data-test-id': 'old-price'}).text.strip().replace(' ', '').replace('₽', '')) if article.find('div', {'data-test-id': 'old-price'}) else None,
                int(article.find('div', {'data-test-id': 'actual-price'}).text.strip().replace(' ', '').replace('₽', '')) if article.find('div', {'data-test-id': 'actual-price'}) else None) for article in articles]

    # For each article, create a dictionary with the extracted details and append it to the urls list
    for i in range(len(articles)):
        urls.append({
            'price': prices[i],
            'full_name': full_name[i],
            'scroll_id': scroll_ids[i],
            'product_path': product_paths[i]
        })
    print(urls)



def main():
    url = 'https://goldapple.ru/makijazh?calculatedprices=22-4053'
    get_content_list(url)
    # TODO: добавить сохранение в базу данных
    # TODO: написать парсер для каждой карточки


    # with open('data.csv', 'w', newline='') as f:
    #     writer = csv.writer(f)
    #     writer.writerow(['title', 'price'])
    #     for product in soup.find_all('div', class_='product-item'):
    #         title = product.find('a', class_='product-item__title').text
    #         price = product.find('span', class_='price').text
    #         writer.writerow([title, price])

if __name__ == '__main__':
    main()

