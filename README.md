# README

---

## About

Several different scripts to help with metadata QA and cleanup for the Digital Library of Tennessee.

## Requirements

**NOTE:** install script coming.

* Python3
* MongoDB
* Python 3 Modules
	* pymongo
	* argparse
	* json
	* lxml
	* xmltodict
	* urllib

## Examples

### Storing metadata with *addrecords.py*

* **Grab all metadata as *"oai_dc"* from set *"p15838coll4"* at *"http://cdm15838.contentdm.oclc.org/oai/oai.php"* and write each record as a document to a collection called *"mtsu_master"*.**

	* `python3 addrecords.py -u http://cdm15838.contentdm.oclc.org/oai/oai.php -s p15838coll4 -m oai_dc -c mtsu_master`

#### All available flags with "*addrecords.py*":
	* -u
		* Specify your OAI-PMH url that you want to pull metadata from
	* -s
		* Specify the OAI-PMH set you want to pull metadata from
	* -m
		* Specify the metadata format available from your OAI-PMH enpoint that you want to grab and store
	* -c
		* Specify the Mongo collection you want to store the metadata in
		* By default, this is **"default"**
	* -h
		* Help!!!

### Q/A-ing your Metadata with *analyze.py*

#### Find Unique Values with "*Find*" Operation
**Example:** Find all distinct values associated with the *"dc:rights"* field in *"mtsu_master""*.

`python3 analyze.py -m oai_dc -c mtsu_master -f rights`

#### Find Records that Match Query with "*Match*" Operation
**Example**: Find all records in "*mtsu_master*" that have a "*dc:rights*" field with the value of "*Not covered by copyright*".

`python3 analyze.py -m oai_dc -c mtsu_master -f rights -o match -s "Not covered by copyright"`

#### Find If Any Records in a Collection are Missing a Particular Field (Element) with "Exists" Operation
**Example**: Find if any records in "*mtsu_master*" are missing a "*dc:rights*" field.

`python3 analyze.py -m oai_dc -c mtsu_master -f rights -o exists`

#### All available flags with *analyze.py*:
	* -m
		* Specify the metadata format to retrieve from Mongo Collection
	* -o
		* Choose operation: match, exists, or find.
	* -f
		* Specify the field (Element) to search
	* -c
		* Specify the Mongo Collection to Retrieve Metadata from
	* -s
		* Specify a value to match with a field
	* -h
		* Help!
