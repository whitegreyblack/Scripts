#!/usr/bin/env python

'Scrapes nasa image website to retrieve daily images'

__author__ = "Sam WGB Whang"
__filename__ = "Nasa.py"
__license__= "MIT"

from bs4 import BeautifulSoup
from typing import Sequence, Optional
import urllib.request
import datetime
import os

# base url, path extension
base = "http://apod.nasa.gov/apod/"
path = "archivepix.html"

# Date functions to sanitize dates

def create_dates(start: datetime.date, end: datetime.date) -> Sequence:
    '''
    Handles date matching and returns days between startdate x and enddate y
    @Parameters
    x: StartDate
    y: EndDate
    '''
    delta = end - start if start and end else start - start
    dates = [(start + datetime.timedelta(days = i)).isoformat().split("-") 
            for i in range(delta.days + 1)]
    return set(["ap" + "".join([d[0][2::], d[1], d[2]]) + ".html" for d in dates])

def return_date(datestring: str) -> datetime.date:
    '''
    Handles transforming user input date into a datetime used for comparison 
    with datetimes found on the target website
    @Paremeters:
    x: TargetDate
    '''
    year = int("19" + datestring[0:2] if int(datestring[0:2]) > 17 else "20" + datestring[0:2])
    return datetime.date(
            year = year,
            month = int(datestring[2:4]),
            day = int(datestring[4:6])).isoformat()

def valid_date(date: datetime.date) -> bool:
    '''
    Make sure the date inputed by user does not exceed past a certain date,
    since nasa only started putting up pictures since June 16, 1995. Also 
    validates if the date is a real date
    @Parameters:
    x: TargetDate
    '''
    if date is None or not datetime.date(1995,6,16) <= date <= datetime.date.today():
        return False
    return True

def transform_text(string: str) -> str:
    '''
    Make sure the file name used to save image is a valid filename identifier
    used on the platform the image is being saved on.

        Ex: Windows does not allow for colons, spaces, or mountaintops
    '''
    invalid_chars = ('^', ' ', '\\', '/', ':', '*', '&')
    for character in invalid_chars:
        if character in string:
            string = string.replace(character, '_')
    return string

def scrape(start: datetime.date, end: Union[datetime.date, None]) -> None:
    '''
    Handles the web scraping using urllib and bs4 to fetch target website and 
    search for all images located within html
    @Parameters
    x: StartDate
    y: EndDate
    '''
    links = {}
    dates = create_dates(start, end)
    req = urllib.request.urlopen(base+path)
    soup = BeautifulSoup(req,'html.parser')

    imgs = soup.find_all("a")

    # iterate through all found images
    for i in imgs:
        name = transform_text(i.getText("a").strip())
        subpath = i.get('href')

        # make sure the images match one of the days found in dates list
        if subpath in dates:
            sreq = urllib.request.urlopen(base+subpath)
            ssoup = BeautifulSoup(sreq,'html.parser')
            img = ssoup.find_all("a")

            for j in img:
                imgpath = j.get('href')

                # print the downloaded message
                if (imgpath.startswith('image')):
                    urllib.request.urlretrieve(
                            base + imgpath,
                            name + "." + imgpath.split(".")[-1])

                    print("Downloaded File for %s: %s.%s" % (
                        return_date(subpath.split('.')[0][2::]),
                        name,
                        imgpath.split(".")[-1]))

if __name__ == "__main__":
    # makes sure if user inputs slashes instead of dashes, that they are 
    # changed into a valid date string
    today = datetime.date.today().isoformat().replace("-","/")
    print('[1995/06/16 - %s]' % today)

    # variables used in user input prompts
    year = "Enter in a year [1995-2017]: "
    month = "Enter in a month     [1-12]: "
    day = "Enter in a day       [1-31]: "
    sdate, edate = None, None

    # sanitize startdate
    while not valid_date(sdate):
        try:
            print("[--Start Date--]")
            sdate = datetime.date(
                    year = int(input(year)),
                    month = int(input(month)),
                    day = int(input(day)))
        except ValueError as ve:
            print("<Error: " + str(ve) + ">")
        except KeyboardInterrupt:
            exit('Need to input a date')
        finally:
            if not valid_date(sdate):
                print("<Error: Start Date not valid>")

    # sanitze end date
    while not valid_date(edate):
        try:
            print("[-- End Date --]")
            edate = datetime.date(
                    year = int(input(year)),
                    month = int(input(month)),
                    day = int(input(day)))
        except ValueError as ve:
            print("<Error: " + str(ve) + ">")
        except KeyboardInterrupt:
            break
        finally:
            if edate and not valid_date(edate):
                print("<Error: End Date not valid>")

    # error checking -- make dates are in the right order
    # only goes through if a second date was provided
    if sdate and edate and sdate > edate:
        sdate, edate = edate, sdate
    
    print("Crawling through site with given dates %s %s" % (
        sdate.isoformat(),
        "and " + edate.isoformat() if edate else None))
    scrape(sdate, edate)
