import Transaction
import json
import csv

ORG = '\x1b[0;34;40m'
YEL = '\x1b[0;33;40m'
GRN = '\x1b[1;32;40m'
RED = '\x1b[1;31;40m'
END = '\x1b[0m'

dates=[]
header=True
balance=True
tx=1

spacer="+-----------------+------------------+----------------+-----+"
credit="| "+GRN+"Credit"+END+": {:7.2f} | Balance: {:7.2f} | Total: {:7.2f} | {:3} | {}"
debit="| "+RED+"Debit"+END+": {:8.2f} | Balance: {:7.2f} | Total: {:7.2f} | {:3} | {}"


with open('transactions.json','r') as transactions:
    account=Transaction.Transaction()
    line = transactions.readline()
    line = transactions.readline()

    if line:
        data = json.loads(line)
        account.set(float(data['Balance']))
        print('Start: ',account.balance) 

    while line:
        tx += 1
        data = json.loads(line)
        bx = data['Balance']
        cx = data['Credit']
        dx = data['Debit'] 
        
        bx = account.account() if bx is "" else float(bx)
        print(spacer)
        if cx is not "":
            cx = float(cx)
            print(credit.format(cx, bx, bx-cx, tx, data['Date']))
            account.credit(cx)
        
        if data['Debit'] is not "":
            dx = float(dx)
            print(debit.format(-dx, bx, bx+dx, tx, data['Date']))
            account.debit(dx)

        line=transactions.readline()

    print(spacer)
    print("{:6.2f}".format(account.account()))

