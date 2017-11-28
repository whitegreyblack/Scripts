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
        print('Retrieving: {} @ {}'.format(url, url.split('/')[-1]))
        urlretrieve(url, url.split('/')[-1])
    
    exit('Finished')

if __name__ == "__main__":
    verse()

