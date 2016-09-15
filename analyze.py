from pymongo import MongoClient
import argparse
import json

parser = argparse.ArgumentParser(description='Enter Your OAI Endpoint Information')
parser.add_argument("-f", "--field", dest="field", help="Specify DC Field", required=True)
parser.add_argument("-c", "--collection", dest="collection", help="What collection are we calling?")
parser.add_argument("-m", "--metadata_format", dest="metadata_format", help="Specify prefix: oai_dc, oai_qdc, oai_etdms,"
                                                                            "mods, or digital_commons", required=True)
parser.add_argument("-o", "--operation", dest="operation", help="Choose operation: match, exists, or find.",
                    required=True)
parser.add_argument("-s", "--string", dest="string_value", help="Enter a string to search on.")
args = parser.parse_args()


def find_matching_documents(formatted_mongo_parameter, collection, value):
    formatted_mongo_parameter = '{"' + formatted_mongo_parameter + '": "' + value + '"}'
    data = json.loads(formatted_mongo_parameter)
    matching_documents = collection.find(data)
    message = 'records with matching values'
    create_file(matching_documents, formatted_mongo_parameter, message)


def find_distinct(formatted_mongo_parameter, collection):
    cursor = collection.distinct(formatted_mongo_parameter)
    message = 'distinct values'
    create_file(cursor, formatted_mongo_parameter, message)


def create_file(parseable_object, field, system_string):
    total_records = 0
    text_file = open('result.txt', 'w')
    report = open('report.md', 'w')
    markdown_header = mark_it_down(system_string, field)
    report.write(markdown_header)
    print('\nUnique values in {0} field:\n'.format(field))
    for document in parseable_object:
        print('\t{0}\n'.format(document))
        text_file.write('\n\n{0}\n'.format(document))
        if system_string != 'distinct values':
            if 'mods' in document['metadata']:
                try:
                    document_title = document['metadata']['mods']['titleInfo']['title']
                except:
                    document_title = "Not Defined in MODS Record"
                report.write('{0}. [{1}]({2}?verb=GetRecord&identifier={3}'
                             '&metadataPrefix=MODS)\n'.format(total_records + 1,
                                                              document_title,
                                                              document['oai_provider'],
                                                              document['record_id']))
            elif 'oai_dc:dc' in document['metadata']:
                try:
                    document_title = document['metadata']['oai_dc:dc']['dc:title']
                except:
                    document_title = "Not Defined in Metadata Record"
                report.write('{0}. [{1}]({2}?verb=GetRecord&identifier={3}'
                             '&metadataPrefix=oai_dc)\n'.format(total_records + 1,
                                                                document_title,
                                                                document['oai_provider'],
                                                                document['record_id']))
            elif 'thesis' in document['metadata']:
                try:
                    document_title = document['metadata']['thesis']['title']
                except:
                    document_title = "Not Defined in Metadata Record"
                report.write('{0}. [{1}]({2})\n'.format(total_records + 1,
                                                                document_title,
                                                                document['metadata']['thesis']['identifier']))
            else:
                report.write('{1}. {0}\n'.format(document, total_records + 1))
        else:
            report.write('{1}. {0}\n'.format(document, total_records + 1))
        total_records += 1
    text_file.close()
    report.close()
    print('\nTotal {0}: {1}'.format(system_string, total_records))


def check_exists(mongo_string, collection, boolean):
    formatted_field = '{"' + mongo_string + '": { "$exists" : ' + boolean + ' }}'
    print(formatted_field)
    data = json.loads(formatted_field)
    missing_elements = collection.find(data)
    if boolean == 'false':
        message = 'records missing this element'
    else:
        message = 'records with this element'
    create_file(missing_elements, formatted_field, message)


def format_metadata(prefix, field):
    if prefix == "oai_dc" or prefix == "simple-dublin-core":
        formatted_field = 'metadata.' + prefix + ':dc.dc:' + field
    elif prefix == "mods":
        formatted_field = 'metadata.' + prefix + '.' + field
    elif prefix == "oai_qdc":
        formatted_field = 'metadata.' + prefix + ':qualifieddc.' + field
    elif prefix == "oai_etdms":
        formatted_field = 'metadata.thesis.' + field
    elif prefix == "digital_commons":
        formatted_field = 'metadata.document.' + field
    elif prefix == "dpla":
        formatted_field = 'metadata.' + field
    else:
        print('This metadata format is not currently supported. '
              'Feel free to add an issue to the GitHub tracker.')
    return formatted_field


def mark_it_down(checker, key):
    header_string = "# Report\n---\n"
    if checker == 'records missing this element':
        header_string += "These records are missing a {0}:\n\n".format(key)
    elif checker == 'records with matching values':
        header_string += "These records match the field and string value you provided:\n\n"
    elif checker == 'distinct values':
        header_string += "These are the distinct values associated with {0}:\n\n".format(key)
    return header_string


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
    mongo_parameter = format_metadata(metadata_format, key)
    if args.operation == 'match':
        if string_value is None:
            print("\nMatch operations require both a key and a value.")
        else:
            find_matching_documents(mongo_parameter, mongo_collection, string_value)
    elif args.operation == 'missing':
        check_exists(mongo_parameter, mongo_collection, 'false')
    elif args.operation == 'exists':
        check_exists(mongo_parameter, mongo_collection, 'true')
    elif args.operation == 'find':
        find_distinct(mongo_parameter, mongo_collection)
    else:
        print("Missing an operation.")

if __name__ == "__main__":
    main()
