import csv
import os
import string
from pymongo import MongoClient
import json
import time
from datetime import datetime
import pymongo
import ast

testbed = {}
client = MongoClient('localhost',27017)
db = client.issu.issu

count = 0

records = db.find({})

for record in records:
    print ( record)
    if record['version2'] == '6.1.99':
        if '6.1.3' in record['version1']:
            record['version2'] = '6.1.3.99'
        if '6.1.2' in record['version1']:
            record['version2'] = '6.1.2.99'
        if '5.2.6' in record['version1']:
            if '11/15/2016' in record['date'] or '11/16/2016' in record['date'] or '11/17/2016' in record['date']:
                record['version2'] = '6.1.2.99'
            else:
                record['version2'] = '6.1.3.99'

        print('changed record', record)
        db.remove({'ID': record['ID']})
        count += 1
        db.insert(record)
    elif record['version2'] == '6.2.99':
        if '6.2.' in record['version1']:
            record['version2'] = '6.2.1.99'
            print('changed record', record)
            db.remove({'ID': record['ID']})
            count += 1
            db.insert(record)
    elif record['version1'] == '6.1.99':
        if '6.1.3' in record['version2']:
            record['version1'] = '6.1.3.99'
        if '6.1.2' in record['version2']:
            record['version1'] = '6.1.2.99'

        print('changed record', record)
        db.remove({'ID': record['ID']})
        count += 1
        db.insert(record)


print (count)