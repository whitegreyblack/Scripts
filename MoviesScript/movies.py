#!/bin/env python

# File    : movies.py
# Desc    : Scrapes local movie website for current and future movies
# Author  : Sam Whang | WGB
# License : MIT

from urllib.request import urlretrieve
from bs4 import BeautifulSoup
import requests
import sys
import os

text = []

def parser(link, tag, cls=None):
    html = requests.get(link)
    soup = BeautifulSoup(html.text, 'html.parser')
    for title in soup.find_all(tag, {'class': cls} if cls else {}):
        try:
            text.append(title.get_text())
        except KeyError:
            raise

def vc_listing():
    '''Retrieves movie list from valley-city section Finds all headers with
    tag "h4" and class id "heading14" to find all valley city listed movies
    '''
    link = "http://bison6cinema.com/valley-city/"
    text.append('--- Valley City Listings ---')
    parser(link, 'h4', 'heading14')

def jt_listing():
    '''Retrieves movie list from jamestown section. Finds all headers with 
    tag "h4" and class id "heading18" to find all jamestown listed movies.
    '''
    link = "http://bison6cinema.com"
    text.append('--- Jamestown Listings  ---')
    parser(link, 'h4', 'heading18')

def upcoming():
    '''Retrieves upcoming movie lsit from jamestown section. Upcoming is a 
    little different from VC and JT functions since they are not surrounded
    by spans like the upcoming movies.
    '''
    link = "http://bison6cinema.com"
    html = requests.get(link)
    soup = BeautifulSoup(html.text, 'html.parser')

    text.append('---   Upcoming Movies   ---')
    for title in soup.find_all('span'):
        if not title.attrs:
            for string in title.stripped_strings:
                text.append(string)

def movies():
    '''Main driver that calls vc, jt, and upcoming functions
    Input arguments specified are parsed here for running commands
    '''
    # dictionary used during args parsing to specify individual functions
    listings = {
        'vc': vc_listing,
        'jt': jt_listing,
        'up': upcoming,
    }

    # check if args not specified
    if len(sys.argv) == 1:
        for link in listings.values():
            link()

    else:
        try:
            listings[sys.argv[1].replace('-', '')]()
        except KeyError:
            print('Parameter input not recognized', sys.argv[1])

    # combine text array into multi line string and print
    if text:
        print("\n".join(text))

if __name__ == "__main__":
    # print(len(sys.argv), sys.argv)
    movies()
