#!/bin/env python

# File    : movies.py
# Desc    : Scrapes local movie website for current and future movies
# Author  : Sam Whang | WGB
# License : MIT

import os
import sys
from bs4 import BeautifulSoup

def vc_listing():
    link = http://bison6cinema.com/valley-city/

def jt_listing():
    link = http://bison6cinema.com

def upcoming():
    link = http://bison6cinema.com
    
listings = {
    'vc': vc_listing,
    'jt': jt_listing,
    'up': upcoming,
}

def movies():
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
