from pymongo import MongoClient
import json


class MongoAnalyzer:
    """ A class to handle querying of DLTN metadata in MongoDB.

    Attributes:
        formatted_field: A mongo formatted field based on the field you want to query and the specified metadata format.

    """

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
        self.__collection = self.__db_connection[mongo_collection]

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

    def find_distinct(self):
        """ Find distinct values of your formatted field.

        Return:
            list: a list of distinct values as strings, dicts, etc.

        Example:
            >>> MongoAnalyzer("recordInfo.recordContentSource", "mods", "some_digital_oai").find_distinct()
            [None, 'Athenaeum Rectory', 'Austin Peay State University', 'Blount County Public Library',
            'Calvin M. McClung Historical Collection']

        """
        return [
            distinct for distinct in self.__collection.distinct(self.formatted_field)
        ]

    def match(self, matching_value):
        """ Finds documents where matching value matches the formatted field.

        Accepts:
            matching_value (str): The value you want to match documents on.

        Returns:
            list: A list of documents where the matching value is the value of the formatted field.

        Example:
            >>> MongoAnalyzer("recordInfo.recordContentSource", "mods", "some_digital_oai").match('Athenaeum Rectory')
            [{'@xsi:schemaLocation': 'info:ofi/fmt:xml:xsd:iso20775 http://www.loc.gov/standards/iso20775/N130_ISOholdings_v6_1.xsd',
            'physicalAddress': {'text': ['City: Columbia', 'County: Maury County', 'State: Tennessee']}}}}, 'subject':
            [{'@authority': 'lcsh', '@valueURI': 'http://id.loc.gov/authorities/subjects/sh85133873', 'topic':
            'Tennessee--History'}, {'@displayLabel': 'Tennessee Social Studies K-12 Eras in American History',
            'temporal': 'Era 4 - Expansion and Reform (1801-1861)'}], 'relatedItem': [{'@displayLabel': 'Project',
            '@type': 'host', 'titleInfo': {'title': 'Volunteer Voices'}, 'location': {'url':
            'http://digital.lib.utk.edu/collections/volvoices'}}, {'@displayLabel': 'Collection', '@type': 'host',
            'titleInfo': {'title': 'Historic Collection'}}], 'accessCondition': {'@type': 'use and reproduction',
            '@xlink:href': 'http://rightsstatements.org/vocab/NoC-US/1.0/', '#text': 'No Copyright - United States'},
            'recordInfo': {'recordIdentifier': 'record_0098_000050_000209_0001', 'recordContentSource':
            'Athenaeum Rectory', 'languageOfCataloging': {'languageTerm': {'@authority': 'iso639-2b', '@type': 'code',
            '#text': 'eng'}}, 'recordOrigin': 'Created and edited in general conformance to MODS Guidelines (Version 3.5).',
            'recordCreationDate': {'@encoding': 'edtf', '#text': '2008-08-19'}, 'recordChangeDate': [{'@encoding':
            'edtf', '#text': '2015-03-23'}, {'@encoding': 'edtf', '#text': '2015-03-31'}, {'@encoding': 'edtf', '#text':
             '2015-04-01'}]}, 'note': {'@displayLabel': 'dpn', '#text':
             'This object was added to the Digital Preservation Network in November 2017.'}}}}]

        """
        return [
            doc
            for doc in self.__collection.find(
                json.loads(f'{{ "{self.formatted_field}": "{matching_value}" }}')
            )
        ]

    def check_if_exists(self, exists=True):
        """Return documents where a particular field is present or missing.

        Arguments:
            exists (bool): True returns where present, false returns where missing.

        Return:
            list: The list of matching documents.

        Examples:
            >>> MongoAnalyzer("recordInfo.recordContentSource", "mods", "some_digital_oai").check_if_exists(False)
            [{'_id': ObjectId('5eea8f8e36e31071221cb083'), 'record_id': 'oai:utklib:collections_tndp', 'oai_provider':
            'https://digital.lib.utk.edu/collections/oai2', 'metadata': {'mods': {'@xmlns': 'http://www.loc.gov/mods/v3',
            '@xmlns:mods': 'http://www.loc.gov/mods/v3', '@xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
            '@xmlns:xlink': 'http://www.w3.org/1999/xlink', 'titleInfo': {'title': 'Tennessee Newspaper Digitization Project (TNDP)'},
             'abstract': "The Tennessee Newspaper Digitization Project (TNDP) is a partnership between the University of Tennessee and the Tennessee State Library and Archives. The project provides access to a selection of Tennessee's historical newspapers.",
             'originInfo': {'dateCreated': ['1861-1922', {'@encoding': 'edtf', '@point': 'start', '#text': '1861'},
             {'@encoding': 'edtf', '@point': 'end', '#text': '1922'}]}, 'physicalDescription': {'form': {'@authority': 'aat',
             '@valueURI': 'http://vocab.getty.edu/aat/300026656', '#text': 'newspapers'}}, 'subject': [{'@authority':
             'lcsh', '@valueURI': 'http://id.loc.gov/authorities/subjects/sh85020870', 'topic': 'Cataloging of newspapers'},
              {'@authority': 'lcsh', '@valueURI': 'http://id.loc.gov/authorities/subjects/sh2007101077', 'topic':
              'American newspapers--Directories'}, {'@authority': 'lcsh', '@valueURI':
              'http://id.loc.gov/authorities/subjects/sh85133876', 'topic': 'Tennessee--Politics and government'},
              {'@authority': 'lcsh', '@valueURI': 'http://id.loc.gov/authorities/subjects/sh85133873', 'topic':
              'Tennessee--History'}, {'@authority': 'lcsh', '@valueURI': 'http://id.loc.gov/authorities/subjects/sh85133875',
              'topic': 'Tennessee--History--Civil War, 1861-1865'}, {'@authority': 'lcsh', '@valueURI':
              'http://id.loc.gov/authorities/subjects/sh2008113838', 'topic': 'World War, 1914-1918--Periodicals'},
              {'@authority': 'naf', '@valueURI': 'http://id.loc.gov/authorities/names/n82044753', 'name':
              {'namePart': 'United States. Constitution. 19th Amendment'}}], 'typeOfResource': {'@collection': 'yes', '#text': 'text'},
               'language': {'languageTerm': {'@authority': 'iso639-2b', '@type': 'text', '#text': 'English'}}, 'accessCondition':
               {'@type': 'use and reproduction', '@xlink:href': 'http://rightsstatements.org/vocab/NoC-US/1.0/', '#text':
               'No Copyright - United States'}, 'identifier': 'https://digital.lib.utk.edu/collections/islandora/object/collections%3Atndp'}}}]

        """
        return [
            doc
            for doc in self.__collection.find(
                json.loads(
                    f'{{ "{self.formatted_field}": {{ "$exists" : {str(exists).lower()} }}}}'
                )
            )
        ]

    def find_based_on_array_length(self, array_length):
        """Returns documents where the formatted field is a certain number of values long.

        Argument:
            array_length (int): The length to base your match on.

        Returns:
            list: The list of matching documents.

        Example:
            >>> MongoAnalyzer("identifier", "mods", "some_digital_oai").find_based_on_array_length(6)
            {'_id': ObjectId('5eea8d4236e31071221c064e'), 'record_id': 'oai:utklib:knoxgardens_129', 'oai_provider':
            'https://digital.lib.utk.edu/collections/oai2', 'metadata': {'mods': {'@xmlns': 'http://www.loc.gov/mods/v3',
            '@xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance', '@xmlns:xlink': 'http://www.w3.org/1999/xlink',
            '@xmlns:xs': 'http://www.w3.org/2001/XMLSchema', '@xsi:schemaLocation':
            'http://www.loc.gov/mods/v3 http://www.loc.gov/standards/mods/v3/mods-3-5.xsd', 'identifier': [{'@type':
            'local', '#text': '0012_000463_000229'}, {'@type': 'pid', '#text': 'knoxgardens:129'}, {'@type':
            'slide number', '#text': 'Slide 16'}, {'@type': 'film number', '#text': 'Film  81'}, {'@type': 'spc',
            '#text': 'record_spc_4504'}, 'https://digital.lib.utk.edu/collections/islandora/object/knoxgardens%3A129'],
            'titleInfo': {'title': 'Flame Azalea'}, 'abstract': 'Glass slide of Flame Azalea flowers.', 'originInfo':
            {'dateCreated': [{'@qualifier': 'inferred', '#text': '1927-1935'}, {'@encoding': 'edtf', '@point': 'start',
            '@qualifier': 'inferred', '@keyDate': 'yes', '#text': '1930'}, {'@encoding': 'edtf', '@point': 'end',
            '@qualifier': 'inferred', '#text': '1939'}]}, 'physicalDescription': {'form': {'@authority': 'aat',
            '@valueURI': 'http://vocab.getty.edu/aat/300134977', '#text': 'lantern slides'}, 'extent':
            '3 1/4 x 5 inches', 'internetMediaType': 'image/jp2'}, 'name': {'@valueURI':
            'http://id.loc.gov/authorities/names/no2018075078', '@authority': 'naf', 'namePart': 'Jim Thompson Company',
            'role': {'roleTerm': {'@authority': 'marcrelator', '@valueURI': 'http://id.loc.gov/vocabulary/relators/pht',
            '#text': 'Photographer'}}}, 'subject': [{'@authority': 'lcsh', '@valueURI':
            'http://id.loc.gov/authorities/subjects/sh85101348', 'topic': 'Photography of gardens'}, {'@authority':
            'lcsh', '@valueURI': 'http://id.loc.gov/authorities/subjects/sh85053123', 'topic': 'Gardens, American'},
            {'@authority': 'lcsh', '@valueURI': 'http://id.loc.gov/authorities/subjects/sh85010626', 'topic': 'Azaleas'},
            {'@authority': 'lcsh', '@valueURI': 'http://id.loc.gov/authorities/subjects/sh85113765', 'topic': 'Rhododendrons'},
            {'@authority': 'naf', '@valueURI': 'http://id.loc.gov/authorities/names/n79109786', 'geographic': 'Knoxville (Tenn.)',
            'cartographics': {'coordinates': '35.96064, -83.92074'}}], 'note':
            'Mrs. A. C. Bruner donated this collection to the University of Tennessee. Creation dates were inferred from the dates associated with the archival collection and the activity dates of the Jim Thompson Company.',
            'relatedItem': [{'@displayLabel': 'Project', '@type': 'host', 'titleInfo': {'title':
            'Knoxville Garden Slides'}}, {'@displayLabel': 'Collection', '@type': 'host', 'titleInfo': {'title':
            'Knoxville Gardens Slides'}, 'identifier': 'MS.1324', 'location': {'url':
            'https://n2t.net/ark:/87290/v88w3bgf'}}], 'typeOfResource': 'still image', 'location': {'physicalLocation':
            {'@valueURI': 'http://id.loc.gov/authorities/names/no2014027633', '#text':
            'University of Tennessee, Knoxville. Special Collections'}}, 'recordInfo': {'recordContentSource': {
            '@valueURI': 'http://id.loc.gov/authorities/names/n87808088', '#text':
            'University of Tennessee, Knoxville. Libraries'}, 'languageOfCataloging': {'languageTerm': {'@type': 'text',
            '@authority': 'iso639-2b', '#text': 'English'}}}, 'accessCondition': {'@type': 'use and reproduction',
            '@xlink:href': 'http://rightsstatements.org/vocab/InC/1.0/', '#text': 'In Copyright'}}}}]

        """
        return [
            digital_object
            for digital_object in self.__collection.find(
                json.loads(json.dumps({self.formatted_field: {"$size": array_length}}))
            )
        ]

    def get_digital_objects_of_a_type(self, mongo_type):
        """Get documents where your field is of a certain type.

        Argument:
            mongo_type (string): The mongo type you want to match on.

        Return:
            list: A list of matching documents

        Example:
             >>> MongoAnalyzer("recordInfo.recordContentSource", "mods", "some_digital_oai").get_digital_objects_of_a_type("null")
             [{'_id': ObjectId('5eea8fc236e31071221cbe92'), 'record_id': 'oai:utklib:tdh_8445', 'oai_provider':
             'https://digital.lib.utk.edu/collections/oai2', 'metadata': {'mods': {'@xmlns': 'http://www.loc.gov/mods/v3',
             '@xmlns:xlink': 'http://www.w3.org/1999/xlink', '@xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
             '@version': '3.5', '@xsi:schemaLocation': 'http://www.loc.gov/mods/v3 http://www.loc.gov/standards/mods/v3/mods-3-5.xsd',
             'identifier': [{'@type': 'local', '#text': 'um079'}, {'@type': 'oclc', '#text': '50316643'},
             'https://digital.lib.utk.edu/collections/islandora/object/tdh%3A8445'], 'titleInfo': {'title':
             '[Letter] 1841 June 18, Columbia Female Institute [to] Mrs. Elizabeth Chester, Jackson, Tennessee / M[ary] J[ane] Chester'},
             'abstract': 'The following document is a letter dated June 18, 1841, from Mary Jane Chester to her mother Elizabeth Chester. In the letter, Mary Jane expresses anticipation about returning home soon, and she also discusses her upcoming examination.',
             'originInfo': {'dateCreated': ['June 18, 1841', {'@encoding': 'edtf', '#text': '1841-06-18'}]}, 'subject':
             [{'topic': 'Letters'}, {'topic': 'Boarding school students'}, {'topic': 'Tennessee -- History'}],
             'name': {'namePart': 'Chester, Mary Jane', 'role': {'roleTerm': {'@authority': 'marcrelator',
             '@valueURI': 'http://id.loc.gov/vocabulary/relators/crp', '#text': 'Correspondent'}}}, 'accessCondition':
             {'@type': 'use and reproduction', '@xlink:href': 'http://rightsstatements.org/vocab/CNE/1.0/', '#text':
             'Copyright Not Evaluated'}, 'location': {'physicalLocation': None}, 'relatedItem': [{'@displayLabel':
             'Project', '@type': 'host', 'titleInfo': {'title': 'Tennessee Documentary History'}}, {'@displayLabel':
             'Collection', '@type': 'host', 'titleInfo': {'title': 'Chester Family Papers MS-25 (May/Jun 1841)'}}],
             'typeOfResource': 'text', 'language': {'languageTerm': {'@authority': 'iso639-2b', '@type': 'text',
             '#text': 'English'}}, 'recordInfo': {'recordContentSource': None, 'languageOfCataloging': {'languageTerm':
             {'@authority': 'iso639-2b', '@type': 'code', '#text': 'eng'}}, 'recordCreationDate': '2020-04-23-04:00',
             'recordOrigin': 'This MODS record was generated into MODS v3.5 from the TEI teiHeader by\n          University of Tennessee Libraries Digital Initiatives, using a stylesheet available at\n          https://github.com/utkdigitalinitiatives/tei-to-mods.'}}}}
             ]

        """
        mongo_types = {
            "double": 1,
            "string": 2,
            "object": 3,
            "array": 4,
            "binData": 5,
            "objectId": 7,
            "bool": 8,
            "date": 9,
            "null": 10,
            "regex": 11,
            "javascript": 13,
            "javascriptWithScope": 15,
            "int": 16,
            "timestamp": 17,
            "long": 18,
            "decimal": 19,
            "minKey": -1,
            "maxKey": 127,
        }
        return [
            digital_object
            for digital_object in self.__collection.find(
                json.loads(
                    json.dumps(
                        {self.formatted_field: {"$type": mongo_types[mongo_type]}}
                    )
                )
            )
        ]
