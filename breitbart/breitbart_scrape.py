import csv
import numpy as np
import os
import pandas as pd
import requests
import sys
from bs4 import BeautifulSoup

if __name__ == '__main__':
    title = 'breitbart_data.csv'
    root = './'
    path_to_data = os.path.join(root, title)

    path_to_article_data = os.path.join(root, 'breitbart_articles.csv')

    urls = list(pd.read_csv(path_to_data).drop(['time', 'title'], axis=1).url.values)

    if os.path.exists(path_to_article_data):
        old_headlines = list(pd.read_csv(path_to_article_data).drop(['article'], axis=1).title.values)
    else:
        old_headlines = []

    headline_article = []
    updated = 0
    for url in urls:
        response = requests.get(url)

        html = response.content

        soup = BeautifulSoup(html, "lxml")

        headline = soup.find_all('h1', itemprop='headline')

        if len(headline) > 0 and headline not in old_headlines:
            headline = headline[0].get_text()
            headline = ''.join((c for c in headline if ord(c) < 128))
            if headline not in old_headlines:
                content = soup.find_all('div', {"class": "entry-content"})[0].get_text()
                content = content.replace('SIGN UP FOR OUR NEWSLETTER', '')
                content = content.replace('var _ndnq=_ndnq||[];_ndnq.push(["embed"])', '')
                content = ''.join((c for c in content if ord(c) < 128))

                headline_article.append([headline, content])
                updated += 1

    print 'saving %03d articles' % updated

    df = pd.DataFrame(data=headline_article, columns=['title', 'article'])

    if not os.path.exists(path_to_article_data):
        df.to_csv(path_to_article_data, header=True, index=False)
    else:
        df.to_csv(path_to_article_data, header=False, index=False, mode='a')
