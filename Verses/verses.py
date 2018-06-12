#!/bin/env python

# File    : verses.py
# Desc    : parses verse website to retrieve daily hosted image
# Author  : Sam Whang | WGB
# License : MIT

from urllib.request import urlretrieve
from bs4 import BeautifulSoup
import requests
import sys
import os

debug = True

def verse():
    '''Retrieves a verse img reference path to download image to local 
    directory. Checks for duplicates in the directory so multiple calls
    to this function will not download duplicate image links again
    '''
    img_urls = set()
    url_main = 'https://www.bible.com/'
    link = "https://www.bible.com/verse-of-the-day"
    html_tag = 'a'

    # retrieve the html from link
    html = requests.get(link)
    # parse the html into a valid tree object
    soup = BeautifulSoup(html.text, 'html.parser')
    
    # get all meta tag objects with image contents
    for img in soup.find_all(html_tag):
        try:
            if img['content'].endswith('jpg'):
                img_urls.add(img['content'])
        except KeyError:
            pass
    if debug:
        for img_url in img_urls:
            print(img_url)
    
    print(f'Image Links Founds: {len(img_urls)}')
    
    # retrieve the image using given url link
    for url in img_urls:
        # split paths for file and folder names append file name to folder 
        # to create path the final destination path for downloaded image
        file = [url.split('/')[-1]]
        path = os.path.realpath(__file__).split('\\')[:-1]
        final_path = "/".join(path + file)

        path_exists = os.path.exists(final_path)
        path_not_file = not path_exists and not os.path.isfile(final_path)
        if path_not_file:
            print(f'Retrieving: {url} @ {final_path}')
            urlretrieve(url, final_path)
    
    exit('Finished')

if __name__ == "__main__":
    print(os.path.realpath(__file__))
    verse()

