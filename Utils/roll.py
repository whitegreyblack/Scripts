#!/usr/bin/env python
import re
import click
import random
import datetime
__author__  = "Sam Whang"
__email__   = "sangwoowhang@gmail.com"

# make sure pseudorandom number is based on non-reoccuring pattern
random.seed(datetime.datetime.now())

header = "roll: "
footer = "..... "
direct = "Type 'exit' to exit"
invalid_input = "Invalid Input"
di_regex_helper = "[1-9]d[1-n][+-][1-n]"
program_usage = "USAGE: roll.py [-r DICE STRING] | [-i] | [--help]"

dice_str_regex = re.compile(r'^(\d*\s*)d(\s*\d+\s*)(\s*[+-]\s*\d+)?$')

def parse(pattern):
    ''' Checks the input pattern to parse the type of die to use'''
    dice = [int(x) for x in re.findall(r'[\d]+', pattern)]
    bonus_sign = re.findall(r'[\W]', pattern)
    di_only = sum([random.randint(1, dice[1]) for _ in range(dice[0])])
    bonus = 0
    if len(dice) > 2:
        bonus = int(bonus_sign.pop() + str(dice[2]))

    return di_only + bonus

def output(p, prev=header):
    if dice_str_regex.match(p):
        message = f"{prev} {parse(p)}"
    else:
        message = f"{prev}{invalid_input}\n{footer}{di_regex_helper}"
    print(message)

@click.command()
@click.option('-r', 'roll', default=None, help=di_regex_helper)
@click.option('-i', 'inputflag', is_flag=True, help='Continuous Input')
def roll(roll, inputflag):
    ''' Main driver program '''
    # possibly only one roll
    if not inputflag:
        if roll:
            output(roll)
        else:
            # no arguments given, print program usage string
            print(program_usage)
    # could be n + 1 rolls, check roll variable first
    else:
        if roll:
            output(roll, footer)
        while 1:
            try:
                rollin = input(header)
            except KeyboardInterrupt:
                print("Goodbye and happy rolling!")
                break
            if rollin == 'exit': 
                break
            output(rollin)

if __name__ == "__main__":
    roll()
