__author__ = 'mbagget1'

from lxml import etree
import argparse

parser = argparse.ArgumentParser(description='Enter Your OAI Endpoint Information')
parser.add_argument("-u", "--url", dest="urlforoai", help="Specify your OAI endpoint")
parser.add_argument("-s", "--set", dest="oaiset", help="Specify your OAI set", required=True)
parser.add_argument("-m", "--metadata", dest="metadataprefix", help="Specify your metadata prefix", required=True)
args = parser.parse_args()

def grab_oai(url, token):
    document = etree.parse(url + token)
    session_token = document.findall('//{http://www.openarchives.org/OAI/2.0/}resumptionToken')
    publishers = document.xpath('/e:OAI-PMH/e:ListRecords/e:record/e:metadata/f:dc/g:publisher', namespaces={'e': 'http://www.openarchives.org/OAI/2.0/', 'f': 'http://www.openarchives.org/OAI/2.0/oai_dc/', 'g': 'http://purl.org/dc/elements/1.1/'})
    for publisher in publishers:
        print(publisher.text)
    if len(session_token) == 1:
        resumption_token = '&resumptionToken={0}'.format(session_token[0].text)
        token_attributes = session_token[0].attrib
        print('Token is at {0} of {1} total records.'.format(token_attributes["cursor"], token_attributes["completeListSize"]))
        grab_oai(oai_endpoint, resumption_token)



if __name__ == "__main__":
    #Defaults
    oai_endpoint = 'http://dpla.lib.utk.edu:8080/repox/OAIHandler?verb=ListRecords'
    oai_set = '&set='
    metadata_prefix = '&metadataPrefix='
    session_token = ''
    num_publishers = 0

    if args.urlforoai:
        oai_endpoint = args.urlforoai
    metadata_prefix = metadata_prefix + args.metadataprefix
    oai_set = oai_set + args.oaiset

    full_search_string = oai_endpoint + oai_set + metadata_prefix
    grab_oai(full_search_string, session_token)
