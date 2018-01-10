#!/bin/env python

# File    : movies.py
# Desc    : Scrapes local movie website for current and future movies
# Author  : Sam Whang | WGB
# License : MIT

import os
import sys
from bs4 import BeautifulSoup

def vc_listing():
    '''Retrieves movie list from valley-city section'''
    link = http://bison6cinema.com/valley-city/

def jt_listing():
    '''Retrieves movie list from jamestown section'''
    link = http://bison6cinema.com

def upcoming():
    '''Retrieves upcoming movie lsit from jamestown section'''
    link = http://bison6cinema.com
    
# dictionary used during args parsing to specify individual functions
listings = {
    'vc': vc_listing,
    'jt': jt_listing,
    'up': upcoming,
}

def movies():
    '''Main driver that calls vc, jt, and upcoming functions
    Input arguments specified are parsed here for running commands
    '''
    if len(sys.argv) == 1:
        vc_listing()
        jt_listing()
        upcoming()

    else:
        try:
            listings[sys.argv[1]]()
        except KeyError:
            print('Parameter input not recognized', sys.argv[1])

if __name__ == "__main__":
    print(len(sys.argv), sys.argv)
    movies()
