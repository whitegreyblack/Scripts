#!/bin/env python
'''
Author: Sam Whang
File  : accounts.py
Usage : python Accounts/accounts.py -i ransact -o transact.json
Info  : calculates debit and credit transactions to my bank account using 
        a csv file and prints remainder in every transaction line printed
'''
from funcutils import parse_date, valid_date
from collections import namedtuple
from namedlist import namedlist
from datetime import date
import sqlite3
import getopt
import json
import csv
import sys

# TODO:
# - Choose credit and/or debit
# - Single input/output file, uses respective file input name as both in/out files
# - Json is currently not writing new values to file -- fix soon
# - Input as debit card transactions (DC) or credit card transactions (CC)
#   Will allow for two types of transaction csv lists BOH vs AMEX
# - Question: Should we parse outside of main?

def main(argv):
    '''transforms csv transaction data into json for formatted printing'''

    # -- START FUNCTION VARIABLES --
    usage = """
    accounts.py -s <start> -e <end> -i <infile> -o <outfile> -c/-d
                -i, -o : input transaction csv file and/or json outfile
                -s, -e : start/end date formats [MM/DD/YYYY], [MM-DD-YYYY] 
                -d, -c : print either debit or credit statements, not both
    """[1:]

    fields = ("Account",
              "ChkRef",
              "Debit",
              "Credit",
              "Balance",
              "Date",
              "Description")

    translation_table = {}

    # Internal variables
    file_in = ""
    file_out = ""
    debit = True
    credit = True
    verbose = False
    date_format = "%m/%d/%Y"

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
    pcredit = "| {:4} | {:3} | {:7.2f} | " + GRN + "{:7.2f}" + END + " | {:7.2f} |"
    pdebit =  "| {:4} | {:3} | {:7.2f} | " + RED + "{:7.2f}" + END + " | {:7.2f} |"
    header =  "| Num  |   Date   |  Prev   | Amount  |  New    | Desc     |"
    spacer =  "+------+----------+---------+---------+---------+----------+"
    final =  "| {:35} |".format("Current Bank Balance") + " {:7.2f} |"
    p_months_in = "| {:32} ".format("Monthly Income") + "{:2} | {:7.2f} |"
    p_months_out = "| {:32} ".format("Monthly Expenses") + "{:2} | {:7.2f} |"
    p_months_avg = "| {:35} |".format("Monthly Average") + " {:7.2f} |"
    p_monthly_avgs_low = "| {:35} |".format("Monthly Avg") + GRN + " {:7.2f} " + END + "|"
    p_monthly_avgs_high = "| {:35} |".format("Monthly Avg") + RED + " {:7.2f} " + END + "|"
    p_monthly_gain = "| {:32} ".format("Monthly Net :- Gain") + "{:2} |" + GRN + "{:8.2f}" + END + " |"
    p_monthly_loss = "| {:32} ".format("Monthly Net :- Loss") + "{:2} |" + RED + "{:8.2f}" + END + " |"
    # -- END FUNCTION VARIABLES --

    # -- START INTERNAL FUNCTIONS --
    def monthly_stats(month, income, usage):
        '''Terminal output print if income and usage exists'''
        if income > 0.0 or usage > 0.0:
            print(spacer)

            if income > 0.0:
                print(p_months_in.format(transactions_in, income))

            if usage > 0.0:
                print(p_months_out.format(transactions_out, usage))

            net_total = income - usage

            if income > usage:
                print(p_monthly_gain.format(month, net_total))
            else:
                print(p_monthly_loss.format(month, net_total))

            print(spacer + "\n")
            monthly_average.append(net_total)

    def credit_transaction(credit, account):
        credit = float(credit)
        row = {}
        row['Type'] = "credit"
        row['Amount'] = credit
        row['Prev'] = balance - credit
        row['Change'] = balance
        account -= credit
        return account, row

    def debit_transaction(debit, account):
        debit = float(debit)
        row = {}
        row['Type'] = "debit"
        row["Amount"] = debit
        row["Prev"] = balance + debit
        row["Change"] = balance + debit
        account += debit
        # accrue debit per two weeks
        return account, row

    def transact_wrapper(transaction_func, transaction, account):
        try:
            return transaction_func(transaction, account)
        except ValueError as err:
            err.args = (transaction,)
            raise
    # -- END INTERNAL FUNCTIONS --
    
    # -- START ARGS PARSING --
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
        # raise ValueError("No output file has been specified")
        print("No output file specified -- no json will be saved")
    elif not file_out.endswith("json"):
        raise ValueError("Output file has wrong extension type: need json")
    
    if verbose:
        print("File Input : {}".format(file_in))
        print("File Output: {}".format(file_out))
        print("Start Date : {}".format(start.strftime(date_format)))
        print("End Date   : {}".format(end.strftime(date_format)))

        # pause to let user see verbose info before proceeding
        # we could just wait 5 seconds but this allows users to 
        # manually choose when to go to the next step
        input()

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
    with open(file_in, 'r') as csvfile:
        if file_out:
            with open(file_out, 'w') as jsonfile:
                account, header_check = None, False

                # loop through the csv line with given fields
                reader = csv.DictReader(csvfile, fields)

                # iterate through the csv file
                for row in reader:
                    if not header_check:
                        header_check = True
                    else:
                        # string formatting and correcting for valid dates
                        # during print to terminal
                        month, day, year = tuple(map(lambda x: int(x), 
                                               row['Date'].split('/')))
                        transact_date = date(year=year, month=month, day=day)
                        # reading backwards so pass until we're in range
                        # pass if outside of past end date
                        if transact_date >= end:
                            pass

                        # stop if past start date
                        if transact_date < start:
                            break

                        if not account:
                            account = float(row['Balance'])
                        transaction_number += 1

                        # checks if balance exists
                        balance = row['Balance']
                        if balance == "":
                            balance = account
                        else:
                            balance = float(balance)
                            
                        # reading the transaction
                        credit, debit = row['Credit'], row['Debit']
                        if credit:                  
                            account, new_row = transact_wrapper(credit_transaction,
                                                                credit,
                                                                account)
                        else:
                            account, new_row = transact_wrapper(debit_transaction,
                                                                debit,
                                                                account)
                            
                        new_row['Date'] = transact_date.strftime("%m/%d/%y")
                        new_row['New'] = account   
                        new_row["Desc"] = row["Description"]
                        transactions.append(new_row)

                        # write new_row to file
                        json.dump(new_row, jsonfile)
                        jsonfile.write('\n')
                
        # print(spacer+spacer_ext)
        print("Total Transactions Read and Processed: {}".format(
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
        # if valid_date(row['Date']):
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

        # Dont include service fees that is less than 1 dollar
        if row['Amount'] < 1.00:
            pass
        elif row['Type'].lower() == "credit":
            monthly_income += row['Amount']
            transactions_in += 1
            print(pcredit.format(transact_num,
                                    row['Date'],
                                    row['Prev'],
                                    row['Amount'],
                                    row['New']))
        else:
            monthly_usage += row['Amount']
            transactions_out += 1
            print(pdebit.format(transact_num,
                                row["Date"],
                                row['Prev'],
                                row['Amount'],
                                row['New']))

    monthly_stats(current_month, monthly_income, monthly_usage)

    print(spacer)
    print("| {:56} |".format("Statistics from selected months"))
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

# only call script if this script is the main script run
if __name__ == "__main__":
    main(sys.argv[1:])
