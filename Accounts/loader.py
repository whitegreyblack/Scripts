import sqlite3
import json
import csv

csvfile = open('transactions.csv', 'r')
jsonfile = open('transactions.json', 'w')

fields = ("Account", "ChkRef", "Debit", "Credit", "Balance", "Date", "Description")
reader = csv.DictReader(csvfile, fields)
read=False
for row in reader:
    json.dump(row, jsonfile)
    jsonfile.write('\n')

jsonfile.close()
csvfile.close()
