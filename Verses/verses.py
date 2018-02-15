#!/bin/env python

# File    : verses.py
# Desc    : parses website to retrieve daily hosted image
# Author  : Sam Whang | WGB
# License : MIT

import os
import sys
import requests
from bs4 import BeautifulSoup
from urllib.request import urlretrieve

def verse():
    img_urls = set()
    link = "https://www.bible.com/verse-of-the-day"
    
    # retrieve the html from link
    html = requests.get(link)
    # parse the html into a valid tree object
    soup = BeautifulSoup(html.text, 'html.parser')
    
    # get all meta tag objects with image contents
    for img in soup.find_all('meta'):
        try:
            if img['content'].endswith('jpg'):
                img_urls.add(img['content'])
        except KeyError:
            pass
    
    print(f'\033[1AImage Links Founds: {len(img_urls)}')
    
    # retrieve the image using given url link
    for url in img_urls:
        # split paths for folder and append file name to create
        # the final destination path for downloaded image
        file = [url.split('/')[-1]]
        path = os.path.realpath(__file__).split('\\')[:-1]
        final_path = "/".join(path + file)
        if not os.path.exists(final_path) or (os.path.exists(final_path) and not os.path.isfile(final_path)):
            print(f'\033[1ARetrieving: {url} @ {final_path}')
            urlretrieve(url, final_path)
    
    exit('\033[1AFinished')

if __name__ == "__main__":
    print(os.path.realpath(__file__))
    verse()

