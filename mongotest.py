__author__ = 'mbagget1'
from pymongo import MongoClient
import sys
import argparse

parser = argparse.ArgumentParser(description='Enter Your OAI Endpoint Information')
parser.add_argument("-f", "--field", dest="dc_field", help="Specify DC Field", required=True)
parser.add_argument("-d", "--database", dest="database", help="What database are we calling?")
args = parser.parse_args()

dc_field = args.dc_field
if args.database:
    database = args.database
else:
    database = "oaipublishers"

client = MongoClient()
db = client.oaipublishers
cursor = db.database.distinct(dc_field)
total_records = 0
text_file = open('uniquerecords.txt', 'w')
for document in cursor:
    print(document)
    text_file.write('\n\n{0}\n'.format(document))
    total_records += 1
text_file.close()
print('\n\n{0}'.format(total_records))
