{% extends "BASE_TEMPLATE base.md" %}
{% block body %}
# SYSTEMATIC SURVEY METADATA TEMPLATE INSTRUCTIONS

## Intended Usage
This Systematic Survey Metadata template should be used to record metadata relating to a Systematic Survey dataset.

The Systematic Survey Metadata template **must be used in combination** with the
Systematic Survey Occurrence template and, in some cases, the Systematic Survey Site template
with or without the Systematic Survey Site Visit template.

Templates have been provided to facilitate integration of your data into the Biodiversity
Data Repository database. Not all types of data have been catered for in the available
templates at this stage; therefore, if you are unable to find a suitable template, please
contact <bdr-support@gaiaresources.com.au> to make us aware of your data needs.

## Data Validation Requirements:
For data validation, you will need your data file to:

- be the correct **file format**,
- have **fields that match the template downloaded** (do not remove, or 
  change the order of fields),
- have extant values for **mandatory fields** (see Table 1), and
- comply with all **data value constraints**; for example the geographic coordinates are
  consistent with a [geodeticDatum](#geodeticDatum-vocabularies) type of the ***{{values.geodetic_datum_count}}*** available
  options.
- only **one row of metadata** should be included and only the first row of metadata will be accepted
  (this symbolises one Survey per dataset submission).

Additional fields may be added **after the templated fields** (noting that the data type 
is not assumed and values will be encoded as strings).

### FILE FORMAT
- The systematic survey metadata template is a [UTF-8](#appendix-iv-utf-8) encoded csv (not Microsoft
Excel Spreadsheets). Be sure to save this file with your data as a .csv (UTF-8) as
follows, otherwise it will not pass the in-browser csv validation step upon upload.
<br>`[MS Excel: Save As > More options > Tools > Web options > Save this document as >
Unicode (UTF-8)]`
- **Do not include empty rows.**

### FILE NAME

When making a manual submission to the Biodiversity Data Repository,
the file name must include the version number
of this biodiversity data template (`v{{ metadata.version }}`).
The following format is an example of a valid file name:

`data_descripion-v{{ metadata.version }}-additional_description.csv`

where:

* `data_description`: A short description of the data (e.g. `survey_meta`, `test_data`).
* `v{{ metadata.version }}`: The version number of this template.
* `additional_description`: (Optional) Additional description of the data, if needed (e.g. `test_data`).
* `.csv`: Ensure the file name ends with `.csv`.

For example, `survey_meta-v{{ metadata.version }}-test_data.csv` or `test_data-v{{ metadata.version }}.csv`

### FILE SIZE
MS Excel imposes a limit of 1,048,576 rows on a spreadsheet, limiting a CSV file to the
header row followed by 1,048,575 occurrences. Furthermore, MS Excel has a 32,767 character
limit on individual cells in a spreadsheet. These limits may be overcome by using or
editing CSV files with other software.

Larger datasets may be more readily ingested using the API interface. Please contact
<bdr-support@gaiaresources.com.au> to make us aware of your data needs.

## TEMPLATE FIELDS
The template file contains the field names in the top row that form part of the core Survey
data model. Table 1 will assist you in transferring your data to the template with the following
information:

- **Field name** in the template (and an external link to the Darwin Core standard for that
field where available);
- **Description** of the field;
- **Required** i.e. whether the field is **<font color="Crimson">mandatory</font>,
<font color="DarkGoldenRod">conditionally mandatory</font>, or optional**;
- **Datatype format** required for the data values for example text (string), number
(integer, float), or date; and
- **Example/s** of an entry for that field.
- **Vocabulary links** within this document (for example pick list values) where relevant.
The fields that have suggested values options for the fields in Table 1 are listed in
Table 2 in alphabetical order of field name.

### ADDITIONAL FIELDS
Data that do not match the existing template fields may be added as additional columns in
the CSV files after the templated fields. 
For example, `sampleSizeUnit`, `sampleSizeValue`.

<ins>Table 1: Systematic Survey Metadata template fields with descriptions, conditions,
datatype format, and examples.</ins>

{{tables.fields}}

## CHANGELOG

No changes from Systematic Survey Metadata Template v2.0.0

## APPENDICES
### APPENDIX-I: Vocabulary List
With the exception of `geodeticDatum`, data validation
does not require adherence to the vocabularies for the various vocabularied fields.. These vocabularies are provided as a
means of assistance in developing consistent language within the database. New terms can be added
to more appropriately describe your data that goes beyond the current list. 

Table 2 provides some
suggested values from existing sources such as: [Biodiversity Information Standard (TDWG)](https://dwc.tdwg.org/),
[EPSG.io Coordinate systems worldwide](https://epsg.io/), the [Global Biodiversity Information
System](https://rs.gbif.org/), and [Open Nomenclature in the biodiversity
era](https://doi.org/10.1111/2041-210X.12594).

<ins>Table 2: Suggested values for the controlled vocabulary fields in the template. Each term has
a preferred label with a definition to aid understanding of its meaning. For some terms, alternative
labels with similar semantics are provided. <br>Note: <font color="red">the value for `geodeticDatum`
must come from one of five options in this table.</font></ins>

{{tables.vocabularies}}

### APPENDIX-II: Well Known Text (WKT)
For general information on how WKT coordinate reference data is formatted is available [here](https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry).
The length of a WKT string or of its components is not prescribed; however, MS Excel *does* has a
32,767 (32K) character limit on individual cells in a spreadsheet.

It is possible to edit CSV files outside of Excel in order to include more than 32K characters.

**Note:** Ensure the coordinates are arranged in `longitude latitude` order and do not include the CRS in the WKT expression (it comes from the geodeticDatum field).

![Multipart geometries (2D) WKT](assets/multipart_geometries_2d_wkt.png)
<br><center><small>*Source: Mwtoews - CC BY-SA 3.0 -  Wikipedia <https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry>*</small></center>

### APPENDIX-III: Timestamp
Following date and date-time formats are acceptable within the timestamp:

| TYPE | FORMAT                                                                                                                              |
| --- |-------------------------------------------------------------------------------------------------------------------------------------|
| **xsd:dateTimeStamp with timezone** | yyyy-mm-ddThh:mm:ss.sTZD (eg 1997-07-16T19:20:30.45+01:00) OR <br/> yyyy-mm-ddThh:mm:ssTZD (eg 1997-07-16T19:20:30+01:00) OR <br/>  yyyy-mm-ddThh:mmTZD (eg 1997-07-16T19:20+01:00)|
| **xsd:dateTime** | yyyy-mm-ddThh:mm:ss.s (eg 1997-07-16T19:20:30.45) OR<br/> yyyy-mm-ddThh:mm:ss (eg 1997-07-16T19:20:30) OR<br/> yyyy-mm-ddThh:mm (eg 1997-07-16T19:20) |
| **xsd:Date** | dd/mm/yyyy OR<br/> d/m/yyyy OR<br/> yyyy-mm-dd OR<br/> yyyy-m-d |
| **xsd:gYearMonth** | mm/yyyy OR<br/> m/yyyy OR<br/> yyyy-mm |
| **xsd:gYear** | yyyy |

Where:<br/>
&emsp; `yyyy`: four-digit year <br/>
&emsp; `mm`: two-digit month (01=January, etc.) <br/>
&emsp; `dd`: two-digit day of month (01 through 31) <br/>
&emsp; `hh`: two digits of hour (00 through 23) (am/pm NOT allowed) <br/>
&emsp; `mm`: two digits of minute (00 through 59) <br/>
&emsp; `ss`: two digits of second (00 through 59) <br/>
&emsp; `s`: one or more digits representing a decimal fraction of a second <br/>
&emsp; `TZD`: time zone designator (Z or +hh:mm or -hh:mm) <br/>

### APPENDIX-IV: UTF-8
UTF-8 encoding is considered a best practice for handling character encoding, especially in
the context of web development, data exchange, and modern software systems. UTF-8
(Unicode Transformation Format, 8-bit) is a variable-width character encoding capable of
encoding all possible characters (code points) in Unicode.<br/>
Here are some reasons why UTF-8 is recommended:
- **Universal Character Support:** UTF-8 can represent almost all characters from all writing 
  systems in use today. This includes characters from various languages, mathematical symbols, 
  and other special characters.
- **Backward Compatibility:** UTF-8 is backward compatible with ASCII (American
  Standard Code for Information Interchange). The first 128 characters in UTF-8 are
  identical to ASCII, making it easy to work with systems that use ASCII.
- **Efficiency:** UTF-8 is space-efficient for Latin-script characters (common in English
  and many other languages). It uses one byte for ASCII characters and up to four
  bytes for other characters. This variable-length encoding minimises storage and
  bandwidth requirements.
- **Web Standards:** UTF-8 is the dominant character encoding for web content. It is
  widely supported by browsers, servers, and web-related technologies.
- **Globalisation:** As software applications become more globalised, supporting a wide
  range of languages and scripts becomes crucial. UTF-8 is well-suited for
  internationalisation and multilingual support.
- **Compatibility with Modern Systems:** UTF-8 is the default encoding for many
  programming languages, databases, and operating systems. Choosing UTF-8 helps
  ensure compatibility across different platforms and technologies.

When working with text data, UTF-8 encoding is recommended to avoid issues related to character
representation and ensure that a diverse set of characters and languages is supported.

For assistance, please contact: <bdr-support@gaiaresources.com.au>
{% endblock %}
