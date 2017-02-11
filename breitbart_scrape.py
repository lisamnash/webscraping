import csv
import numpy as np
import requests
from bs4 import BeautifulSoup

if __name__ == '__main__':
    urls = [
        'http://www.breitbart.com/jerusalem/2017/02/11/palestinian-authority-media-americans-made-mistake-electing-megalomaniac-trump-as-germans-did-with-hitler/',
        'http://www.breitbart.com/london/2017/02/11/wilders-whatever-happens-2017-populist-genie-bottle/',
        'http://www.breitbart.com/jerusalem/2017/02/11/trump-iranian-president-rouhani-better-careful/',
        'http://www.breitbart.com/big-government/2017/02/10/chicago-four-charged-in-facebook-live-torture-case-plead-not-guilty/',
        'http://www.breitbart.com/video/2017/02/10/moveon-spox-you-fear-trumps-presidency-if-youre-not-white-male-and-straight/'
    ]

    headlines = []
    articles = []
    for url in urls:
        response = requests.get(url)

        html = response.content

        soup = BeautifulSoup(html, "lxml")

        headline = soup.find_all('h1', itemprop='headline')[0].get_text()

        content = soup.find_all('div', {"class": "entry-content"})[0].get_text()

        content = content.split('SIGN UP FOR OUR NEWSLETTER')
        content = ''.join(c for c in content)
        content = content.split('var _ndnq=_ndnq||[];_ndnq.push(["embed"])')
        content = ''.join(c for c in content)
        content = ''.join((c for c in content if ord(c) < 128))
        headline = ''.join((c for c in headline if ord(c) < 128))

        headlines.append(headline)
        articles.append(content)

    print 'saving...'

    outfile = open("./breitbart_articles.csv", "wb")
    writer = csv.writer(outfile)

    writer.writerows(np.array([headlines, articles]).T)
