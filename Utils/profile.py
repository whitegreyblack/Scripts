import platform

__author__  = "Sam WHang | WGB"
__email__   = "sangwoowhang@gmail.com"
__license__ = "MIT"

# Print color formatting
ORG = '\x1b[0;34;40m'
YEL = '\x1b[0;33;40m'
GRN = '\x1b[1;32;40m'
RED = '\x1b[1;31;40m'
DIM = '\x1b[2;49;90m'
END = '\x1b[0m'

attributes=[
        'architecture',
        'linux_distribution',
        'mac_ver',
        'machine',
        'node',
        'platform',
        'processor',
        'python_build',
        'python_compiler',
        'python_version',
        'release',
        'system',
        'version',
        'uname',
        ]

# helper functions for nested empty tuples
def flatten(x):
    return list(filter(lambda x: x != " ", sum(map(flatten, x), []) if isinstance(x, tuple) else [x]))

def empty(x):
    return all(t == '' for t in x)

if __name__ == "__main__":
    for attr in attributes:
        if hasattr(platform, attr):
            details = getattr(platform, attr)()
            if isinstance(details, platform.uname_result):
                details = ('\n' + " " * 22).join(['{:10} = {}'.format(k, getattr(details, k)) 
                    for k in details._fields])
            else:
                details = flatten(details)
                if empty(details):
                    details = ""
                else:
                    details = ("\n" + " " * 22).join(details)

            print("{:20}: {:<}".format(
                attr,
                YEL+ details + END))
