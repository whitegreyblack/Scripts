#!/bin/env python
'''
File    : korean number parser
Desc    : parses input integer into korean words
Author  : Sam Whang | WGB
License : MIT
'''

import sys
import re

numerical = r"^(?:\$){0,1}(?:\d{0,3})(?:(?:\.\d{3})*|(?:\,\d{3})*|(?:\d)*)(?:\.\d{2}){0,1}$"

def parser(args):
    '''Takes in a number of different inputs relating to numbers and tries to
    convert them into korean words.
    1. Numbers: 
        1 | 12141 | 12,141 | 12.141 | 142,123,132.00
    2. Currency: 
        $123123, $12,241
    3. Dates

    How it works:
        If it is a numerical input (Number/Currency) there are various styles
        and formats on how to represent these values. Testing as we go for
        inclusion and valid inputs will be the fastest method in determining
        what type of input was recieved by the parser.

        Once number parsing has been completed. Detecting currency should not 
        be too hard. We find if the value starts with a Dollar or Won symbol.
    '''

    def is_number(arg):
        try:
            value = int(arg)
        except ValueError:
            return False
        else:
            return value

    def is_currency(arg):
        if arg.startswith('$'):
            value = arg.replace('$', '')
            return is_number(value)
        return False

    print(args)
    
    if re.match(numerical, args):
        if args.startswith('$'):
            print('mon')
        else:
            print('num')
    # elif re.match(dateformat, args):


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        parser(sys.argv[1])
    else:
        print("No input parameter detected")
        
