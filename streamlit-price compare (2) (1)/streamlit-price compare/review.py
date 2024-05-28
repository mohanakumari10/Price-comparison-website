import requests
from bs4 import BeautifulSoup
import pandas as pd
from pathlib import Path

reviewlist = []
# url = input("link")


def get_soup(url):
    '''r = requests.get('http://localhost:8050/render.html',
                     params={'url': url, 'wait': 2})'''

    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup


def get_reviews(soup):
    reviews = soup.find_all('div', {'data-hook': 'review'})
    try:
        for item in reviews:
            review = {
                'product': soup.title.text.replace('Amazon.co.uk:Customer reviews:', '').strip(),
                'title': item.find('a', {'data-hook': 'review-title'}).text.strip(),
                'rating':  float(item.find('i', {'data-hook': 'review-star-rating'}).text.replace('out of 5 stars', '').strip()),
                'body': item.find('span', {'data-hook': 'review-body'}).text.strip(),
            }
            reviewlist.append(review)
    except:
        pass


def review_scrapper(url, name):
    for x in range(1, 5):
        url = url.replace('dp', 'product-review')
        soup = get_soup(f'{url}={x}')
        print(f'Getting page: {x}')
        get_reviews(soup)
        print(len(reviewlist))
        product_name = soup.find(id="ResultsContainer")
        if not soup.find('li', {'class': 'a-disabled a-last'}):
            pass
        else:
            break
    df = pd.DataFrame(reviewlist)
    # df.to_csv('review.csv', index=False)
    file_path = Path('review_csv/{0}_amazon.csv'.format(name))
    df.to_csv(file_path, index=False)

  # ('sony-headphones.csv', index=False)


# review_scrapper(url)
