# README

---

## About

Several different scripts to help with metadata QA and cleanup for the Digital Library of Tennessee.

---

## Requirements and Installation

These scripts require **Python 3.4 and above**.  For instructions on installing this to your operating system, see [python.org](https://www.python.org/downloads/).

**MongoDB** is required for storing and analyzing documents.  For instructions on installing this to your operating system, see [the Mongo Community Page](https://www.mongodb.com/download-center#community).

### Install Required Python Modules

To install all Python dependencies, use:

`pip install -r requirements.txt`

---

## Add Records Examples

### Storing OAI-PMH with *addrecords.py*

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

### Storing DPLA JSON-LD with *add_dpla.py*

**Grab all metadata contributed to DPLA by the Digital Library of Tennessee and write to a collection called *dltn_dpla*.**

`python3 add_dpla.py -k MyDPLAKey -p "http://dp.la/api/contributor/tn" -c dltn_dpla`

---

## Q/A-ing your Metadata with *analyze.py*

**Note**: All analyze operations work with the following formats.

* oai_dc
* oai_qdc
* oai_etdms
* mods
* dpla (use for DPLA JSON LD)
* digital_commons (use for Bepress's proprietary XML format)

MODS and OAI DC examples are given below for each operation, but all operations should work with each of these formats.

#### Find Unique Values with "*Find*" Operation
**DC Example:** Find all distinct values associated with the *"dc:rights"* field in *"mtsu_master""*.

`python3 analyze.py -m oai_dc -c mtsu_master -f rights`

**MODS Example:** Find all distinct authorities associated with subjects the dltn_master collection.

`python3 analyze.py -c dltn_master -f subject.@authority -o find -m mods`

#### Find Records that Match Query with "*Match*" Operation
**DC Example**: Find all records in "*mtsu_master*" that have a "*dc:rights*" field with the value of "*Not covered by copyright*".

`python3 analyze.py -m oai_dc -c mtsu_master -f rights -o match -s "Not covered by copyright"`

**MODS Example**: Find all records in "*dltn_master*" that have a "*\physicalDescription\form" element with a text value of "*illustrations*".

`python3 analyze.py -c dltn_master -f physicalDescription.form.#text -o match -m mods -s "illustrations"
`

#### Find If Any Records in a Collection are Missing a Particular Field (Element) with "Missing" Operation
**DC Example**: Find if any records in "*mtsu_master*" are missing a "*dc:rights*" field.

`python3 analyze.py -m oai_dc -c mtsu_master -f rights -o missing`

**MODS Example**: Find if any records are missing a "*\location\url*".

`python3 analyze.py -c dltn_master -f location.url -o missing -m mods`

#### Find If Any Records in a Collection have a Particular Field (Element) with the "Exists" Operation
**DC Example**: Find if any records in "*mtsu_master*" have a "*dc:rights*" field.

`python3 analyze.py -m oai_dc -c mtsu_master -f rights -o exists`

**MODS Example**: Find if any records have a "*\location\url*".

`python3 analyze.py -c dltn_master -f location.url -o exists -m mods`

#### Find how many specific elements a document has with the "length" operation.
**DC Example**: Find if any records in "*mtsu_master*" have 3 "*dc:publisher*" fields.

`python3 analyze.py -m oai_dc -c mtsu_master -o length -f publisher -s 3`

**MODS Example**: Find if any records in "*mtsu_master*" have 3 "*accessCondition*" fields.

`python3 analyze.py -c dltn_master -f accessCondition -o length -s 3`

#### All available flags with *analyze.py*:
* -m
	* Specify the metadata format to retrieve from Mongo Collection
* -o
	* Choose operation: match, missing, exists, find, or length.
* -f
	* Specify the field (Element) to search
* -c
	* Specify the Mongo Collection to Retrieve Metadata from
* -s
	* Specify a value to match with a field
* -h
	* Help!
