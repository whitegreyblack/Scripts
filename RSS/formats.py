## File : feedparser.py
# Name : Sam Whang | WGB

"""
    REQUIRED: 
        RSS 2.0: feed-level title, link and description
        RSS 2.0: does not require any of the fields in a feed be present
        Atom1.0: both feeds and entries need a title, uiuqe identifier and last-updated timestamp
        Atom1.0: a newer spec of the rss format feed
    COMPARISON:
        RSS 2.0 VS ATOM 1.0
        LABEL:
            RSS 2.0                    | ATOM 1.0                   | Comments/Advice
           +---------------------------+----------------------------+-----------------------------------------------------------+
            rss                        | -----                      |
            channel                    | feed                       |
            title                      | title                      |
            link                       | link                       | (link contains a list of "rel" values")
            language                   | -----                      |
            copyright                  | rights                     |
            webMaster                  | -----                      |
            managingEditor             | author/contributor         |
            pubDate                    | published (in entry)       | Atom has no feed-level equivalent
            lsatBuildDate (in channel) | updated                    | RSS has no item-level equivalent
            category                   | category                   |
            docs                       | -----                      |
            cloud                      | -----                      |
            ttl                        | -----                      |
            image                      | -----                      |
            -----                      | icon                       |
            rating                     | -----                      |
            textInput                  | -----                      |
            skipHours                  | -----                      |
            skipDays                   | -----                      |
            item                       | entry                      |
            author                     | author                     |
            -----                      | contributor                |
            description                | summary/content            | depends on wheter full content is provided
            coments                    | summary/content            | ...
            enclosure                  | -----                      | (rel="enclosure" in link)
            guid                       | id                         |
            source                     | -----                      | (rel="via" in link)
            -----                      | source                     | Container for feed-level metadata to support aggregation
          +----------------------------+----------------------------+-----------------------------------------------------------+
"""
# working on atom rss parser
# maybe rss v1,2 later

# ---
# <atom : feed>
#       <atom : person>
#           <atom : name>
#           <atom : email>
#           <atom : uri>
#       <atom : /person>
#       <atom : entry>
#           <atom : pass>
#       <atom : /entry>
# <atom : /feed>

def dtparse(dt):
    pass

class PersonConstruct:
    def __init__(self, name, uri, email)
        self.construct="Author"
        self.name=name
        self.uri=uri
        self.email=email
    
class atom:
    def __init__(self):
        self.tag=''
        self.attrib={}
        self.children=[]
