import lxml.etree
import sys
import os
import textwrap
from collections import namedtuple
import requests
import re
"""
Design
    ---
Dont need to write to any files, only read
    ---
Start with an empty cache
Initially call requests for first xml text
Populate cache with posts
Print any posts and mark read
Wait 30 seconds
Refresh xml text and check for any new posts
Print any posts not in the dictionary aleady
"""
# Print color formatting 
ORG = '\x1b[0;34;40m'
YEL = '\x1b[0;33;40m'
GRN = '\x1b[1;32;40m'
RED = '\x1b[1;31;40m'
DIM = '\x1b[2;49;90m'
END = '\x1b[0m'

def convertXMLtoBinary(string):
    #return " ".join(format(ord(x), 'b') for x in string)
    return string.encode()

# use requests to get xml
def getXML(url):
    headers={'user-agent': 'beautify'}
    # urls = [ url for url in url_file ]
    try:
        req = requests.get(url, headers=headers)
        parseXML(req.text)
    except:
        raise
# naive cache using dictionary
post = namedtuple('Post', ['title', 'urlink'])
posts={}

# used in text wrapping to print clean wrapped lines
rows, columns = os.popen('stty size', 'r').read().split()

def readXML():
    # TODO: removal -- will use requests to dynamically update xml text
    with open('reddit.rss', 'br') as f:
        string = lt.fromstring(f.read())

def parseXML(string):
    string=convertXMLtoBinary(string)
    print(string)
    try:
        tree=lxml.etree.fromstring(string)
    except:
        print("Invalid XML format")
        raise
        return
    title= ""
    postid= ""
    dtime= ""
    urlink= ""

    for child in tree:
        if "entry" in child.tag:
            for subchild in child:
                if "title" in subchild.tag:
                    title=subchild.text
                if "id" in subchild.tag:
                    postid=subchild.text
                if "link" in subchild.tag:
                    urlink=subchild.attrib['href']

        print(" "+postid) 
        print(textwrap.fill(" "+format(YEL+title+END), width=int(columns), subsequent_indent=' '))
        print(" "+DIM+urlink[:int(columns)-2:]+END)

if __name__ == "__main__":
    if len(sys.argv)==2:
        print(sys.argv[1])
        getXML(sys.argv[1])
