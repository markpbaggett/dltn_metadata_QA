import requests
import argparse
from pymongo import MongoClient
import math

parser = argparse.ArgumentParser(description='Enter Your DPLA Connection Info')
parser.add_argument("-k", "--key", dest="api_key", help="Specify your API key", required=True)
parser.add_argument("-p", "--provider", dest="data_provider", help="Specify your data_provider")
parser.add_argument("-c", "--collection", dest="collection", help="Which collection?")
parser.add_argument("-dp", "--dataprovider", dest="real_data_provider", help="Which data provider?")
args = parser.parse_args()

client = MongoClient()
db = client.dltndata

# set variables
if args.data_provider:
    data_provider = args.data_provider
else:
    data_provider = "http://dp.la/api/contributor/tennessee"
api_key = args.api_key
if args.collection:
    collection = args.collection
else:
    collection = "dpla_test"
if args.real_data_provider:
    real_data_provider = f"&dataProvider={args.real_data_provider}"
else:
    real_data_provider = ""


def get_count(key, provider):
    full_url = "http://api.dp.la/v2/items?q={2}&provider.@id={0}&page_size=1&page=1&api_key={1}".format(provider, key, real_data_provider)
    x = requests.get(full_url)
    if x.status_code == 200:
        results = x.json()
        token = math.ceil(results['count']/100)
        return token
    else:
        print("Something went wrong.")


def add_records_from_DPLA(key, provider, mongo_collection, page_number):
    full_url = "http://api.dp.la/v2/items?q=&provider.@id={0}&page_size=100&page={1}&api_key={2}".format(provider, page_number, key)
    x = requests.get(full_url)
    if x.status_code == 200:
        results = x.json()
        for doc in results['docs']:
            try:
                doc_data_provider = doc['dataProvider']
            except:
                doc_data_provider = "Unknown"
            metadata = {"ingest_date": doc['ingestDate'],
                        "data_provider": doc_data_provider,
                        "description": doc['sourceResource']}
            result = mongo_collection.update({"record_id": doc['@id']},
                                            {"record_id": doc['@id'],
                                             "metadata": metadata}, True)
    return


if __name__ == "__main__":
    my_mongo_collection = db[collection]
    page_number = 1
    pages = get_count(api_key, data_provider)
    while page_number <= pages:
        print("Adding documents from page {0} of {1}.".format(page_number, pages))
        add_records_from_DPLA(api_key,data_provider, my_mongo_collection, page_number)
        page_number += 1
    print("Done")