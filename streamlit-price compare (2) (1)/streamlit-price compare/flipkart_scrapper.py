import bs4
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
from time import sleep
from random import random
import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import urllib.parse as urlparse
from urllib.parse import parse_qs
from pathlib import Path


def flipkart(name):
    name1 = name.replace(" ", "+")
    link = f'https://www.flipkart.com/search?q={name1}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off'
    BASE_URL = 'https://www.flipkart.com/'
    SEARCH_QUERY = name
    page = requests.get(link)

    page.content

    soup = bs(page.content, 'html.parser')

    results = soup.find_all('div', {
                            'class': '_2kHMtA', 'data-tkid': "en_SK+90lGNxp6h4SPV/tOrynkEl54PwEvslt7kAZV+B+hYmcfJnFUYF2h009hRPITG/qlO06Ee58jEdsJwOPD2hg=="})
    products = []
    prices = []
    ratings = []
    links = []
    for data in soup.findAll('div', class_='_4ddWXP'):
        names = data.find('a', attrs={'class': 's1Q9rs'}).text
        price = data.find('div', attrs={'class': '_30jeq3'}).text
        rating = soup.find('div', class_="_3LWZlK").text
        products.append(names)

        title_mention_subrow = data.find("a", attrs={"class": "s1Q9rs"})

        product_relative_url = title_mention_subrow["href"]
        product_url = urljoin(BASE_URL, product_relative_url)

        parsed_url = urlparse.urlparse(product_url)
        parsed_url_path = parsed_url.path
        parsed_url_path_split = parsed_url_path.split("/")
        parsed_url_path_split[2] = "product-reviews"
        parsed_url_path_modified = "/".join(parsed_url_path_split)
        parsed_url_modified = parsed_url._replace(
            path=parsed_url_path_modified)
        product_url = parsed_url_modified.geturl()

        links.append(product_url)
        price = price.replace("₹", "")
        price = price.replace(",", "")
        price = int(price)
        prices.append(price)
        rating = float(rating)
        ratings.append(round(rating, 1))
    df = pd.DataFrame({'Product Name': products, 'Price': prices,
                       'Rating': ratings, 'link': links})

    if df.empty:
        for data in soup.findAll('div', class_='_2kHMtA'):
            names = data.find('div', attrs={'class': '_4rR01T'}).text
            price = data.find('div', attrs={'class': '_30jeq3'}).text
            rating = soup.find('div', class_="_3LWZlK").text
            products.append(names)
            price = price.replace("₹", "")
            price = price.replace(",", "")
            price = int(price)
            prices.append(price)
            rating = float(rating)
            ratings.append(round(rating, 1))

            title_mention_subrow = data.find("a", attrs={"class": "_1fQZEK"})

            product_relative_url = title_mention_subrow["href"]
            product_url = urljoin(BASE_URL, product_relative_url)

            parsed_url = urlparse.urlparse(product_url)
            parsed_url_path = parsed_url.path
            parsed_url_path_split = parsed_url_path.split("/")
            parsed_url_path_split[2] = "product-reviews"
            parsed_url_path_modified = "/".join(parsed_url_path_split)
            parsed_url_modified = parsed_url._replace(
                path=parsed_url_path_modified)
            product_url = parsed_url_modified.geturl()

            links.append(product_url)
        df = pd.DataFrame(
            {'Product Name': products, 'Price': prices, 'Rating': ratings, 'link': links})

    file_path = Path('csv_files/{0}_flipkart.csv'.format(name))
    df.to_csv(file_path, index=False)
    # print(link)
    # print(df)
