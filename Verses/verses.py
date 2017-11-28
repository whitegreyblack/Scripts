#!/bin/env python

# File    : function to parse website and scrape daily image
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
    
    print('Image Links Founds: {}'.format(len(img_urls)))
    
    # retrieve the image using given url link
    for url in img_urls:
        # split paths for folder and append file name to create
        # the final destination path for downloaded image
        file = [url.split('/')[-1]]
        path = os.path.realpath(__file__).split('\\')[:-1]
        final_path = "/".join(path + file)

        print('Retrieving: {} @ {}'.format(url, final_path))
        urlretrieve(url, final_path)
    
    exit('Finished')

if __name__ == "__main__":
    print(os.path.realpath(__file__))
    verse()

