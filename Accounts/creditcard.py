#!/bin/env python
'''
Author: Sam Whang
File  : creditcard.py
Usage : python Accounts/credditcard.py -i transactions.csv -o transact.json
Info  : calculates credit card transactions using a csv file
        and prints remainder in every transaction line printed
        Uses the same engine as accounts but since the csv's differ, had to
        move functionality to a new script
'''
from collections import namedtuple
from namedlist import namedlist
from datetime import date
import sqlite3
import getopt
import json
import csv
import sys

# -- START SCRIPT VARIABLES --
usage = """
creditcard.py -s <start> -e <end> -i <infile> -o <outfile> -c/-d
              -i, -o : input transaction csv file and/or json outfile
              -s, -e : start/end date formats [MM/DD/YYYY], [MM-DD-YYYY] 
              -d, -c : print either debit or credit statements, not both
"""[1:]
date_format = "%m/%d/%y"
dateday = namedtuple("Dateday", "month date year day")

def main(argv):
    fields = ("Dateday",
              "",
              "Description",
              "",
              "",
              "",
              "",
              "Amount",
              "",
              "",
              "Category",
              "Seller",
              "Location",
              "SellerID",
              "Transaction")

    translation_table = {}

    # Internal variables
    file_in = ""
    file_out = ""
    debit = True
    credit = True
    verbose = False
    date_format = "%m/%d/%y"

    # Start/End used in date checking when specific dates are 
    # entered through command line
    start = date(2015, 10, 27)
    end = date.today()

    verbose = False
    try:
        opts, args = getopt.getopt(argv, "cdhve:i:o:s:", ["fin=", "fout="])
    except getopt.GetoptError:
        exit(usage)
        
    for opt, arg in opts:
        if opt == "-h":
            exit(usage)
        # elif opt in ("-v", "--verbose"):
        #     verbose = True
        # elif opt in ("-d", "--debit"):
        #     credit = False
        # elif opt in ("-c", "--credit"):
        #     debit = False
        elif opt in ("-s", "--start"):
            start = arg
        elif opt in ("-e", "--end"):
            end = arg
        # elif opt in ("-i", "--infile"):
        #     file_in = arg
        # elif opt in ("-o", "--outfile"):
        #     file_out = arg
# only call script if this script is the main script run
if __name__ == "__main__":
    main(sys.argv[1:])