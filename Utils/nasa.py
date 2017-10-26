__author__ = "Sam WGB Whang"
__filename__ = "Nasa.py"
__license__= "MIT"

from bs4 import BeautifulSoup
import urllib.request
import datetime
import os

# base url, path extension
base = "http://apod.nasa.gov/apod/"
path = "archivepix.html"

# Date functions to sanitize dates

def createDates(x, y):
    '''
    Handles date matching and returns days between startdate x and enddate y
    @Parameters
    x: StartDate
    y: EndDate
    '''
    delta = y - x
    dates = [(x + datetime.timedelta(days = i)).isoformat().split("-") 
            for i in range(delta.days + 1)]
    return set(["ap" + "".join([i[0][2::], i[1], i[2]]) + ".html" for i in dates])

def returnDate(x):
    '''
    Handles transforming user input date into a datetime used for comparison 
    with datetimes found on the target website
    @Paremeters:
    x: TargetDate
    '''
    return datetime.date(
            year = (int("19" + x[0:2]) if int(x[0:2]) > 17 else int("20" + x[0:2])),
            month = int(x[2:4]),
            day = int(x[4:6])).isoformat()

def validDate(x):
    '''
    Make sure the date inputed by user does not exceed past a certain date,
    since nasa only started putting up pictures since June 16, 1995. Also 
    validates if the date is a real date
    @Parameters:
    x: TargetDate
    '''
    if x is None or not datetime.date(1995,6,16) <= x <= datetime.date.today():
        return False
    return True


def scrapeData(x, y):
    '''
    Handles the web scraping using urllib and bs4 to fetch target website and 
    search for all images located within html
    @Parameters
    x: StartDate
    y: EndDate
    '''
    links = {}
    dates = createDates(x,y)
    req = urllib.request.urlopen(base+path)
    soup = BeautifulSoup(req,'html.parser')

    imgs = soup.find_all("a")

    # iterate through all found images
    for i in imgs:
        name = i.getText("a").strip()
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
                            name.replace(" ","_") + "." + imgpath.split(".")[-1])
                    print("Downloaded File for %s: %s.%s" % (
                        returnDate(subpath.split('.')[0][2::]),
                        name.replace(" ","_"),
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
    while not validDate(sdate):
        try:
            print("[--Start Date--]")
            sdate = datetime.date(
                    year = int(input(year)),
                    month = int(input(month)),
                    day = int(input(day)))
        except ValueError as ve:
            print("<Error: " + str(ve) + ">")
        finally:
            if not validDate(sdate):
                print("<Error: Start Date not valid>")

    # sanitze end date
    while not validDate(edate):
        try:
            print("[-- End Date --]")
            edate = datetime.date(
                    year = int(input(year)),
                    month = int(input(month)),
                    day = int(input(day)))
        except ValueError as ve:
            print("<Error: " + str(ve) + ">")
        finally:
            if not validDate(edate): 
                print("<Error: End Date not valid>")

    # error checking -- make dates are in the right order
    if sdate > edate:
        sdate, edate = edate, sdate
    
    print("Crawling through site with given dates %s and %s" % (
        sdate.isoformat(),
        edate.isoformat()))

    scrape(sdate, edate)
