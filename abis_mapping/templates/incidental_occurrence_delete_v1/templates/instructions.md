{% extends "BASE_TEMPLATE base.md" %}
{% block body %}
# INCIDENTAL OCCURRENCE DELETE TEMPLATE INSTRUCTIONS

## Intended Usage
This Incidental Occurrence Delete template should be used to delete occurrence data.

## Data Validation Requirements:
For data validation, you will need your data file to:

- be the correct **file format,**
- have **fields that match the template downloaded** (do not remove, or change the order of fields),
- have extant values in **mandatory fields** (see Table 1),

### FILE FORMAT
- The incidental occurrence data template is a [UTF-8](#appendix-i-utf-8) encoded csv (not Microsoft
Excel Spreadsheets). Be sure to save this file with your data as a .csv (UTF-8) as follows,
otherwise it will not pass the csv validation step upon upload.
<br>`[MS Excel: Save As > More options > Tools > Web options > Save this document as >
Unicode (UTF-8)]`
- **Do not include empty rows**.

### FILE NAME

When making a manual submission to the Biodiversity Data Repository,
the file name must include the version number
of this biodiversity data template (`v{{ metadata.version }}`).
The following format is an example of a valid file name:

`data_descripion-v{{ metadata.version }}-additional_description.csv`

where:

* `data_description`: A short description of the data (e.g. `incidental_occ`, `test_data`).
* `v{{ metadata.version }}`: The version number of this template.
* `additional_description`: (Optional) Additional description of the data, if needed (e.g. `test_data`).
* `.csv`: Ensure the file name ends with `.csv`.

For example, `incidental_occ_delete-v{{ metadata.version }}-test_data.csv` or `test_data-v{{ metadata.version }}.csv`

### FILE SIZE
MS Excel imposes a limit of 1,048,576 rows on a spreadsheet, limiting a CSV file to the
header row followed by 1,048,575 occurrences. Furthermore, MS Excel has a 32,767 character
limit on individual cells in a spreadsheet. These limits may be overcome by using or
editing CSV files with other software.

Larger datasets may be more readily ingested using the API interface. Please contact
<bdr-support@gaiaresources.com.au> to make us aware of your data needs.

## TEMPLATE FIELDS
The template contains the field names in the top row. Table 1 will assist you in transferring
your data to the template indicating:

- **Field name** in the template;
- **Description** of the field;
- **Required** i.e. whether the field is **<font color="Crimson">mandatory</font>,
<font color="DarkGoldenRod">conditionally mandatory</font>, or optional**;
- **Format** (datatype) required for the data values for example text (string), number
  (integer, float), or date;
- **Example** of an entry or entries for that field;


<ins>Table 1: Incidental occurrence delete template fields with descriptions, conditions,
datatype format, and examples.</ins>

{{tables.fields}}


## APPENDICES

### APPENDIX-I: UTF-8
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

When working with text data, it's generally a good idea to use UTF-8 encoding to avoid
issues related to character representation and ensure that your software can handle a
diverse set of characters and languages.

For assistance, please contact: <bdr-support@gaiaresources.com.au>

{% endblock %}
