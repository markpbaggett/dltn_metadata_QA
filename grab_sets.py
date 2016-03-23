from lxml import etree
import argparse

parser = argparse.ArgumentParser(description='Enter Your OAI Endpoint')
parser.add_argument("-u", "--url", dest="urlforoai", help="Specify OAI endpoint", required=True)
args = parser.parse_args()

def grab_oai(url):
    document = etree.parse(url)
    sets = document.xpath('/a:OAI-PMH/a:ListSets/a:set/a:setSpec', namespaces={'a': 'http://www.openarchives.org/OAI/2.0/'})
    number_of_sets = 0
    for set in sets:
        print(set.text)
        number_of_sets += 1
    print('\n\nNumber of sets: ' + str(number_of_sets))

if __name__ == "__main__":
    oai_endpoint = args.urlforoai + '?verb=ListSets'
    grab_oai(oai_endpoint)
