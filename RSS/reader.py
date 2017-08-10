from multiprocessing import Process
from collections import namedtuple
import lxml.etree
import requests
import textwrap
import signal
import json
import time
import sys
import os
import re

# Print color formatting 
ORG = '\x1b[0;34;40m'
YEL = '\x1b[0;33;40m'
GRN = '\x1b[1;32;40m'
RED = '\x1b[1;31;40m'
DIM = '\x1b[2;49;90m'
END = '\x1b[0m'

# naive cache using dictionary
feed = namedtuple('Feed', ['updated'])
feeds={}
post = namedtuple('Post', ['title', 'urlink'])
posts={}

# used in text wrapping to print clean wrapped lines
rows, columns = os.popen('stty size', 'r').read().split()



# used to check rss feeds
def parseJSON(filename):
    """
    ARG: Filename - the local file holding the urls in wellformed json
    DEF: Parses the filename based on url base schema and links data
         Sends the parsed url list to getXML
    """
    urls=None
    try:
        with open(filename, 'r') as f:
            data=json.loads(f.read())
            schema=data["reddit"]["schema"]
            links=data["reddit"]["links"]
            urls=[schema.format(link["sub"]) for link in links]
    except:
        raise
        print("Incorrect Json Format")
    if urls:
        loopURLS(urls)

def loopURLS(urls):
    """
    ARG: Urls - the list of urls to retrieve data from
    DEF: Generates a while loop of fetching xml data to keep feed alive
    """
    try:
        while 1:
            for url in urls:
                fetchURL(url)
            time.sleep(5)
    except KeyboardInterrupt:
        pass

def fetchURL(url):
    """
    ARG: Url - a single uri link used by requests package to fetch rss data
    DEF: Using requests, sets user-agent header and gets request from url
         If the url is illformed or not complete then an exception is raised
    """
    headers={'user-agent': 'beautify'}
    try:
        req = requests.get(url, headers=headers)
        parseRSS(req.text.encode())
    except:
        raise

def parseRSS(string):
    """
    ARG: String - rss text encoded in bytes
    DEF: creates a lxml tree from string and walks down tree access data
         Puts all entries into a posts dictionary so that reiteration does
         not print the same post again. Also loops again only prints more
         posts if the rss feed's updated text has been changed
    """
    global update
    try:
        tree=lxml.etree.fromstring(string)
    except:
        print("Invalid XML format")
        return

    title= ""
    postid= ""
    dtime= ""
    urlink= ""
    label=""

    for child in tree:
        if "category" in child.tag:
            if not label:
                label=child.attrib["label"]
        if "updated" in child.tag:
            if not update:
                update=child.text
            else:
                if child.text==update:
                    return
        if "entry" in child.tag:
            for subchild in child:
                if "title" in subchild.tag:
                    title=subchild.text
                if "id" in subchild.tag:
                    postid=subchild.text
                if "link" in subchild.tag:
                    urlink=subchild.attrib['href']

            if postid not in posts.keys():
                # printing time -- uses textwrap to pretty print the post data
                print(textwrap.fill(format(" "+YEL+title+END+" ["+label+"]"), width=int(columns), subsequent_indent=' '))
                print(" "+DIM+urlink[:int(columns):]+END)
                time.sleep(1)

        if title and postid and urlink:
            # add to the posts cache and reset variables
            posts[postid] = post(title, urlink)
            title, postid, urlink = "", "", ""

if __name__ == "__main__":
    if len(sys.argv)==2:
        parseJSON(sys.argv[1])
