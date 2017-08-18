import re
interfaces = [
    [["TenGigabitEthernet","Te"],"Te"],
    [["GigabitEthernet","Gi"],"Gi"],
    [["FastEthernet","Fa"],"Fa"],
    [["Ethernet","Eth"],"Eth"],
    [["Port-channel","Po"],"Po"],
    [["Serial"],"Ser"],
]
def deviceRegex(string):
    pattern = r'([a-zA-Z\-]*)(\d+[\/\d\:]*)'
    result = re.match(pattern, string)
    try:
        groups = result.groups()
        print(list(groups)[1])
    except:
        raise

def convertName(string):
    pattern = r'[a-zA-Z\-]*(\d+[\/\d\:]*)'
    result = re.match(pattern, string)
    if result:
        print(result.groups())
        name, number = list(result.groups())
        print(name, number)
    else:
       exit('No matches')
deviceRegex('GigabitEthernet1/3')
deviceRegex('tengigabitethernet7/1/25')
deviceRegex('Serial1/0/0/15:1')

