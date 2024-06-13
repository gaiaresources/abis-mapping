# INCIDENTAL OCCURRENCE DATA TEMPLATE INSTRUCTIONS

## OVERVIEW
Use this template to record occurrence data; that is the presence or absence of an organism
at a particular site locality at a point in time.

Templates have been provided to facilitate integration of your data into the Biodiversity
Data Repository database. Not all types of data have been catered for in the available
templates at this stage; therefore, if you are unable to find a suitable template, please 
contact <bdr-support@gaiaresources.com.au> to make us aware of your data needs.

#### NEED TO KNOW:
For data validation, you will need your data file to:
* be the correct **file format,**
* have **matching template fields** to the template downloaded (do not remove, or 
change the order of fields), however
* additional fields may be added **after the templated fields** (noting that the
data type is not assumed and values will be encoded as strings),
* have values in **mandatory fields** (see Table 1),
* comply with data **value constraints** for example the geographic coordinates are
consistent with a [geodeticDatum](...) type of the ***{{values.geodetic_datum_count}}*** available 
options, and
* align with existing controlled [vocabularies](...) wherever possible (this is mandatory
for geodeticDatum), but new terms may be submitted for consideration amd will not cause a 
validation error.

### FILE FORMAT
* The incidental occurrence data template is a [UTF-8](...) encoded csv (not Microsoft
Excel Spreadsheets). Be sure to save this file with your data as a .csv (UTF-8) as follows,
otherwise it will not pass the csv validation step upon upload.
  * [MS Excel: Save As > More options > Tools > Web options > Save this document as >
  Unicode (UTF-8)]
* **Do not include empty rows**.

#### FILE SIZE
MS Excel imposes a limit of 1,048,576 rows on a spreadsheet, limiting a CSV file to the
header row followed by 1,048,575 occurrences. Furthermore, MS Excel has a 32,767 character
limit on individual cells in a spreadsheet. These limits may be overcome by using or
editing CSV files with other software.

Larger datasets may be more readily ingested using the API interface. Please contact
<bdr-support@gaiaresources.com.au> to make us aware of your data needs.

## TEMPLATE FIELDS
The template contains the field names in the top row. Table 1 will assist you in transferring
your data to the template indicating:
* **Field name** in the template (and an external link to the [Darwin Core standard](...)
for that field where relevant);
* **Description** of the field;
* **Required** whether the field is **<font color="red">mandatory</font> or optional**;
* **Format** (datatype) required for the data values for example text (string), number
  (integer, float), or date;
* **Example** of an entry or entries for that field; and
* **[Vocabulary links](#{{anchors.vocabulary_list}})** within this document (for example pick list values) where
relevant. The fields that have suggested values options for the fields in Table 1 are 
listed in Table 2 in alphabetical order of the field name.

### ADDITIONAL FIELDS
Data that do not match the existing template fields may be added as additional columns in
the CSV files after the templated fields. <br>
E.g. eventRemarks, associatedTaxa, pathway.

<ins>Table 1: Incidental occurrence data template fields with descriptions, conditions,
datatype format, and examples.</ins>

{{tables.fields}}

## APPENDICES
### APPENDIX-I: VOCABULARY LIST
Apart from geodeticDatum, the data validation doesnot require adherence tho the below vocabularies
for each of the fields indicated as having vocabularies. These vocuabularies are provided as a 
means of assistance in developing consistent language within the database. New terms can be added
to more appropriately describe your data that goes beyond the current list. Table 2 provides some 
suggested values from existing sources such as: [Biodiversity Information Standard (TDWG)](https://dwc.tdwg.org/),
[EPSG.io Coordinate systems worldwide](https://epsg.io/), the [Global Biodiversity Information 
System](https://rs.gbif.org/), and [Open Nomenclature in the biodiversity 
era](https://doi.org/10.1111/2041-210X.12594).

<a name="{{anchors.vocabulary_list}}" />
<ins>Table 2: Suggested values for the controlled vocabulary fields in the template. Each term has
a preferred label with a definition to aid understanding of its meaning. For some terms, alternative
labels are provided that mean the same sort of thing. Note: <font color="red">geodeticDatum value 
must come from one of five options in this table.</font></ins>

{{tables.vocabularies}}

<ins>Table 2b: Suggested values for conditionally mandatory values for the threatStatus and
conservationJurisdiction in the template. State and Territory conservationJurisdictions spelt out
in words are also valid. For some threatStatus terms, alternative labels are provided that are also
valid for that conservationJurisdiction.

{{tables.threat_status_conservation_jurisdiction}}

## APPENDIX-II: Timestamp
Following date and date-time formats are acceptable within the timestamp:

| TYPE | FORMAT                                                                                                                              |
| --- |-------------------------------------------------------------------------------------------------------------------------------------|
| **xsd:dateTimeStamp with timezone** | yyyy-mm-ddThh:mm:ss.sTZD (eg 1997-07-16T19:20:30.45+01:00) OR <br/> yyyy-mm-ddThh:mm:ssTZD (eg 1997-07-16T19:20:30+01:00) OR <br/>  yyyy-mm-ddThh:mmTZD (eg 1997-07-16T19:20+01:00)|
| **xsd:dateTime** | yyyy-mm-ddThh:mm:ss.s (eg 1997-07-16T19:20:30.45) OR<br/> yyyy-mm-ddThh:mm:ss (eg 1997-07-16T19:20:30) OR<br/> yyyy-mm-ddThh:mm (eg 1997-07-16T19:20) |
| **xsd:Date** | dd/mm/yyyy OR<br/> d/m/yyyy OR<br/> yyyy-mm-dd OR<br/> yyyy-m-d |
| **xsd:gYearMonth** | mm/yyyy OR<br/> m/yyyy OR<br/> yyyy-mm |
| **xsd:gYear** | yyyy |
Where:<br/>
&emsp; yyyy = four-digit year <br/>
&emsp; mm = two-digit month (01=January, etc.) <br/>
&emsp; dd = two-digit day of month (01 through 31) <br/>
&emsp; hh = two digits of hour (00 through 23) (am/pm NOT allowed) <br/>
&emsp; mm = two digits of minute (00 through 59) <br/>
&emsp; ss = two digits of second (00 through 59) <br/>

