__author__ = 'mbagget1'

from lxml import etree
import argparse
from pymongo import MongoClient

parser = argparse.ArgumentParser(description='Enter Your OAI Endpoint Information')
parser.add_argument("-u", "--url", dest="urlforoai", help="Specify your OAI endpoint")
parser.add_argument("-s", "--set", dest="oaiset", help="Specify your OAI set", required=True)
args = parser.parse_args()

client = MongoClient()
db = client.oaipublishers


def grab_oai(url, token):
    document = etree.parse(url + token)
    new_session_token = document.findall('//{http://www.openarchives.org/OAI/2.0/}resumptionToken')
    publishers = document.xpath('/e:OAI-PMH/e:ListRecords/e:record/e:metadata/f:dc/g:publisher',
                                namespaces={'e': 'http://www.openarchives.org/OAI/2.0/',
                                            'f': 'http://www.openarchives.org/OAI/2.0/oai_dc/',
                                            'g': 'http://purl.org/dc/elements/1.1/'})
    for publisher in publishers:
        result = db.oaipublishers.insert_one({"publisher": publisher.text})
    if len(new_session_token) == 1:
        resumption_token = '&resumptionToken={0}'.format(new_session_token[0].text)
        grab_oai(oai_endpoint, resumption_token)
    else:
        print('Done')


if __name__ == "__main__":
    # Defaults
    oai_endpoint = 'http://dpla.lib.utk.edu:8080/repox/OAIHandler?verb=ListRecords'
    oai_set = '&set='
    metadata_prefix = '&metadataPrefix=oai_dc'
    session_token = ''
    num_publishers = 0

    if args.urlforoai:
        oai_endpoint = args.urlforoai
    oai_set = oai_set + args.oaiset

    full_search_string = oai_endpoint + oai_set + metadata_prefix
    grab_oai(full_search_string, session_token)
