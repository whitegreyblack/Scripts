#!/bin/env python
'''
Author: Sam Whang
File  : accounts.py
Usage : py accounts.py
Info  : calculates debit and credit transactions using a csv file
        and prints remainder in every transaction line printed
Cmd   : python Accounts/accounts.py  -i Accounts/transact-17-10-30.csv -o Accounts/transact.json
'''

from collections import namedtuple
from namedlist import namedlist
from datetime import date
import sqlite3
import getopt
import json
import csv
import sys

# TODO:
# Choose credit and/or debit
# Single input/output file, uses respective file input name as both in/out files
# Json is currently not writing new values to file -- fix soon

usage = """
accounts.py -s <start> -e <end> -i <infile> -o <outfile> -c/-d
    -s, -e : date formats [MM/DD/YYYY], [MM-DD-YYYY] 
    -d, -c : print either debit or credit statements, not both
"""[1:]
    
# Internal variables
file_in = ""
file_out = ""
debit = True
credit = True
verbose = False
date_format = "%m/%d/%y"

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

# Start/End used in date checking when specific dates are 
# entered through command line
start = date(2015, 10, 27)
end = date.today()

# variables used in printouts
current_month = None
monthly_income = 0
transactions_in = 0
monthly_usage = 0
transactions_out = 0
monthly_average = []

# Color format printing
GRN = '\x1b[1;32;40m'
RED = '\x1b[1;31;40m'
END = '\x1b[0m'

# strings for printing
pcredit = "| {:4} | {:3} | {:7.2f} | "+GRN+"{:7.2f}"+END+" | {:7.2f} |"
pdebit =  "| {:4} | {:3} | {:7.2f} | "+RED+"{:7.2f}"+END+" | {:7.2f} |"
header =  "| Num  |   Date   |  Prev   | Amount  |  New    |"
spacer =  "+------+----------+---------+---------+---------+"
final =  "| {:35} |".format("Current Bank Balance") + " {:7.2f} |"
p_months_in = "| {:32} ".format("Monthly Income") + "{:2} | {:7.2f} |"
p_months_out = "| {:32} ".format("Monthly Expenses") + "{:2} | {:7.2f} |"
p_months_avg = "| {:35} |".format("Monthly Average") + " {:7.2f} |"
p_monthly_avgs_low = "| {:35} |".format("Monthly Avg") + GRN + " {:7.2f} " + END + "|"
p_monthly_avgs_high = "| {:35} |".format("Monthly Avg") + RED + " {:7.2f} " + END + "|"
p_monthly_gain = "| {:32} ".format("Monthly Net :- Gain") + "{:2} |" + GRN + "{:8.2f}" + END + " |"
p_monthly_loss = "| {:32} ".format("Monthly Net :- Loss") + "{:2} |" + RED + "{:8.2f}" + END + " |"

def main(argv):
    '''transforms csv transaction data into json for formatted printing'''

    def parse_date(ddate):
        """Error checking for input dates"""
        if "/" in ddate:
            ddate = ddate.split("/")
        elif "-" in ddate:
            ddate = ddate.split("-")
        else:
            raise ValueError("Date contains invalid seperator")

        try:
            ddate = tuple(map(lambda x: int(x), ddate))
        except ValueError:
            raise ValueError("Date contains invalid variables types")

        if len(ddate) != 3:
            raise ValueError("Date contains invalid number of variables")

        # All errors have been safely checked -- now create a valid date object
        ddate = date(
            year = ddate[2], 
            month = ddate[0],
            day = ddate[1]
        )

        return ddate

    def valid_date(ddate):
        """Date parsing used in final output date checking"""
        ddate = tuple(map(lambda x: int(x), ddate.split("/")))
        ddate = date(
            year = 2000 + ddate[2],
            month = ddate[0],
            day = ddate[1]
        )

        return start <= ddate <= end

    def monthly_stats(month, income, usage):
        '''Terminal output print if income and usage exists'''
        if income > 0.0 or usage > 0.0:
            print(spacer)
            
            if income > 0.0:
                print(p_months_in.format(
                    transactions_in, income))

            if usage > 0.0:
                print(p_months_out.format(
                    transactions_out, usage))

            net_total = income - usage

            if income > usage:
                print(p_monthly_gain.format(month, net_total))
            else:
                print(p_monthly_loss.format(month, net_total))

            print(spacer)
            print()

            monthly_average.append(net_total)

    # args parsing
    try:
        opts, args = getopt.getopt(argv, "cdhve:i:o:s:", ["fin=", "fout="])
    except getopt.GetoptError:
        exit(usage)
        
    for opt, arg in opts:
        if opt == "-h":
            exit(usage)
        elif opt in ("-v", "--verbose"):
            verbose = True
        elif opt in ("-d", "--debit"):
            credit = False
        elif opt in ("-c", "--credit"):
            debit = False
        elif opt in ("-s", "--start"):
            start = arg
        elif opt in ("-e", "--end"):
            end = arg
        elif opt in ("-i", "--infile"):
            file_in = arg
        elif opt in ("-o", "--outfile"):
            file_out = arg

    # argument post-checks
    # valid dates: parse and error check
    if not (debit or credit):
        raise ValueError("To output both debit and credit -- omit c & d")
    
    if start != date(2015, 10, 27):
        if verbose:
            print("Start date not entered -- using last entry in file as start")
        
        start = parse_date(start)

    if end != date.today():
        if verbose:
            print("End date not entered   -- using today's date")
        
        end = parse_date(end)
    
    if start > end:
        raise ValueError("Start date is more recent than End date")

    if file_in == "":
        raise ValueError("No input file has been specified")
    elif not file_in.endswith("csv"): 
        raise ValueError("Input file has wrong extension type: need csv")
    
    if file_out == "":
        raise ValueError("No output file has been specified")
    elif not file_out.endswith("json"):
        raise ValueError("Output file has wrong extension type: need json")
    
    if verbose:
        print("File Input : {}".format(file_in))
        print("File Output: {}".format(file_out))
        print("Start Date : {}".format(start.strftime(date_format)))
        print("End Date   : {}".format(end.strftime(date_format)))

    # We start at one to correct for the number of transactions 
    # placed on account offsetted by one to skip off-by-one errors
    transaction_number = 1

    # due to long transaction files print the header every time
    # number of debit followed by credit is longer than 15
    header_print = 0
    transactions = []
    
    # we have to read twice since the order we want is not in the
    # correct order and reading backwards leaves open spaces in
    # the transaction history due to removal of data from history loss
    # so read from latest to earliest history to fill empty cells and 
    # then print from earliest to latest using calculated data
    with open(file_in, 'r') as csvfile, open(file_out, 'w') as jsonfile:
        account = None
        header_check = False

        # loop through the csv line with given fields
        reader = csv.DictReader(csvfile, fields)

        # iterate through the csv file
        for row in reader:
            if not header_check:
                header_check = True

            else:
                # write the info to json file
                json.dump(row, jsonfile)
                jsonfile.write('\n')

                if not account:
                    account = transaction(float(row['Balance']))

                transaction_number += 1

                # checks if balance exists
                balance = row['Balance']
                if balance == "":
                    balance = account.balance
                else:
                    balance = float(balance)

                credit = row['Credit']
                debit = row['Debit']

                # string formatting and correcting for valid dates 
                # during print to terminal
                m, d, y = tuple(map(
                                    lambda x: int(x), 
                                    row['Date'].split('/')))

                txdate = date(
                            year = y,
                            month = m,
                            day = d).strftime("%m/%d/%y")
                
                # txdate = tuple(map(
                #                 lambda x: int(x), 
                #                 row['Date'].split('/')))
                # txdate = date(
                #         year = txdate[2],
                #         month = txdate[0],
                #         day = txdate[1]).strftime("%m/%d/%y")

                # reading a credit transaction
                if credit is not "":
                    new_row = {}
                    new_row['Type'] = "credit"
                    new_row['Amount'] = float(credit)
                    new_row['Prev'] = balance - float(credit)
                    new_row['Change'] = balance
                    new_row['Date'] = txdate
                    new_row['New'] = account.balance
                    transactions.append(new_row)
                    account.balance -= float(credit)
                    # credit transactions means two weeks
                    # so reset monthly calculations every
                    # two weeks

                # reading a debit transaction
                elif debit is not "":
                    new_row = {}
                    new_row['Type'] = "debit"
                    new_row["Amount"] = float(debit)
                    new_row["Prev"] = balance + float(debit)
                    new_row["Change"] = balance + float(debit)
                    new_row["Date"] = txdate
                    new_row["New"] = account.balance
                    transactions.append(new_row)
                    account.balance += float(debit)
                    # accrue debit per two weeks
                    header_print += 1

        # print(spacer+spacer_ext)
        print("Total Transactions Read Processed: {}".format(
            transaction_number))

    # print header information
    print(spacer)
    print(header)
    print(spacer)

    # TODO: write monthly budget information in json format

    # read the file in reverse now to find out monthly income and expenses
    # iterate through the rows and calculate monthly costs and averages
    for transact_num, row in enumerate(reversed(transactions)):
        
        # check for valid dates and parse if true
        if valid_date(row['Date']): 
            month = parse_date(row['Date']).month
            
            if month != current_month:
                # we can skip printing if we do not detect any changes in 
                # balance during the month
                monthly_stats(current_month, monthly_income, monthly_usage)

                if monthly_income > 0.0 or monthly_usage > 0.0:
                    print(spacer)
                    print(header)
                    print(spacer)

                # reset monthly statistics
                current_month = month
                monthly_income = 0
                monthly_usage = 0
                transactions_in = 0
                transactions_out = 0

            # Dont include service fees that equals less than 1 dollar
            if row['Amount'] < 1.00:
                pass

            elif row['Type'].lower() == "credit":
                monthly_income += row['Amount']
                transactions_in += 1
                print(pcredit.format(
                    transact_num,
                    row['Date'],
                    row['Prev'],
                    row['Amount'],
                    row['New']))

            else:
                monthly_usage += row['Amount']
                transactions_out += 1
                print(pdebit.format(
                    transact_num,
                    row["Date"],
                    row['Prev'],
                    row['Amount'],
                    row['New']))

    monthly_stats(current_month, monthly_income, monthly_usage)

    print(spacer)
    print("| {:45} |".format("Statistics from selected months"))
    print(spacer)

    if monthly_average:
        average = sum(monthly_average) / len(monthly_average)
        if average > 0.0:
            print(p_monthly_avgs_low.format(average))
        else:
            print(p_monthly_avgs_high.format(average))

    print(final.format(row['New']))
    print(spacer)
    exit("Finished")

if __name__ == "__main__":
    main(sys.argv[1:])
