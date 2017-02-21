import csv
import numpy as np
import os
import pandas as pd
import requests
import sys
import time
from bs4 import BeautifulSoup
import re

if __name__ == '__main__':
    title = 'slate_data.csv'
    root = './'
    path_to_data = os.path.join(root, title)

    if os.path.exists(path_to_data):
        old_data = list(pd.read_csv(path_to_data).drop(['time', 'title'], axis=1).url.values)
    else:
        old_data = []

    now = time.strftime('%Y_%m_%d_%H.%M.%S')

    slate_url = 'http://www.slate.com'
    response = requests.get(slate_url)
    html = response.content
    soup = BeautifulSoup(html, "lxml")

    featured = soup.find_all('a', {'class': 'primary'}, href=True)

    urls = []
    new = 0
    for feature in featured:
        try:

            data_track = feature['data-track']
            article_info = re.findall(r"[\w']+", data_track)

            if 'TopShelf' or 'Cabinet' in article_info:
                url = feature['href']

                title = feature['data-vr-excerpttitle']
                title = ''.join((c for c in title if ord(c) < 128))
                url = ''.join((c for c in url if ord(c) < 128))

                if url not in old_data:
                    urls.append([now, title, url])
                    new += 1
        except:
            for sub in feature:
                try:
                    data_track = sub['data-track']
                    article_info = re.findall(r"[\w']+", data_track)

                    if 'TopShelf' or 'Cabinet' in article_info:
                        url = feature['href']

                        title = sub['data-vr-excerpttitle']
                        title = ''.join((c for c in title if ord(c) < 128))
                        url = ''.join((c for c in url if ord(c) < 128))

                        if url not in old_data:
                            urls.append([now, title, url])
                            new += 1
                except:
                    a=1
    print 'saving...'
    print 'number of new urls , ', new
    df = pd.DataFrame(data=urls, columns=['time', 'title', 'url'])

    if not os.path.exists(path_to_data):
        df.to_csv(path_to_data, header=True, index=False, date_format='%Y%m%d')
    else:
        df.to_csv(path_to_data, header=False, index=False, date_format='%Y%m%d', mode='a')
