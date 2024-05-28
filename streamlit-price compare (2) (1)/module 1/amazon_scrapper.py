import bs4
from bs4 import BeautifulSoup
import requests
import pandas as pd
from time import sleep
from pathlib import Path
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip',
    'DNT': '1',  # Do Not Track Request Header
    'Connection': 'close'
}

# name = input('enter the product name: ')
# search_query = name.replace(' ', '+')
# base_url = 'https://www.amazon.com/s?k={0}'.format(search_query)


def amazon(base_url):
    items = []
    for i in range(1, 5):
        print('Processing {0}...'.format(base_url + '&page={0}'.format(i)))
        response = requests.get(
            base_url + '&page={0}'.format(i), headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        results = soup.find_all(
            'div', {'class': 's-result-item', 'data-component-type': 's-search-result'})

    for result in results:
        product_name = result.h2.text

        try:
            rating = result.find('i', {'class': 'a-icon'}).text
            # rating_count = result.find_all('span', {'aria-label': True})[1].text
        except AttributeError:
            continue

        try:
            price1 = result.find('span', {'class': 'a-price-whole'}).text
            price2 = result.find('span', {'class': 'a-price-fraction'}).text
            price1 = re.findall(r'\b\d+\b', price1)
            price1 = int(price1[0])
            price = round(float(price1)*82.76)

            product_url = 'https://amazon.com' + result.h2.a['href']

            # print(rating_count, product_url)
            items.append(
                [product_name, rating, price, product_url])
        except AttributeError:
            continue
    return items
    sleep(1.5)


def amozon_csv(items, name):
    df = pd.DataFrame(
        items, columns=['product', 'rating', 'price', 'product url'])
    file_path = Path('csv_files/{0}_amazon.csv'.format(name))
    df.to_csv(file_path, index=False)
    print(df)


# amozon_csv(items)
def run(name):
    search_query = name.replace(' ', '+')
    base_url = 'https://www.amazon.com/s?k={0}'.format(search_query)
    items = amazon(base_url)
    amozon_csv(items, name)


print("Amazon product search")
name = input("Enter the search product name: ")
run(name)
