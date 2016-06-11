__author__ = 'mbagget1'
from pymongo import MongoClient
import sys
import argparse

parser = argparse.ArgumentParser(description='Enter Your OAI Endpoint Information')
parser.add_argument("-f", "--field", dest="dc_field", help="Specify DC Field", required=True)
parser.add_argument("-c", "--collection", dest="collection", help="What database are we calling?")
args = parser.parse_args()

dc_field = args.dc_field
if args.collection:
    collection = args.collection
else:
    collection = "default"

client = MongoClient()
db = client.oaidc
mongocollection = db[collection]
cursor = mongocollection.distinct(dc_field)
total_records = 0
text_file = open('uniquerecords.txt', 'w')
print('\nUnique values in {0} field:\n'.format(dc_field))
for document in cursor:
    print('\t{0}\n'.format(document))
    text_file.write('\n\n{0}\n'.format(document))
    total_records += 1
text_file.close()
print('\nTotal distinct values: {0}'.format(total_records))
