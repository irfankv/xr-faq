import pymongo
import os
import json
from datetime import datetime, timedelta
import time

client = pymongo.MongoClient('localhost',27017)

db = client.nft.ddts



'''
new query
 command ="/auto/qddtscache/qddtsnxt/bin/query.pl 'submitter-manager-org:suneets or submitter-manager-org:viruhonn and Status:S[170101:] '  | /auto/qddtscache/qddtsnxt/bin/qbugval.pl -json Identifier Project Status Severity Found Submitted-on DE-manager Component Submitter-id Submitter-manager-org Headline Product Attribute ENCLOSURES Version"
'''

while (True):

    db.remove({})

    command ="/auto/qddtscache/qddtsnxt/bin/query.pl 'submitter-manager-org:suneets or submitter-manager-org:viruhonn '  | /auto/qddtscache/qddtsnxt/bin/qbugval.pl -json Attribute Identifier Status Severity Found Submitted-on DE-manager Component Submitter-id Submitter-manager-org ENCLOSURES Headline Product Version"

    p = os.popen(command)
    output = p.read()
    output = json.loads(output)
    for record in output:
        submitted = record['Submitted-on']
        record['Submitted-on'] = submitted.split(' ')[0]
        version = record['Version'][:8]
        week = datetime.strptime(record['Submitted-on'], "%y%m%d")
        record['Submitted-week'] = week
        record['Version'] = version 
        endw = record['Submitted-week'] - timedelta(days=datetime(week.year, week.month, week.day).weekday())
        if "SS-Eval" in record['ENCLOSURES']:
            record['SS-Eval'] = "Y"
        else:
            record['SS-Eval'] = "N"
        if "TS-Eval" in record['ENCLOSURES']:
            record['TS-Eval'] = "Y"
        else:
            record['TS-Eval'] = "N"
        if ('TSHF-NFT' in record['Attribute']) or ('TSHF-IDT' in record['Attribute']) or ('TSHF-DEV' in record['Attribute']):            record['Leak-Present'] = "Y"
        else :
            record['Leak-Present'] = "N"
        record['Submitted-week'] = int(time.mktime(endw.timetuple()))

        end = datetime.strptime(record['Submitted-on'], "%y%m%d")
        endm = datetime.strptime(record['Submitted-on'][:4], "%y%m")
        record['Submitted-on'] = int(time.mktime(end.timetuple()))
        record['Submitted-onm'] = int(time.mktime(endm.timetuple())) + (8 * 3600)


        db.insert(record)

    # file = open('Temp.json', 'r')

    print ("done")


    time.sleep(86400)
