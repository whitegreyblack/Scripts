import datetime
from bs4 import BeautifulSoup
import urllib.request
import os

__author__ = "Sam WGB Whang"
__license__= "MIT"

# base path
base = "http://apod.nasa.gov/apod/"
path = "archivepix.html"

def createDates(x,y):
    delta = y - x
    dates = [(x + datetime.timedelta(days=i)).isoformat().split("-") for i in range(delta.days+1)]
    return set(["ap"+"".join([i[0][2::],i[1],i[2]])+".html" for i in dates])

def scrape(x,y):
    links = {}
    dates = createDates(x,y)
    req = urllib.request.urlopen(base+path)
    soup = BeautifulSoup(req,'html.parser')

    imgs = soup.find_all("a")
    for i in imgs:
        name = i.getText("a").strip()
        subpath = i.get('href')
        if subpath in dates:
            sreq = urllib.request.urlopen(base+subpath)
            ssoup = BeautifulSoup(sreq,'html.parser')
            img = ssoup.find_all("a")
            for j in img:
                imgpath = j.get('href')
                if (imgpath.startswith('image')):
                    print("Downloaded File for %s: %s.%s"
                            %(returnDate(subpath.split('.')[0][2::]),name.replace(" ","_"),imgpath.split(".")[-1]))
                    urllib.request.urlretrieve(base+imgpath,name.replace(" ","_")+"."+imgpath.split(".")[-1])
def returnDate(x):
    return datetime.date(year=(int("19"+x[0:2]) if int(x[0:2]) > 17 else int("20"+x[0:2])),
            month = int(x[2:4]),
            day = int(x[4:6])).isoformat()

def validDate(x):
    if x is None or not datetime.date(1995,6,16) <= x <= datetime.date.today():
        return False
    return True

def main():
    today = datetime.date.today().isoformat().replace("-","/")
    print('[1995/06/16 - %s]'%today)
    year = "Enter in a year [1995-2017]: "
    month = "Enter in a month     [1-12]: "
    day = "Enter in a day       [1-31]: "
    sdate, edate = None, None
    while not validDate(sdate):
        try:
            print("[--Start Date--]")
            sdate = datetime.date(year=int(input(year)),month=int(input(month)),day=int(input(day)))
        except ValueError as ve:
            print("<Error: "+str(ve)+">")
        finally:
            if not validDate(sdate):
                print("<Error: Start Date not valid>")

    while not validDate(edate):
        try:
            print("[-- End Date --]")
            edate = datetime.date(year=int(input(year)),month=int(input(month)),day=int(input(day)))
        except ValueError as ve:
            print("<Error: "+str(ve)+">")
        finally:
            if not validDate(edate): print("<Error: End Date not valid>")
    
    if sdate > edate:
        sdate, edate = edate, sdate
    
    print("Crawling through site with given dates %s and %s"%(sdate.isoformat(),edate.isoformat()))
    scrape(sdate, edate)


if __name__ == "__main__":
    main()
