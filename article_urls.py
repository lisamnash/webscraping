import csv
import numpy as np
import requests
from bs4 import BeautifulSoup

if __name__ == '__main__':
    url = 'http://www.breitbart.com/'

    response = requests.get(url)

    html = response.content

    soup = BeautifulSoup(html, "lxml")


    # < div class ="featured col4 endcol"

    featured = soup.find_all('div', {'class': 'featured col4 endcol', 'data-tb-region': 'featured'})[0]

    titles = featured.find_all('a', {'class':'thumbnail-url'})

    urls = []
    for title in titles:
        url = 'http://www.breitbart.com/' + title['href']
        urls.append(url)

    print 'saving...'

    outfile = open("./breitbart_urls.csv", "wb")
    writer = csv.writer(outfile)

    writer.writerows([urls])
