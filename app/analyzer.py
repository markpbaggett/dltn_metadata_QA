from pymongo import MongoClient
import json


class MongoAnalyzer:
    def __init__(
        self,
        field,
        metadata_format,
        mongo_collection="default",
        uri="localhost",
        port="27017",
    ):
        self.formatted_field = self.__format_metadata(field, metadata_format)
        self.__db_connection = MongoClient(f"mongodb://{uri}:{port}/").dltndata
        self.collection = self.__db_connection[mongo_collection]

    @staticmethod
    def __format_metadata(field, prefix):
        formatted_field = {
            "oai_dc": f"metadata.{prefix}:dc.dc:{field}",
            "simple-dublin-core": f"metadata.{prefix}:dc.dc:{field}",
            "mods": f"metadata.{prefix}.{field}",
            "oai_qdc": f"metadata.{prefix}:qualifieddc.{field}",
            "oai_etdms": f"metadata.thesis.{field}",
            "digital_commons": f"metadata.document.{field}",
            "dpla": f"metadata.{field}",
        }
        return formatted_field[prefix]

    def find(self):
        return self.collection.distinct(self.formatted_field)

    def match(self, matching_value):
        return [
            doc
            for doc in self.collection.find(
                json.loads(f'{{ "{self.formatted_field}": "{matching_value}" }}')
            )
        ]


if __name__ == "__main__":
    x = MongoAnalyzer("name.role.roleTerm.#text", "mods", "all_digital_oai")
    test = x.match("Minute")
    for document in test:
        print(document)
