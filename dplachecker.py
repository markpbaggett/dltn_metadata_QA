__author__ = 'mbagget1'

from lxml import etree
import argparse
from pymongo import MongoClient

parser = argparse.ArgumentParser(description='Enter Your OAI Endpoint Information')
parser.add_argument("-u", "--url", dest="urlforoai", help="Specify your OAI endpoint")
parser.add_argument("-s", "--set", dest="oaiset", help="Specify your OAI set", required=True)
parser.add_argument("-f", "--field", dest="dc_field", help="Specify DC Field", required=True)
parser.add_argument("-c", "--collection", dest="collection", help="Which collection?")
args = parser.parse_args()

client = MongoClient()
db = client.oaidc


def grab_oai(url, token):
    document = etree.parse(url + token)
    new_session_token = document.findall('//{http://www.openarchives.org/OAI/2.0/}resumptionToken')
    publishers = document.xpath('/e:OAI-PMH/e:ListRecords/e:record/e:metadata/f:dc/g:{0}'.format(dc_field),
                                namespaces={'e': 'http://www.openarchives.org/OAI/2.0/',
                                            'f': 'http://www.openarchives.org/OAI/2.0/oai_dc/',
                                            'g': 'http://purl.org/dc/elements/1.1/'})
    for publisher in publishers:
        result = mongocollection.insert_one({dc_field: publisher.text})
    if len(new_session_token) == 1:
        resumption_token = '&resumptionToken={0}'.format(new_session_token[0].text)
        grab_oai(oai_endpoint, resumption_token)
    else:
        print('Done')


if __name__ == "__main__":
    # Defaults
    oai_endpoint = 'http://dpla.lib.utk.edu:8080/repox/OAIHandler'
    oai_set = '&set='
    metadata_prefix = '&metadataPrefix=oai_dc'
    session_token = ''
    num_publishers = 0
    collection = "default"

    if args.urlforoai:
        oai_endpoint = args.urlforoai
    oai_set = oai_set + args.oaiset
    dc_field = args.dc_field
    if args.collection:
        collection = args.collection
    mongocollection = db[collection]
    oai_endpoint = oai_endpoint +"?verb=ListRecords"

    full_search_string = oai_endpoint + oai_set + metadata_prefix
    grab_oai(full_search_string, session_token)
