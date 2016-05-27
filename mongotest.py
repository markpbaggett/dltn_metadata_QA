__author__ = 'mbagget1'
from pymongo import MongoClient
import sys
import argparse
reload(sys)
sys.setdefaultencoding('utf-8')

parser = argparse.ArgumentParser(description='Enter Your OAI Endpoint Information')
parser.add_argument("-f", "--field", dest="dc_field", help="Specify DC Field", required=True)
args = parser.parse_args()

dc_field = args.dc_field

client = MongoClient()
db = client.oaipublishers
cursor = db.oaipublishers.distinct(dc_field)
total_records = 0
text_file = open('uniquerecords.txt', 'w')
for document in cursor:
    print(document)
    text_file.write('{0}\n'.format(document))
    total_records += 1
text_file.close()
print('\n\n{0}'.format(total_records))
