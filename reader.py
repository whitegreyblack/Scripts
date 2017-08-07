import lxml.etree as lt
import os
import textwrap
from collections import namedtuple
import requests

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

# use requests to get xml
def getxml():
    headers={'user-agent': 'beautify'}
    # urls = [ url for url in url_file ]
    url = 'https://www.reddit.com/r/popular/.rss'
    req = requests.get(url, headers=headers)
    return req.text

# naive cache using dictionary
Post = namedtuple('Post', ['title', 'urlink'])
posts={}

# used in text wrapping to print clean wrapped lines
rows, columns = os.popen('stty size', 'r').read().split()

# TODO: removal -- will use requests to dynamically update xml text
with open('reddit.rss', 'br') as f:
    string = lt.fromstring(f.read())

def parse():
    title= ""
    postid= ""
    dtime= ""
    urlink= ""

    for child in string:
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

