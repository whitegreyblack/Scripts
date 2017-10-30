#!/bin/env python
'''
Author: Sam Whang
File  : accounts.py
Usage : py accounts.py
Info  : calculates debit and credit transactions using a csv file
        and prints remainder in every transaction line printed
'''

from collections import namedtuple
from namedlist import namedlist
from datetime import date
import sqlite3
import json
import csv
import sys

# pre-check
if len(sys.argv) < 3:
    exit("Incorrect num of args")

# TODO: Extensions for script parsing and formatting
grammar = {}
grammar['+'] = {'+', 'plus', 'add'}

# Color format printing
ORG = '\x1b[0;34;40m'
YEL = '\x1b[0;33;40m'
GRN = '\x1b[1;32;40m'
RED = '\x1b[1;31;40m'
END = '\x1b[0m'

# string outputs used in printing
header = "| Transaction Type| Balance"
spacer = "+-----------------+------------------+----------------+----------+"
spacer_ext = "---------+---------+"
pcredit = "| " + GRN + "Credit" + END + ": {:7.2f} | \
Balance: {:7.2f} | Total: {:7.2f} | {:3} | {:7.2f} | {:7.2f} |"
pdebit = "| " + RED + "Debit" + END + ": {:8.2f} | \
Balance: {:7.2f} | Total: {:7.2f} | {:3} | {:7.2f} |         |"


# simple data structure: Transaction
transaction = namedlist('Transaction', 'balance')
fields = (
    "Account",
    "ChkRef",
    "Debit",
    "Credit",
    "Balance",
    "Date",
    "Description"
    )
# We start at one to correct for the number of transactions 
# placed on account offsetted by one to skip off-by-one errors
transactions = 1
# due to long transaction files print the header every 10-25 lines
header_print = 0
# load data from csv and transform to json
with open(sys.argv[1], 'r') as csvfile:
    with open(sys.argv[2], 'w') as jsonfile:
        monthly = 0
        account = None
        header_check = False
        # loop through the csv line with given fields
        reader = csv.DictReader(csvfile, fields)
        for row in reader:

            # write the info to json file
            json.dump(row, jsonfile)
            jsonfile.write('\n')

            # write the info to terminal 
            # header check skips first line
            # of csv that contains header
            if not header_check:
                header_check = True
            else:
                if not account:
                    account = transaction(float(row['Balance']))
                    print('Start: {}'.format(account.balance))
                transactions += 1
                print(spacer+spacer_ext)
                
                # checks if balance exists
                balance = row['Balance']
                if balance == "":
                    balance = account.balance
                else:
                    balance = float(balance)

                credit = row['Credit']
                debit = row['Debit']

                # string formatting and correcting for valid dates during print
                txdate = tuple(map(lambda x: int(x), row['Date'].split('/')))
                txdate = date(
                        year = txdate[2],
                        month = txdate[0],
                        day = txdate[1]).strftime("%m/%d/%y")

                if credit is not "":
                    credit = float(credit)
                    print(pcredit.format(
                        credit,
                        balance,
                        balance - credit,
                        txdate,
                        account.balance,
                        monthly))
                    account.balance -= credit
                    # credit transactions means two weeks
                    # so reset monthly calculations every
                    # two weeks
                    monthly = 0.00

                elif debit is not "":
                    debit = float(debit)
                    new_balance = balance + debit
                    print(pdebit.format(
                        debit,
                        balance,
                        balance + debit,
                        txdate,
                        monthly))
                    account.balance += debit
                    # accrue debit per two weeks
                    monthly += debit
        print(spacer+spacer_ext)

exit("Done writing")
with open('transactions.json', 'r') as transactions:
    line = transactions.readline()
    line = transactions.readline()

    if line:
        data = json.loads(line)
        account = tx(float(data['Balance']))
        print('Start: ', account.balance)

    monthly = 0
    while line:
        txn += 1
        data = json.loads(line)
        bx = data['Balance']
        cx = data['Credit']
        dx = data['Debit']

        bx = account.balance if bx is "" else float(bx)

        print(spacer)

        # Found a credit transaction
        if cx is not "":
            cx = float(cx)
            print(credit.format(cx,
                                bx,
                                bx - cx,
                                txn,
                                data['Date'],
                                monthly))
            account = tx(bx - cx)
            monthly = 0.00

        # found a debit transaction
        if dx is not "":
            dx = float(dx)
            print(debit.format(-dx,
                               bx,
                               bx + dx,
                               txn,
                               data['Date']))
            monthly += dx
            account = tx(bx + dx)

        line = transactions.readline()

    print(spacer)
    print("{:6.2f}".format(account.balance))
