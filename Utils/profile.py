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
    '''Returns a 1D list constructed from a tuple of nested tuples'''
    return list(filter(
        lambda x: x != " ", sum(map(flatten, x), []) if isinstance(x, tuple) else [x]))

def empty(x):
    '''Returns a newline delimited string if the input list has no spaces'''
    return ("\n"+ " " * 22).join(x) if not all(t == '' for t in x) else ""

if __name__ == "__main__":
    for attr in attributes:
        if hasattr(platform, attr):
            details = getattr(platform, attr)()

            # Check for uname_result -- only case in which attribute is not of type tuple
            if isinstance(details, platform.uname_result):
                details = ('\n' + " " * 22).join(['{:10} = {}'.format(k, getattr(details, k)) 
                    for k in details._fields])
            else:
                details = empty(flatten(details))

            print("{:20}: {:<}".format(
                attr,
                YEL+ details + END))
