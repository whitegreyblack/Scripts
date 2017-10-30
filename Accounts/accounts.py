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
import getopt
import json
import csv
import sys

usage = """
accounts.py -s <start> -e <end> -i <infile> -o <outfile> -c/-d
    -s, -e : date formats [MM/DD/YYYY], [MM-DD-YYYY] 
    -d, -c : print either debit or credit statements, not both
"""[1:]
    


def main(argv):
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
        ddate = date(year = ddate[2],
                    month = ddate[0],
                    day = ddate[1])
        return ddate

    def valid_date(ddate):
        """Date parsing used in final output date checking"""
        ddate = tuple(map(lambda x: int(x), ddate.split("/")))
        ddate = date(year = 2000+ddate[2],
                    month = ddate[0],
                    day = ddate[1])
        return start <= ddate <= end

    # Internal variables
    file_in = ""
    file_out = ""
    # TODO -- Choices for debit/credit
    debit = True
    credit = True
    verbose = False
    date_format = "%m/%d/%y"
    start = date(2015, 10, 27)
    end = date.today()

    # Color format printing
    GRN = '\x1b[1;32;40m'
    RED = '\x1b[1;31;40m'
    END = '\x1b[0m'

    # string outputs used in printing
    header = "  Num  |   Date   |   Transaction   |     Balance      | Total |"
    header_ext = " Balance | Monthly |"
    spacer = "+-----------------+------------------+----------------+----------+"
    spacer_ext = "---------+---------+"
    
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
        start = parse_date(start)
    elif verbose:
        print("Start date not entered -- using last entry in file as start")
    if end != date.today():
        end = parse_date(end)
    elif verbose:
        print("End date not entered   -- using today's date")
    if not file_in.endswith("csv"): 
        raise ValueError("Input file has wrong extension type: need csv")
    if not file_out.endswith("json"):
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
    
    # load data from csv and transform to json
    # we have to read twice since the order we want is not in the
    # correct order and reading backwards leaves open spaces in
    # the transaction history due to removal of data from history loss
    # so read from latest to earliest history to fill empty cells and 
    # then print from earliest to latest using calculated data

    with open(file_in, 'r') as csvfile:
        with open(file_out, 'w') as jsonfile:
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
                    txdate = tuple(map(
                                    lambda x: int(x), 
                                    row['Date'].split('/')))
                    txdate = date(
                            year = txdate[2],
                            month = txdate[0],
                            day = txdate[1]).strftime("%m/%d/%y")

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

    # read the file in reverse now to find out monthly income and expenses
    month = None
    current_month = None
    monthly_income = 0
    monthly_usage = 0
    monthly_average = []
    pcredit = "| {:4} | {:3} | {:7.2f} | "+GRN+"{:7.2f}"+END+" | {:7.2f} |"
    pdebit =  "| {:4} | {:3} | {:7.2f} | "+RED+"{:7.2f}"+END+" | {:7.2f} |"
    header =  "| Num  |   Date   |  Prev   | Amount  |  New    |"
    spacer =  "+------+----------+---------+---------+---------+"
    final =  "| Current Bank Balance                | {:7.2f} |"
    p_months_in = "| Monthly Income {:2}                   | {:7.2f} |"
    p_months_out = "| Monthly Expenses {:2}                 | {:7.2f} |"
    p_months_avg = "| Monthly Average                     | {:7.2f} |"
    p_monthly_avgs_low = "| Monthly Average                     \
|"+GRN+" {:7.2f} "+END+"|"
    p_monthly_avgs_high = "| Monthly Average                     \
|"+RED+" {:7.2f} "+END+"|"
    p_monthly_gain = "| Monthly Gain                        |"+GRN+"{:8.2f}"+END+" |"
    p_monthly_loss = "| Monthly Loss                        |"+RED+"{:8.2f}"+END+" |"

    # print initial headers
    print(spacer)
    print(header)
    print(spacer)

    # iterate through the rowsi and caluclate monthly costs and averages
    for num, row in enumerate(reversed(transactions)):

        if valid_date(row['Date']): 
            month = row['Date'].split('/')[0]

            if month != current_month:
                need_to_print = monthly_income > 0.0 or monthly_usage > 0.0

                if need_to_print:
                    print(spacer)
                    if monthly_income > 0.0:
                        print(p_months_in.format(current_month, monthly_income))
                        if monthly_usage > 0.0:
                            monthly_average.append(monthly_usage)

                    if monthly_usage > 0.0:
                        print(p_months_out.format(current_month, monthly_usage))

                    if monthly_income > monthly_usage:
                        print(p_monthly_gain.format(
                            monthly_income - monthly_usage))
                    else:
                        print(p_monthly_loss.format(
                            monthly_income - monthly_usage))

                    # reprint header information
                    print(spacer)
                    print()
                    print(spacer)
                    print(header)
                    print(spacer)

                # reset monthly statistics
                current_month = month
                monthly_income = 0
                monthly_usage = 0

            if row['Type'].lower() == "credit":
                monthly_income += row['Amount']
                print(pcredit.format(
                    num,
                    row['Date'],
                    row['Prev'],
                    row['Amount'],
                    row['New']))

            else:
                # Dont include service fees that equals less than 1 dollar
                if row['Amount'] < 1.00:
                    pass

                else:
                    monthly_usage += row['Amount']
                    print(pdebit.format(
                        num,
                        row["Date"],
                        row['Prev'],
                        row['Amount'],
                        row['New']))

    # final calculations after iterating through rows
    need_to_print = monthly_income > 0.0 or monthly_usage > 0.0

    if need_to_print:
        print(spacer)
        if monthly_income > 0.0:
            print(p_months_in.format(current_month, monthly_income))
            if monthly_usage > 0.0:
                monthly_average.append(monthly_usage)

        if monthly_usage > 0.0:
            print(p_months_out.format(current_month, monthly_usage))

        if monthly_income > monthly_usage:
            print(p_monthly_gain.format(
                monthly_income - monthly_usage))
        else:
            print(p_monthly_loss.format(
                monthly_income - monthly_usage))
        print(spacer)
        print()

    if monthly_usage > 0.0:
        monthly_average.append(monthly_usage)

    print(spacer)
    print("| {:45} |".format("Statistics from selected months"))
    print(spacer)
    average = sum(monthly_average) / len(monthly_average)
    if average < 1500:
        print(p_monthly_avgs_low.format(average))
    else:
        print(p_monthly_avgs_high.format(average))
    print(final.format(row['New']))
    print(spacer)
    exit("Finished")

if __name__ == "__main__":
    main(sys.argv[1:])
