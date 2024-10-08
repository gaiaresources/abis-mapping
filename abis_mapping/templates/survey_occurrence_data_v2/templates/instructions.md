{% extends "BASE_TEMPLATE base.md" %}
{% block body %}
# SYSTEMATIC SURVEY OCCURRENCES DATA TEMPLATE INSTRUCTIONS

## Intended Usage
This template is used to record occurrence data; that is, the presence or absence of an organism
at a particular site locality at a point in time.

The Systematic Survey Occurrences template **must be used in combination** with the
Systematic Survey Metadata template, and in some cases the Systematic Survey Sites
template.

Templates have been provided to facilitate integration of your data into the Biodiversity
Data Repository database. Not all types of data have been catered for in the available
templates at this stage; therefore, if you are unable to find a suitable template, please
contact <bdr-support@gaiaresources.com.au> to make us aware of your data needs.

#### Data Validation Requirements:
For data validation, you will need your data file to:

- be in the correct **file format,**
- have **fields that match the template downloaded** (do not remove, or 
  change the order of fields),
- have extant values for **mandatory fields** (see Table 1),
- comply with all **data value constraints**; for example the geographic coordinates are
  consistent with a [geodeticDatum](#geodeticDatum-vocabularies) type of the ***{{values.geodetic_datum_count}}*** available
  options, and
- align with existing controlled [vocabularies](#appendix-i-vocabulary-list) wherever possible (this is mandatory
  for geodeticDatum), but new terms may be submitted for consideration amd will not cause a
  validation error.

Additional fields may be added **after the templated fields** (noting that the data type 
is not assumed and values will be encoded as strings).

### FILE FORMAT
- The systematic survey occurrence data template is a [UTF-8](#appendix-iii-utf-8) encoded csv (that is, not Microsoft
  Excel Spreadsheets). Be sure to save this file with your data as a .csv (UTF-8): 
  <br>`[MS Excel: Save As > More options > Tools > Web options > Save this document as >
  Unicode (UTF-8)]`<br>
  otherwise it will not pass the csv validation step upon upload.
- **Do not include empty rows**.

#### FILE SIZE
MS Excel imposes a limit of 1,048,576 rows on a spreadsheet, limiting a CSV file to the
header row followed by 1,048,575 occurrences. Furthermore, MS Excel has a 32,767-character
limit on individual cells in a spreadsheet. These limits may be overcome by using or
editing CSV files with other software.

Larger datasets may be more readily ingested using the API interface. Please contact
<bdr-support@gaiaresources.com.au> to make us aware of your data needs.

## TEMPLATE FIELDS
The template contains the field names in the top row. Table 1 will assist you in transferring
your data to the template by providing guidance on:

- **Field name** in the template (and an external link to the [Darwin Core standard](https://dwc.tdwg.org/terms/)
  for that field where relevant);
- **Description** of the field;
- **Required** whether the field is **<font color="red">mandatory</font> or optional**;
- **Format** (datatype) required for the data values for example text (string), number
  (integer, float), or date;
- **Example** of an entry or entries for that field; and
- **[Vocabulary links](#appendix-i-vocabulary-list)** within this document (for example pick list values) where
  relevant. The fields that have suggested values options for the fields in Table 1 are
  listed in Table 2 in alphabetical order of the field name.

### ADDITIONAL FIELDS
Data that does not match the existing template fields may be added as
additional columns in the CSV files after the templated fields. 
For example: `eventRemarks`, `associatedTaxa`, `pathway`.

<ins>Table 1: Systematic Survey Occurrence data template fields with descriptions, conditions,
datatype format, and examples.</ins>

{{tables.fields}}

## CHANGELOG

Changes from Systematic Survey Occurrence Data Template v1.0.0

### CHANGED FIELDS

* `conservationJurisdiction` is renamed `conservationAuthority`.
* `sensitivityCategory` and `sensitivityAuthority` are added fields. Both are type string.
They are mutually inclusive, both must be provided or both must be blank.
* Add field `siteVisitID`. Type is string, can be blank. 
If provided, should match a `siteVisitID` in the `survey_site_visit_data.csv` template.

## APPENDICES
### APPENDIX-I: VOCABULARY LIST
With the exception of `geodeticDatum`, data validation does not require fields to adhere to the
vocabularies specified for the various vocabularied fields. These vocabularies are merely provided as a
means of assistance in developing a consistent language within the database. New terms may be added
to more appropriately describe your data that goes beyond the current list. Table 2 provides some
suggested values from existing sources such as: [Biodiversity Information Standard (TDWG)](https://dwc.tdwg.org/),
[EPSG.io Coordinate systems worldwide](https://epsg.io/), the [Global Biodiversity Information
System](https://rs.gbif.org/), and [Open Nomenclature in the biodiversity
era](https://doi.org/10.1111/2041-210X.12594).

<ins>Table 2: Suggested values for the controlled vocabulary fields in the template. Each term has
a preferred label with a definition to aid understanding of its meaning. For some terms, alternative
labels with similar semantics are provided. Note: <font color="red">`geodeticDatum` value
**must** come from one of five options in this table.</font></ins>

<a name="vocabulary-list"></a>

{{tables.vocabularies}}

<a name="threatStatus-vocabularies"></a>
<ins>Table 2b: Suggested values for conditionally mandatory values for the `threatStatus` and
`conservationAuthority` fields in the template. State and Territory `conservationAuthority` 
spelt out as words are also valid. For some `threatStatus` terms, alternative labels are provided
that are also valid for that `conservationAuthority`.

{{tables.threat_status}}

### APPENDIX-II: Timestamp
Following date and date-time formats are acceptable within the timestamp:

| TYPE | FORMAT                                                                                                                              |
| --- |-------------------------------------------------------------------------------------------------------------------------------------|
| **xsd:dateTimeStamp with timezone** | yyyy-mm-ddThh:mm:ss.sTZD (eg 1997-07-16T19:20:30.45+01:00) OR <br/> yyyy-mm-ddThh:mm:ssTZD (eg 1997-07-16T19:20:30+01:00) OR <br/>  yyyy-mm-ddThh:mmTZD (eg 1997-07-16T19:20+01:00)|
| **xsd:dateTime** | yyyy-mm-ddThh:mm:ss.s (eg 1997-07-16T19:20:30.45) OR<br/> yyyy-mm-ddThh:mm:ss (eg 1997-07-16T19:20:30) OR<br/> yyyy-mm-ddThh:mm (eg 1997-07-16T19:20) |
| **xsd:Date** | dd/mm/yyyy OR<br/> d/m/yyyy OR<br/> yyyy-mm-dd OR<br/> yyyy-m-d |
| **xsd:gYearMonth** | mm/yyyy OR<br/> m/yyyy OR<br/> yyyy-mm |
| **xsd:gYear** | yyyy |

Where<br/>
&emsp; `yyyy`: four-digit year <br/>
&emsp; `mm`: two-digit month (01=January, etc.) <br/>
&emsp; `dd`: two-digit day of month (01 through 31) <br/>
&emsp; `hh`: two digits of hour (00 through 23) (am/pm NOT allowed) <br/>
&emsp; `mm`: two digits of minute (00 through 59) <br/>
&emsp; `ss`: two digits of second (00 through 59) <br/>


### APPENDIX-III: UTF-8
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
