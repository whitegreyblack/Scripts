#!/usr/bin/env python

import re
import click
from datetime import datetime
from random import seed
from random import randint as rint
__author__  = "Sam WHang | WGB"
__email__   = "sangwoowhang@gmail.com"
__license__ = "MIT"

# make sure pseudorandom number is based on non-reoccuring pattern
seed(datetime.now())

header = 'roll: '
follow = '....  '
direct = 'Type "exit" to exit'
iinput = 'Invalid Input'
dihelp = '[1-10]d[1-n][+-][1-n]'
pusage = 'Usage: roll.py [-r DICE] | [-i] | [--help]'
dregex = re.compile(r'^(\d*\s*)d(\s*\d+\s*)(\s*[+-]\s*\d+)?$')

def match(pattern):
    ''' Checks the input pattern to parse the type of die to use'''
    d, b = re.findall(r'[\d]+', pattern), re.findall(r'[\W]', pattern)
    return sum([rint(1,int(d[1])) for _ in range(int(d[0]))])+(int(b[0]+d[2]) if len(d)>2 else 0)

@click.command()
@click.option('-r', default=None, help=dihelp)
@click.option('-i', is_flag=True, help='Continuous Input')
def roll(r, i):
    ''' Main driver program '''
    def out(p,prev=header): 
        print('{}{}'.format(header, match(p)) if dregex.match(p) else ('{}{}\n{}{}'.format(prev,iinput,follow,dihelp)))
    if r is None and not i:
        print(pusage)
    if i:
        print('{}{}'.format(header, direct) if r is None else ('{}{}'.format(header, direct)))
        if r:
            out(r, follow)
        while 1:
            r = input(header)
            if r == 'exit': 
                break
            out(r)
    if r:
        out(r)

if __name__ == "__main__":
    # run only when called
    roll()
