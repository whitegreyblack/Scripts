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
