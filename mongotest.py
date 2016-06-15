from pymongo import MongoClient
import argparse

parser = argparse.ArgumentParser(description='Enter Your OAI Endpoint Information')
parser.add_argument("-f", "--field", dest="field", help="Specify DC Field", required=True)
parser.add_argument("-c", "--collection", dest="collection", help="What collection are we calling?")
parser.add_argument("-m", "--metadata_format", dest="metadata_format", help="Specify OAI metadata prefix",
                    required=True)
args = parser.parse_args()

field = args.field
if args.collection:
    collection = args.collection
else:
    collection = "default"

client = MongoClient()
db = client.dltndata
metadata_format = args.metadata_format
mongocollection = db[collection]
if metadata_format == "oai_dc":
    formatted_field = 'metadata.' + metadata_format + ':dc.dc:' + field
else:
    formatted_field = 'metadata.' + metadata_format + '.' + field
cursor = mongocollection.distinct(formatted_field)
total_records = 0
text_file = open('uniquerecords.txt', 'w')
print('\nUnique values in {0} field:\n'.format(formatted_field))
for document in cursor:
    print('\t{0}\n'.format(document))
    text_file.write('\n\n{0}\n'.format(document))
    total_records += 1
text_file.close()
print('\nTotal distinct values: {0}'.format(total_records))
