#!/bin/env python
'''
File    : korean number parser
Desc    : parses input integer into korean words
Author  : Sam Whang | WGB
License : MIT
'''

import sys
import re

placements = {
    10: ('ship', '십'),
    100: ('baek', '백'),
    1000: ('chun', '천'),
    10000: ('maan', '만'),
}

numbers = {
    1: ('il', '일'),
    2: ('ee', '이'),
    3: ('ssam', '삼'),
    4: ('ssa', '사'),
    5: ('ooh', '오'),
    6: ('yuuk', '육'),
    7: ('chil', '칠'),
    8: ('pal', '팔'),
    9: ('gu', '구'),
}

days_in_week = {
    'sunday': ('ee-ryoil', '일요일'),
    'monday': ('wur-yoi','월요일'),
    'tuesday': ('','화요일'),
    'wednesday': ('','수요일'),
    'thursday': ('',''),
    'friday': ('',''),
    'saturday': ('',''),
}

# these regex specifiers are combined 
# -- we could split them up and have a huge if-else chain
num_regex = r"^(?:\$){0,1}(?:\d{0,3})(?:(?:\.\d{3})*|(?:\,\d{3})*|(?:\d)*)(?:\.\d{2}){0,1}$"
dateregex = r"(?:(?:\d{0,2}\/){1,2}|(?:\d{0,2}\-){1,2})(?:\d{4}|\d{2})"
day_regex = r"^({})$".format('|'.join(days_in_week))
space = " "

def convert(number, i, placement):
    string = numbers[number][i]
    if placement in placements.keys():
        string += (space if i == 0 else '') + placements[placement][i]
    if placement != 1:
        string += space
    return string

def get_strings(args, val=2):
    both = val == 2
    strings = ["", ""] if both else ["",]
    for i, num in enumerate(args):
        num = int(num)
        if num in numbers.keys():
            placement = 10 ** (len(args) - i - 1)
            for i in range(len(strings)):
                strings[i] += convert(num, i if both else val, placement)
    return strings

if __name__ == "__main__":
    """Takes in a number of different inputs relating to numbers and tries to
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

        If any of the numbers pass either the number or currency regex match
        then we save the input type and strip the number of any special chars.
        We only want to work with the number inputs. We can format after we 
        finish working on the numbers.
    """
    if len(sys.argv) >= 2:
        val = None
        if len(sys.argv) == 2:
            args = sys.argv[1]
        elif len(sys.argv) == 3:
            args, val = sys.argv[1:3]
            if not 0 <= int(val) <= 2:
                raise ValueError("2nd parameter is incorrect. Must be between 0-2")

        if bool(re.match(num_regex, args)):
            if args.startswith('$'):
                args.replace('$', '')
            for string in get_strings(args, int(val)):
                print(string)

        elif bool(re.match(dateregex, args)):
            print('date')

        elif bool(re.match(day_regex, args)):
            print('day')
            
        else:
            print('Invalid input')

    else:
        print("No input parameter detected")