#!/bin/env python
'''
Author: Sam Whang
File  : googlefeed.py
Usage : py googlefeed.py <googlelinks.txt>
Info  : A Google News RSS Feed watcher that consumes newly pushed rss data
        from a list of provided Google News rss urls
'''
from collections import namedtuple
import lxml.etree
import requests
import textwrap
import json
import time
import sys
import os

# debug variable
debug = False

# Used in time.sleep
outputspeed = 1
refreshspeed = 3

# Print color formatting
ORG = '\x1b[0;34;40m'
YEL = '\x1b[0;33;40m'
GRN = '\x1b[1;32;40m'
RED = '\x1b[1;31;40m'
DIM = '\x1b[2;49;90m'
END = '\x1b[0m'

# naive cache using dictionary
feeds = {}
post = namedtuple('Post', ['title', 'urlink', 'category'])
posts = {}
printer=[]

# used in text wrapping to print clean wrapped lines
rows, columns = os.popen('stty size', 'r').read().split()

# used to check rss feeds


def parseJSON(filename):
    """
    ARG: Filename - the local file holding the urls in wellformed json
    DEF: Parses the filename based on url base schema and links data
         Sends the parsed url list to getXML
    """
    urls = None
    if debug:
        print("parse JSON")
    try:
        with open(filename, 'r') as f:
            data = json.loads(f.read())
            for newssite in data:
                print(newssite)
                schema = data[newssite]["schema"]
                links = data[newssite]["links"]
                urls = [schema.format(link["sub"]) for link in links]
                print(urls)
    except KeyError:
        print("Using wrong JSON format")
    if urls:
        loopURLS(urls)


def loopURLS(urls):
    """
    ARG: Urls - the list of urls to retrieve data from
    DEF: Generates a while loop of fetching xml data to keep feed alive
    """
    if debug:
        print("looping")
    try:
        while 1:
            for url in urls:
                fetchURL(url)
    except:
        raise

def fetchURL(url):
    """
    ARG: Url - a single uri link used by requests package to fetch rss data
    DEF: Using requests, sets user-agent header and gets request from url
         If the url is illformed or not complete then an exception is raised
    """
    if debug:
        print("Fetching")
    headers = {'user-agent': 'beautify'}
    try:
        req = requests.get(url, headers=headers)
        parseRSS(req.text.encode())
    except BaseException:
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
    global posts
    '''
    title = None
    postid = None
    dtime = None
    urlink = None
    label = None
    urlid = None
    '''
    try:
        tree = lxml.etree.fromstring(string)
    except BaseException:
        print(string)
        print("Invalid XML format")
        return
    '''
    for child in tree:
        # header information
        if "id" in child.tag:
            urlid = child.text
        if "category" in child.tag:
            label = child.attrib["label"]
        if "updated" in child.tag:
            update = child.text

        # check and update feed info -- should only happen once every parse
        # if update is the same as parsed code then no changes and exit
        if urlid and update:
            if urlid in feeds.keys():
                if feeds[urlid] == update:
                    return
            feeds[urlid] = update
            urlid, update = None, None

        # entry post information
        if "entry" in child.tag:
            for subchild in child:
                if "title" in subchild.tag:
                    title = subchild.text
                if "id" in subchild.tag:
                    postid = subchild.text
                if "link" in subchild.tag:
                    urlink = subchild.attrib['href']

            if postid not in posts.keys():
                # add to the posts cache and reset variables
                print(label, postid, len(posts), [ids for ids in posts.keys()])
                posts[postid] = post(title, urlink, label)

                # printing time -- uses textwrap to pretty print the post data
                printer.append(posts[postid])

                title, postid, urlink = None, None, None

                time.sleep(outputspeed)
    '''
    """
    RSS V2.0:
        channel { generator | title | link | language | copyright | pubdate | lastbuilddate }
        item { title | link | category | pubdate | descrption }
        title == title
        pubdate == dtime but in different format
        link == urlink
        category == label just different name
        no
    """
    title = None
    dtime = None
    build = None
    label = None
    urlink = None
    for child in tree:
        if "channel" in child.tag:
            for info in child:
                # header information
                if "title" in info.tag:
                    urlid = info.text
                if "pubDate" in info.tag:
                    dtime = info.text
                if "lastBuildDate" in info.tag:
                    build = info.text
                if "item" in info.tag:
                    for attr in info:
                        if "title" in attr.tag:
                            title = attr.text
                        if "link" in attr.tag:
                            urlink = attr.text
                        if "category" in attr.tag:
                            label = attr.text
                    print(textwrap.fill(format(" " + YEL + title + END + " [" + label + "]"),
                                        width=int(columns)-2,
                                        subsequent_indent=' '))
                    print(" " + DIM + urlink[:int(columns):] + END)
                    time.sleep(outputspeed)
    #print(urlid, dtime, build)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        parseJSON(sys.argv[1])
    else:
        print("enter in a links json file")
