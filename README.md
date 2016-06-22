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

### Storing metadata

* **Grab all metadata as *"oai_dc"* from set *"p15838coll4"* at *"http://cdm15838.contentdm.oclc.org/oai/oai.php"* and write each record as a document to a collection called *"mtsu_master"*.**

	* `python3 dplachecker.py -u http://cdm15838.contentdm.oclc.org/oai/oai.php -s p15838coll4 -m oai_dc -c mtsu_master`
	
* All available flags with DPLAChecker:
	* -u
		* Specify your OAI-PMH url that you want to pull metadata from
	* -s 
		* Specify the set you want to pull metadata from
	* -m
		* Specify the metadata format that you want to grab and store
	* -c
		* Specify the collection you want to store the metadata in
		* By default, this is **"default"**
	* -h
		* Help!!!

#### Q/A-ing your metadata
		
**Find all distinct values associated with the *"dc:rights"* field in *"mtsu_master""*.**

`python3 mongotest.py -m oai_dc -c mtsu_master -rights`

**Find all records in "*mtsu_master*" that have a "*dc:rights*" field with the value of "*Not covered by copyright*".**

`python3 mongotest.py -m oai_dc -c mtsu_master -f rights -o match -s "Not covered by copyright"`

* All available flags with mongotest:
	* -m
		* Specify the metadata format
	* -o
		* Specify operation (use match to match a key value pair -- leave blank for distinct queries)
	* -f
		* Specify the field to search
	* -c
		* Specify the collection
	* -s
		* Specify a value to match with a key
	* -h
		* Help!
