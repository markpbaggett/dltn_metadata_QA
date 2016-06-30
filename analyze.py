from pymongo import MongoClient
import argparse
import json

parser = argparse.ArgumentParser(description='Enter Your OAI Endpoint Information')
parser.add_argument("-f", "--field", dest="field", help="Specify DC Field", required=True)
parser.add_argument("-c", "--collection", dest="collection", help="What collection are we calling?")
parser.add_argument("-m", "--metadata_format", dest="metadata_format", help="Specify OAI metadata prefix",
                    required=True)
parser.add_argument("-o", "--operation", dest="operation", help="Choose operation: match, exists, or find.", required=True)
parser.add_argument("-s", "--string", dest="string_value", help="Enter a string to search on.")
args = parser.parse_args()


def find_matching_documents(format, collection, field, value):
    if format == "oai_dc":
        formatted_field = '{"metadata.' + format + ':dc.dc:' + field + '": "' + value + '"}'
    else:
        formatted_field = '{"metadata.' + format + '.' + field + '": "' + value + '"}'
    data = json.loads(formatted_field)
    matching_documents = collection.find(data)
    message = 'records with matching values'
    create_file(matching_documents, formatted_field, message)


def find_distinct(format, collection, field):
    if format == "oai_dc":
        formatted_field = 'metadata.' + format + ':dc.dc:' + field
    else:
        formatted_field = 'metadata.' + format + '.' + field
    cursor = collection.distinct(formatted_field)
    message = 'distinct values'
    create_file(cursor, formatted_field, message)


def create_file(parseable_object, field, system_string):
    total_records = 0
    text_file = open('result.txt', 'w')
    report = open('report.txt', 'w')
    if system_string == 'records missing this element':
        report.write('These records are missing a {0}:\n\n'.format(field))
    print('\nUnique values in {0} field:\n'.format(field))
    for document in parseable_object:
        print('\t{0}\n'.format(document))
        text_file.write('\n\n{0}\n'.format(document))
        if system_string == 'records missing this element':
            report.write('\n{1}. MODS: dpla.lib.utk.edu/repox/OAIHandler?verb=GetRecord&identifier={0}&metadataPrefix=MODS\n'.format(document['record_id'], total_records + 1))
            report.write('\n\tOAI_DC: dpla.lib.utk.edu/repox/OAIHandler?verb=GetRecord&identifier={0}&metadataPrefix=oai_dc\n\n'.format(document['record_id']))
        total_records += 1
    text_file.close()
    report.close()
    print('\nTotal {0}: {1}'.format(system_string, total_records))


def check_exists(format, collection, field):
    if format == "oai_dc":
        formatted_field = '{"metadata.' + format + ':dc.dc:' + field
    else:
        formatted_field = '{"metadata.' + format + '.' + field
    formatted_field += '": { "$exists" : false }}'
    data = json.loads(formatted_field)
    missing_elements = collection.find(data)
    message = 'records missing this element'
    create_file(missing_elements, formatted_field, message)


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
    if args.operation == 'exists':
        check_exists(metadata_format, mongo_collection, key)
    if args.operation == 'find':
        find_distinct(metadata_format, mongo_collection, key)

if __name__ == "__main__":
    main()
