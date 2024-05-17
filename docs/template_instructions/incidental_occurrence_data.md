Put here the **incidental occurrence data** instructions

{{ version }}

# INCIDENTAL OCCURRENCE DATA
TEMPLATE INSTRUCTIONS
## OVERVIEW
Use this template to record occurrence data; that is the presence or absence of an organism
at a particular site locality at a point in time.  

Templates have been provided to facilitate integration of your data into the Biodiversity Data
Repository database. Not all types of data have been catered for in the available templates
at this stage; therefore, if you are unable to find a suitable template, please contact
bdr-support@gaiaresources.com.au to make us aware of your data needs.  

### NEED TO KNOW
For data validation, you will need your data file to:
* be the correct file format,
* have matching template fields to the template downloaded (do not remove, or
change the order of fields), however
* additional fields may be added after the templated fields (noting that the data type
is not assumed and values will be encoded as strings),
* have populated the relevant fields using the correct data type (for example dates for
date fields),
* have values in mandatory fields (see Table 1),
* comply with data value constraints for example the geographic coordinates are
consistent with a geodeticDatum type of the five available options, and
* align with existing controlled vocabularies wherever possible (this is mandatory for
geodeticDatum), but new terms may be submitted for consideration and will not
cause a validation error.
### FILE FORMAT
* The incidental occurrence data template is a UTF-8 encoded csv (not Microsoft Excel
Spreadsheets). Be sure to save this file with your data as a .csv (UTF-8) as follows,
otherwise it will not pass the csv validation step upon upload.  
*[MS Excel: Save As > More options > Tools > Web options > Save this document as >
Unicode (UTF-8)]*
* Do not include empty rows.
### FILE SIZE
MS Excel imposes a limit of **1,048,576** rows on a spreadsheet, limiting a CSV file to the
header row followed by 1,048,575 occurrences. Furthermore, MS Excel has a **32,767**
character limit on individual cells in a spreadsheet. These limits may be overcome by using
or editing CSV files with other software.
1
Larger datasets may be more readily ingested using the API interface. Please contact
[bdr-support@gaiaresources.com.au](mailto:bdr-support@gaiaresources.com.au) to make us aware of your data needs.
TEMPLATE FIELDS
The template contains the field names in the top row. Table 1 will assist you in transferring
your data to the template indicating:
* Field name in the template (and an external link to the Darwin Core standard for that
field where relevant);
* Description of the field;
* Required whether the field is mandatory or optional;
* Format (datatype) required for the data values for example text (string), number
(integer, float), or date;
* Example of an entry or entries for that field; and
* Vocabulary links within this document (for example pick list values) where relevant.
The fields that have suggested values options for the fields in Table 1 are listed in
Table 2 in alphabetical order of field name.
### ADDITIONAL FIELDS
Data that do not match the existing template fields may be added as additional columns in
the CSV files after the templated fields.
E.g., eventRemarks, associatedTaxa, pathway.

{{ insert schema table here }}