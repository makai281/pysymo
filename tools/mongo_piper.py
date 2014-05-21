#!/usr/bin/python

import sys
import json
from pymongo import MongoClient
from datetime import datetime

MONGO_HOST = '127.0.0.1'
MONGO_PORT = 27017
MONGO_DATABASE = 'syslog'

db = MongoClient(host=MONGO_HOST, port=MONGO_PORT)[MONGO_DATABASE]

try:
    while 1:
	line = sys.stdin.readline()
	if not line:
	    break
	# 1) fix \' strings
	data = json.loads(line.decode('string_escape'))
	# 2) convert UNIXTIME to Python datetime
	data['d'] = datetime.fromtimestamp(data['d'])

	db['messages'].insert(data)

except Exception, e:
    f = open('/usr/local/bin/error.txt','ab')
    f.write(e.message)
    f.write('\n')
    f.write(line)
    f.close()
    exit(0)
