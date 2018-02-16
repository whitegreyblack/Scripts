#!/bin/env python
'''
File    : korean number parser
Desc    : parses input integer into korean words
Author  : Sam Whang | WGB
License : MIT
'''

import sys
import re

COMMA = ','
PERIOD = '.'
class ValueType:
    SMALLINT = "SMALL INT"
    LARGEINT = "LARGE INT"
    DECIMAL = "FLOAT"
    CURRENCY = "MONEY"
    DATE = "DATE"

SMALLINT, LARGEINT, DECIMAL, CURRENCY, DATE = range(5)

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

    value, vtype = None, None
    # maybe large number
    if COMMA in args:
        value = args.split(',')
        vtype = ValueType.LARGEINT
        print(value)

    if PERIOD in args:
        # maybe decimal, maybe EU style number
        if args.count(PERIOD) == 1:
            # try decimal
            value = args.split(',')
            vtype = ValueType.DECIMAL
        else:
            value = args.split(',')
            vtype = ValueType.LARGEINT

    print('V', value, vtype)

    args = args.replace(',', '')
    print(args)

    number = is_number(args)
    if number:
        print(number)
    else:
        currency = is_currency(args)
        if currency:
            print(currency)

    # if args.startswith('$'):
    #     print('money')
    # elif args.


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        parser(sys.argv[1])
    else:
        print("No input parameter detected")
        
