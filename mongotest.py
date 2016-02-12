__author__ = 'mbagget1'
from pymongo import MongoClient
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

client = MongoClient()
db = client.oaipublishers
cursor = db.oaipublishers.distinct("publisher")
total_records = 0
text_file = open('uniquerecords.txt', 'w')
for document in cursor:
    print(document)
    text_file.write('{0}\n'.format(document))
    total_records += 1
text_file.close()
print('\n\n{0}'.format(total_records))
