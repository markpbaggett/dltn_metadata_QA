from lxml import etree
import argparse
from pymongo import MongoClient
import json
import xmltodict
import urllib

parser = argparse.ArgumentParser(description='Enter Your OAI Endpoint Information')
parser.add_argument("-u", "--url", dest="urlforoai", help="Specify your OAI endpoint")
parser.add_argument("-s", "--set", dest="oaiset", help="Specify your OAI set", required=True)
parser.add_argument("-m", "--metadata_prefix", dest="metadata_prefix", help="Specify metadata prefix", required=True)
parser.add_argument("-c", "--collection", dest="collection", help="Which collection?")
args = parser.parse_args()

client = MongoClient()
db = client.dltndata


def check_endpoint(url):
    document = etree.parse(url)
    error_code = document.findall('//{http://www.openarchives.org/OAI/2.0/}error')
    if len(error_code) == 1:
        print("\nThere is something wrong with your OAI-PMH endpoint. Make sure your set or metadata format exists. "
              "For more information about your error, see this url:\n\n{0}\n".format(url))
    else:
        grab_oai(url, session_token, total_records)


def grab_oai(url, token, num_of_records):
    document = etree.parse(url + token)
    new_session_token = document.findall('//{http://www.openarchives.org/OAI/2.0/}resumptionToken')
    request = urllib.request.urlopen(url+token)
    json_string = json.dumps(xmltodict.parse(request))
    json_document = json.loads(json_string)
    number_of_oai_records = len(json_document['OAI-PMH']['ListRecords']['record'])
    i = 0
    while i < number_of_oai_records:
        if 'metadata' in json_document['OAI-PMH']['ListRecords']['record'][i]:
            record_id = json_document['OAI-PMH']['ListRecords']['record'][i]['header']['identifier']
            metadata = json_document['OAI-PMH']['ListRecords']['record'][i]['metadata']
            result = mongocollection.insert_one({"record_id": record_id, "metadata": metadata})
            num_of_records += 1
        i += 1
    if len(new_session_token) == 1:
        resumption_token = '&resumptionToken={0}'.format(new_session_token[0].text)
        if resumption_token != '&resumptionToken=None':
            grab_oai(oai_endpoint, resumption_token, num_of_records)
    print('\nRecord creation complete. Created or updated {0} records.\n'.format(num_of_records))


if __name__ == "__main__":
    # Defaults
    oai_endpoint = 'http://dpla.lib.utk.edu:8080/repox/OAIHandler'
    metadata_prefix = '&metadataPrefix='
    oai_set = session_token = ''
    num_publishers = total_records = 0
    collection = "default"

    if args.urlforoai:
        oai_endpoint = args.urlforoai
    oai_set = oai_set + args.oaiset
    if args.collection:
        collection = args.collection
    mongocollection = db[collection]
    oai_endpoint = oai_endpoint + "?verb=ListRecords"
    metadata_prefix += args.metadata_prefix

    full_search_string = oai_endpoint + '&set=' + oai_set + metadata_prefix
    check_endpoint(full_search_string)
