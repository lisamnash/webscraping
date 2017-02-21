import csv
import numpy as np
import os
import pandas as pd
import requests
import sys
import time
from bs4 import BeautifulSoup

if __name__ == '__main__':
    title = 'breitbart_data.csv'
    root = './'
    path_to_data = os.path.join(root, title)

    if os.path.exists(path_to_data):
        old_data = list(pd.read_csv(path_to_data).drop(['time', 'title'], axis=1).url.values)

    else:
        old_data = []

    now = time.strftime('%Y_%m_%d_%H.%M.%S')

    Bb_url = 'http://www.breitbart.com'
    response = requests.get(Bb_url)
    html = response.content
    soup = BeautifulSoup(html, "lxml")

    featured = soup.find_all('div', {'class': 'featured col4 endcol', 'data-tb-region': 'featured'})[0]
    titles = featured.find_all('a', {'class': 'thumbnail-url'})

    urls = []
    new = 0
    for title in titles:
        url = Bb_url + title['href']
        title = title.get_text()
        title = ''.join((c for c in title if ord(c) < 128))
        if url not in old_data:
            urls.append([now, title, url])
            new+=1

    print 'saving...'
    print 'new ,' , new
    df = pd.DataFrame(data=urls, columns=['time', 'title', 'url'])

    if not os.path.exists(path_to_data):
        df.to_csv(path_to_data, header=True, index=False, date_format='%Y%m%d')
    else:
        df.to_csv(path_to_data, header=False, index=False, date_format='%Y%m%d', mode='a')
