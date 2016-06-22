from pymongo import MongoClient
import argparse
import json

parser = argparse.ArgumentParser(description='Enter Your OAI Endpoint Information')
parser.add_argument("-f", "--field", dest="field", help="Specify DC Field", required=True)
parser.add_argument("-c", "--collection", dest="collection", help="What collection are we calling?")
parser.add_argument("-m", "--metadata_format", dest="metadata_format", help="Specify OAI metadata prefix",
                    required=True)
parser.add_argument("-o", "--operation", dest="operation", help="Choose operation.")
parser.add_argument("-s", "--string", dest="string_value", help="Enter a string to search on.")
args = parser.parse_args()

def find_matching_documents(format, collection, field, value):
    if format == "oai_dc":
        formatted_field = '{"metadata.' + format + ':dc.dc:' + field + '": "' + value + '"}'
    else:
        formatted_field = '{"metadata.' + format + '.' + field + '": "' + value + '"}'
    print(formatted_field)
    data = json.loads(formatted_field)
    matching_documents = collection.find(data)
    total_records = 0
    text_file = open('uniquerecords.txt', 'w')
    print('\nUnique values in {0} field:\n'.format(formatted_field))
    for document in matching_documents:
        print('\t{0}\n'.format(document))
        text_file.write('\n\n{0}\n'.format(document))
        total_records += 1
    text_file.close()
    print('\nTotal distinct values: {0}'.format(total_records))


def find_distinct(format, collection, field):
    if format == "oai_dc":
        formatted_field = 'metadata.' + format + ':dc.dc:' + field
    else:
        formatted_field = 'metadata.' + format + '.' + field
    cursor = collection.distinct(formatted_field)
    total_records = 0
    text_file = open('uniquerecords.txt', 'w')
    print('\nUnique values in {0} field:\n'.format(formatted_field))
    for document in cursor:
        print('\t{0}\n'.format(document))
        text_file.write('\n\n{0}\n'.format(document))
        total_records += 1
    text_file.close()
    print('\nTotal distinct values: {0}'.format(total_records))


def main():
    key = args.field
    if args.collection:
        collection = args.collection
    else:
        collection = "default"
    client = MongoClient()
    db = client.dltndata
    metadata_format = args.metadata_format
    mongo_collection = db[collection]
    string_value = args.string_value
    if args.operation == 'match':
        if string_value is None:
            print("\nMatch operations require both a key and a value.")
        else:
            find_matching_documents(metadata_format, mongo_collection, key, string_value)
    else:
        find_distinct(metadata_format, mongo_collection, key)

if __name__ == "__main__":
    # db.utk_master.find({'metadata.mods.accessCondition':'Public domain.'}).pretty()
    main()
