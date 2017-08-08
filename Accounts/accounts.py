from collections import namedtuple
import sqlite3
import json
import csv

# Color format printing
ORG = '\x1b[0;34;40m'
YEL = '\x1b[0;33;40m'
GRN = '\x1b[1;32;40m'
RED = '\x1b[1;31;40m'
END = '\x1b[0m'

# simple data structure: Transaction
tx=namedtuple('Transaction', ['balance'])
header=True
balance=True
txn=1

# load data from csv and transform to json
csvfile = open('transactions.csv', 'r')
jsonfile = open('transactions.json', 'w')

fields=("Account", "ChkRef", "Debit", "Credit", "Balance", "Date", "Description")

reader = csv.DictReader(csvfile, fields)
read=False

for row in reader:
    json.dump(row, jsonfile)
    jsonfile.write('\n')
jsonfile.close()
csvfile.close()

spacer="+-----------------+------------------+----------------+-----+"
credit="| "+GRN+"Credit"+END+": {:7.2f} |\
        Balance: {:7.2f} | Total: {:7.2f} | {:3} | {} | {:7.2f}"
debit ="| "+RED+"Debit"+END+": {:8.2f} |\
        Balance: {:7.2f} | Total: {:7.2f} | {:3} | {}"


with open('transactions.json','r') as transactions:
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
        
        if cx is not "":
            cx = float(cx)
            print(credit.format(cx, bx, bx-cx, txn, data['Date'], monthly))
            account = tx(bx-cx)
            monthly = 0.00
        
        if dx is not "":
            dx = float(dx)
            monthly += dx
            print(debit.format(-dx,
                                bx, 
                                bx+dx, 
                                txn, 
                                data['Date']))
            account = tx(bx+dx)
        line=transactions.readline()

    print(spacer)
    print("{:6.2f}".format(account.balance))
