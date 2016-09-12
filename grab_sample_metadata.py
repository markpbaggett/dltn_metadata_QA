import requests
import argparse

parser = argparse.ArgumentParser(description='Enter Your OAI Endpoint')
parser.add_argument("-u", "--url", dest="urlforoai", help="Specify OAI endpoint.", required=True)
parser.add_argument("-f", "--filename", dest="filename", help="Specify filename.")
parser.add_argument("-s", "--set", dest="set", help="Specify set.")
parser.add_argument("-m", "--metadataFormat", dest="metadata_format", help="Specify metadata format.", required=True)
args = parser.parse_args()

if args.filename:
    filename = args.filename
else:
    filename = "sample.xml"
if args.set:
    full_url = "{0}?verb=ListRecords&set={1}&metadataPrefix={2}".format(args.urlforoai, args.set, args.metadata_format)
else:
    full_url = "{0}?verb=ListRecords&metadataPrefix={1}".format(args.urlforoai, args.metadata_format)

def grab_sample(url):
    document = requests.get(url)
    sample = open(filename, "w")
    sample.write(document.text)
    sample.close()
    print("Done.")

if __name__ == "__main__":
    grab_sample(full_url)