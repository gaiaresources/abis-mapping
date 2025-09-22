---
title: Systematic Survey Occurrence Data Template - v1.0.0
 - Archived

summary: A template to translate some Darwin Core fields
---
<small>
**survey_occurrence_data** v1.0.0
</small>


!!! failure "Template Archived"

    This Template is archived, and is no longer available for use.


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
contact <bdr-support@dcceew.gov.au> to make us aware of your data needs.

#### Data Validation Requirements:
For data validation, you will need your data file to:

- be in the correct **file format,**
- have **fields that match the template downloaded** (do not remove, or 
  change the order of fields),
- have extant values for **mandatory fields** (see Table 1),
- comply with all **data value constraints**; for example the geographic coordinates are
  consistent with a [geodeticDatum](#geodeticDatum-vocabularies) type of the ***5*** available
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
<bdr-support@dcceew.gov.au> to make us aware of your data needs.

## TEMPLATE FIELDS
The template contains the field names in the top row. Table 1 will assist you in transferring
your data to the template by providing guidance on:

- **Field name** in the template (and an external link to the [Darwin Core standard](https://dwc.tdwg.org/terms/)
  for that field where relevant);
- **Description** of the field;
- **Required** i.e. whether the field is **<font color="Crimson">mandatory</font>,
<font color="DarkGoldenRod">conditionally mandatory</font>, or optional**;
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

|Field #|Name|Description|Mandatory / Optional|Datatype Format|Examples|
|:---:|:---|:---|:---:|:---:|:---|
|1|<a name="providerRecordID-field"></a>providerRecordID|Unique (within provider) identifier for the record.|**<font color="Crimson">Mandatory</font>**|String|8022FSJMJ079c5cf|
|2|<a name="providerRecordIDSource-field"></a>providerRecordIDSource|Person or Organisation that generated the providerRecordID. For providers registered with the BDR, this field should contain your BDR registrationID. Populate only if the details are different from the dataset submission details.|**<font color="Crimson">Mandatory</font>**|String|Western Australian Biodiversity Information Office|
|3|<a name="locality-field"></a>[locality](https://dwc.tdwg.org/terms/#dwc:locality)|The specific description of the place.|Optional|String|Cowaramup Bay Road|
|4|<a name="decimalLatitude-field"></a>[decimalLatitude](https://dwc.tdwg.org/terms/#dwc:decimalLatitude)|The geographic latitude (in decimal degrees, using the spatial reference system given in geodeticDatum) of the geographic centre of a Location. Positive values are north of the Equator, negative values are south of it. Valid coordinate ranges for the BDR system are within and inclusive of -90 to 0.|**<font color="Crimson">Mandatory</font>**|Number|-33.812314|
|5|<a name="decimalLongitude-field"></a>[decimalLongitude](https://dwc.tdwg.org/terms/#dwc:decimalLongitude)|The geographic longitude (in decimal degrees, using the spatial reference system given in geodeticDatum) of the geographic centre of a Location. Positive values are east of the Greenwich Meridian, negative values are west of it. Valid coordinate ranges for the BDR system are within and inclusive of 0 to 180.|**<font color="Crimson">Mandatory</font>**|Number|115.231512|
|6|<a name="geodeticDatum-field"></a>[geodeticDatum](https://dwc.tdwg.org/terms/#dwc:geodeticDatum)|The acronym for the ellipsoid, geodetic datum, or spatial reference system (SRS) upon which the geographic (non-projected) coordinates given in decimalLatitude and decimalLongitude as based.|**<font color="Crimson">Mandatory</font>**|String|WGS84<br>([Vocabulary link](#geodeticDatum-vocabularies))|
|7|<a name="coordinateUncertaintyInMeters-field"></a>[coordinateUncertaintyInMeters](https://dwc.tdwg.org/terms/#dwc:coordinateUncertaintyInMeters)|The horizontal distance (in metres) from the given decimalLatitude and decimalLongitude describing the smallest circle containing the whole of the Location. Leave the value empty if the uncertainty is unknown, cannot be estimated, or is not applicable (because there are no coordinates). Zero is not a valid value for this term.|Optional|Number|50.0|
|8|<a name="dataGeneralizations-field"></a>[dataGeneralizations](https://dwc.tdwg.org/terms/#dwciri:dataGeneralizations)|Actions taken to make the shared data less specific or complete than in its original form, due to restrictions around identifying locations of particular species. Suggests that alternative data of higher quality may be available on request.|Optional|String|Coordinates rounded to the nearest 10 km for conservation concern|
|9|<a name="eventDate-field"></a>[eventDate](https://dwc.tdwg.org/terms/#dwc:eventDate)|The date (with precision of year (YYYY), month year (YYYY-MM) or date in the following formats DD/MM/YYYY or YYYY-MM-DD are accepted) or date-time without timezone (in ISO 8601 format for example 2021-07-11T06:23:00) or date-time with timezone(in ISO 8601 format for example 2022-05-20T06:23:00+08:00) during which a species occurrence was observed. For occurrences, this is the date-time when the event was recorded. Not suitable for a time in a geological context.|**<font color="Crimson">Mandatory</font>**|Timestamp|2019-09-23T14:03+08:00|
|10|<a name="samplingProtocol-field"></a>[samplingProtocol](https://dwc.tdwg.org/terms/#dwciri:samplingProtocol)|The sampling protocol is the method used to sample the locality to determine the presence (or absence) of the taxon referred to in this record at the indicated time. This may be a collecting method or a method to observe an organism without collection.<br>Recommended best practice is to describe a species occurrence with no more than one sampling protocol. In the case of a summary, in which a specific protocol can not be attributed to specific species occurrences, the recommended best practice is to repeat the property for each IRI that denotes a different sampling protocol that applies to the occurrence.|Optional|String|Human Observation<br>([Vocabulary link](#samplingProtocol-vocabularies))|
|11|<a name="basisOfRecord-field"></a>[basisOfRecord](https://dwc.tdwg.org/terms/#dwc:basisOfRecord)|The specific nature of the data record.|Optional|String|Preserved Specimen<br>([Vocabulary link](#basisOfRecord-vocabularies))|
|12|<a name="recordedBy-field"></a>[recordedBy](https://dwc.tdwg.org/terms/#dwciri:recordedBy)|A person, group, or organisation responsible for recording the original Occurrence.|Optional|String|Stream Environment and Water Pty Ltd|
|13|<a name="recordNumber-field"></a>[recordNumber](http://rs.tdwg.org/dwc/terms/recordNumber)|An identifier given to the Occurrence at the time it was recorded. Often serves as a link between field notes and an Occurrence record, such as a specimen collector's number.|Optional|String|PE:12:8832|
|14|<a name="occurrenceStatus-field"></a>[occurrenceStatus](https://dwc.tdwg.org/terms/#dwc:occurrenceStatus)|A statement about the presence or absence of a Taxon at a Location.|Optional|String|Present<br>([Vocabulary link](#occurrenceStatus-vocabularies))|
|15|<a name="habitat-field"></a>[habitat](http://rs.tdwg.org/dwc/terms/habitat)|A category or description of the habitat in which the event occurred.|Optional|String|Closed forest of Melaleuca lanceolata. White, grey or brown sand, sandy loam.|
|16|<a name="establishmentMeans-field"></a>[establishmentMeans](https://dwc.tdwg.org/terms/#dwc:establishmentMeans)|Statement about whether an organism or organisms have been introduced to a given place and time through the direct or indirect activity of modern humans.|Optional|String|Native<br>([Vocabulary link](#establishmentMeans-vocabularies))|
|17|<a name="organismRemarks-field"></a>[organismRemarks](http://rs.tdwg.org/dwc/terms/organismRemarks)|Comments or notes about the Organism instance.|Optional|String|Dried out leaf tips.|
|18|<a name="individualCount-field"></a>[individualCount](https://dwc.tdwg.org/terms/#dwc:individualCount)|The number of individuals present at the time of the Occurrence. 0 = none, no value = the specific number was not recorded.|Optional|Integer|26|
|19|<a name="organismQuantity-field"></a>[organismQuantity](https://dwc.tdwg.org/list/#dwc_organismQuantity)|A number or enumeration value for the quantity of organisms.|**<font color="DarkGoldenRod">Conditionally mandatory with organismQuantityType</font>**|Number|12.5|
|20|<a name="organismQuantityType-field"></a>[organismQuantityType](https://dwc.tdwg.org/list/#dwc_organismQuantityType)|The type of quantification system used for the quantity organisms.|**<font color="DarkGoldenRod">Conditionally mandatory with organismQuantity</font>**|String|% biomass<br>([Vocabulary link](#organismQuantityType-vocabularies))|
|21|<a name="lifeStage-field"></a>[lifeStage](http://rs.tdwg.org/dwc/terms/lifeStage)|The age class or life stage of the Organism(s) at the time the Occurrence was recorded.|Optional|String|adult<br>([Vocabulary link](#lifeStage-vocabularies))|
|22|<a name="sex-field"></a>[sex](https://dwc.tdwg.org/terms/#dwciri:sex)|The sex of the biological individual(s) represented in the Occurrence.|Optional|String|Unspecified<br>([Vocabulary link](#sex-vocabularies))|
|23|<a name="reproductiveCondition-field"></a>[reproductiveCondition](https://dwc.tdwg.org/terms/#dwc:reproductiveCondition)|The reproductive condition of the biological individual(s) represented in the Occurrence.|Optional|String|No breeding evident|
|24|<a name="ownerRecordID-field"></a>ownerRecordID|Identifier given to the occurrence by the owner of the data. Populate this field if the data owner is different to the data provider. Unique (within data owner) identifier for the record.|**<font color="DarkGoldenRod">Conditionally mandatory with ownerRecordIDSource</font>**|String|12345NT521mc5h|
|25|<a name="ownerRecordIDSource-field"></a>ownerRecordIDSource|Person or Organisation that generated the ownerRecordID. For organisations registered with the BDR, this field should contain the BDR registrationID. For all others, please provide the name of Person or Organisation who owns the data.|**<font color="DarkGoldenRod">Conditionally mandatory with ownerRecordID</font>**|String|WAM|
|26|<a name="collectionCode-field"></a>[collectionCode](https://dwc.tdwg.org/terms/#dwc:collectionCode)|The name, acronym, code, or initialism identifying the collection or data set from which the record was derived. It is associated with the catalogNumber.|Optional|String|ARACH|
|27|<a name="catalogNumber-field"></a>[catalogNumber](http://rs.tdwg.org/dwc/terms/catalogNumber)|An identifier (preferably unique) for the record within the data set or collection.|**<font color="DarkGoldenRod">Conditionally mandatory with catalogNumberSource</font>**|String|145732, 145732a, 2008.1334, R-4313|
|28|<a name="catalogNumberSource-field"></a>catalogNumberSource|Organisation that generated the catalogNumber. In the BDR context, this is likely to be a collecting institution where a specimen or material sample is located. For organisations registered with the BDR, this field should contain the BDR registrationID. For all others, please provide the name of Person or Organisation.|**<font color="DarkGoldenRod">Conditionally mandatory with catalogNumber</font>**|String|Western Australian Museum|
|29|<a name="otherCatalogNumbers-field"></a>[otherCatalogNumbers](http://rs.tdwg.org/dwc/terms/otherCatalogNumbers)|A list (concatenated and separated with a space vertical bar space ( \| )) of previous or alternate fully qualified catalog numbers or other human-used identifiers for the same Occurrence, whether in the current or any other data set or collection.|**<font color="DarkGoldenRod">Conditionally mandatory with otherCatalogNumbersSource</font>**|List|BHP2012-7521 \| M12378|
|30|<a name="otherCatalogNumbersSource-field"></a>otherCatalogNumbersSource|Organisation that generated the otherCatalogNumbers. For organisations registered with the BDR, this field should contain the BDR registrationID. For all others, please provide the name of Person or Organisation.|**<font color="DarkGoldenRod">Conditionally mandatory with otherCatalogNumbers</font>**|String|University of Western Australia|
|31|<a name="preparations-field"></a>[preparations](http://rs.tdwg.org/dwc/terms/preparations)|A list (concatenated and separated with a space vertical bar space ( \| )) of preparations and preservation methods for a specimen.|Optional|String|alcohol<br>([Vocabulary link](#preparations-vocabularies))|
|32|<a name="preparedDate-field"></a>preparedDate|The date (with precision of year (YYYY), month year (YYYY-MM) or date in the following formats DD/MM/YYYY or YYYY-MM-DD are accepted) or date-time without timezone (in ISO 8601 format for example 2021-07-11T11:23:00) or date-time with timezone(in ISO 8601 format for example 2022-05-20T06:23:00+08:00) representing the date or date-time the specimen was prepared.|Optional|Timestamp|2019-09-24|
|33|<a name="associatedSequences-field"></a>[associatedSequences](http://rs.tdwg.org/dwc/terms/associatedSequences)|A list (concatenated and separated with a space vertical bar space ( \| )) of identifiers (publication, global unique identifier, URI) of genetic sequence information associated with the Occurrence.|Optional|List|https://www.ncbi.nlm.nih.gov/nuccore/MH040669.1 \| https://www.ncbi.nlm.nih.gov/nuccore/MH040616.1|
|34|<a name="sequencingMethod-field"></a>sequencingMethod|The method used to obtain sequence data for example DNA, RNA, or protein from the sample.|Optional|String|Sanger-dideoxy-sequencing<br>([Vocabulary link](#sequencingMethod-vocabularies))|
|35|<a name="verbatimIdentification-field"></a>[verbatimIdentification](https://dwc.tdwg.org/terms/#dwc:verbatimIdentification)|A string representing the taxonomic identification as it appeared in the original record. This term is meant to allow the capture of an unaltered original identification/determination, including identification qualifiers, hybrid formulas, uncertainties, etc. This term is meant to be used in addition to scientificName (and identificationQualifier etc.), not instead of it.|Optional|String|Caladenia ?excelsa|
|36|<a name="dateIdentified-field"></a>[dateIdentified](http://rs.tdwg.org/dwc/terms/dateIdentified)|The date (with precision of year (YYYY), month year (YYYY-MM) or date in the following formats DD/MM/YYYY or YYYY-MM-DD are accepted) or date-time without timezone (in ISO 8601 format for example 2021-07-11T11:23:00) or date-time with timezone(in ISO 8601 format for example 2022-05-20T06:23:00+08:00) on which the subject was determined as representing the Taxon.|Optional|Timestamp|2019-09-24|
|37|<a name="identifiedBy-field"></a>[identifiedBy](http://rs.tdwg.org/dwc/terms/identifiedBy)|Group of names, organisations who assigned the Taxon to the subject. For multiple names, use the pipe separator ( \| ).|Optional|String|J. Doe \| WAM|
|38|<a name="identificationMethod-field"></a>identificationMethod|Method used to associate the organism with the scientificName label.|Optional|String|DNA<br>([Vocabulary link](#identificationMethod-vocabularies))|
|39|<a name="scientificName-field"></a>[scientificName](http://rs.tdwg.org/dwc/terms/scientificName)|The full scientific name, with authorship and date information if known. When forming part of an Identification, this should be the name in lowest level taxonomic rank that can be determined. This term should not contain identification qualifications, which should instead be supplied in the identificationQualifier column.<br>NOTE: Phrase names such as Rhagodia sp. Hamersley (M.Trudgen 17794) are permitted in the scientificName field where those are in use.|**<font color="Crimson">Mandatory</font>**|String|Caladenia excelsa|
|40|<a name="identificationQualifier-field"></a>[identificationQualifier](https://dwc.tdwg.org/terms/#dwc:identificationQualifier)|A brief phrase or a standard term ("cf.", "aff.") to express the determiner's doubts about the Identification.|Optional|String|Species incerta<br>([Vocabulary link](#identificationQualifier-vocabularies))|
|41|<a name="identificationRemarks-field"></a>[identificationRemarks](http://rs.tdwg.org/dwc/terms/identificationRemarks)|Comments or notes about the Identification.|Optional|String|DNA evidence may indicate a new species. Further analysis required.|
|42|<a name="acceptedNameUsage-field"></a>[acceptedNameUsage](https://dwc.tdwg.org/terms/#dwc:acceptedNameUsage)|The full name, with authorship and date information if known, of the currently valid (zoological) or accepted (botanical) taxon.|Optional|String|Occiperipatoides gilesii (Spencer, 1909)|
|43|<a name="kingdom-field"></a>[kingdom](https://dwc.tdwg.org/terms/#dwc:kingdom)|The full scientific name of the kingdom in which the taxon is classified.|**<font color="Crimson">Mandatory</font>**|String|Plantae<br>([Vocabulary link](#kingdom-vocabularies))|
|44|<a name="taxonRank-field"></a>[taxonRank](http://rs.tdwg.org/dwc/terms/verbatimTaxonRank)|The taxonomic rank of the most specific name in the scientificName.|Optional|String|Species<br>([Vocabulary link](#taxonRank-vocabularies))|
|45|<a name="threatStatus-field"></a>threatStatus|The conservation status (or code) assigned to an organism that is recognised in conjunction with a specific jurisdiction.|**<font color="DarkGoldenRod">Conditionally mandatory with conservationJurisdiction</font>**|String|EN<br>([Vocabulary link](#threatStatus-vocabularies))|
|46|<a name="conservationJurisdiction-field"></a>conservationJurisdiction|The jurisdiction under which an organism is recognised to have a specific conservation status applied.|**<font color="DarkGoldenRod">Conditionally mandatory with threatStatus</font>**|String|EPBC, WA<br>([Vocabulary link](#conservationJurisdiction-vocabularies))|
|47|<a name="threatStatusCheckProtocol-field"></a>threatStatusCheckProtocol|The method used to determine if the organism is listed under the relevant jurisdictional threatened species list.|Optional|String|Species name check of the Department of Climate Change, Energy, the Environment and Water’s Species Profile and Threat Database http://www.environment.gov.au/cgi-bin/sprat/public/sprat.pl<br>([Vocabulary link](#threatStatusCheckProtocol-vocabularies))|
|48|<a name="threatStatusDateDetermined-field"></a>threatStatusDateDetermined|The date (with precision of year (YYYY), month year (YYYY-MM) or date in the following formats DD/MM/YYYY or YYYY-MM-DD are accepted) or date-time without timezone (in ISO 8601 format for example 2021-07-11T11:23:00) or date-time with timezone(in ISO 8601 format for example 2022-05-20T06:23:00+08:00) on which this record of this organism was assigned to the nominated threatStatus and conservationJurisdiction|Optional|Timestamp|30/08/2022|
|49|<a name="threatStatusDeterminedBy-field"></a>threatStatusDeterminedBy|The person and/organisation responsible for appending the threatStatus and conservationJurisdiction to this organism’s occurrence record.|Optional|String|WA-BIO|
|50|<a name="siteID-field"></a>siteID|Corresponds to a unique site identifier, provided within accompanying survey_site_data.csv template.|Optional|String|P1|
|51|<a name="surveyID-field"></a>surveyID|The identifier of the Survey that the occurrence comes from. This field should be completed if it is ambiguous as to which survey the occurrence belongs to.|Optional|String|AR220-01|


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

|Template field name|Preferred label|Definition|Alternate label|
|:---|:---|:---|:---|
|<a name="basisOfRecord-vocabularies"></a>basisOfRecord|FOSSIL SPECIMEN|A preserved specimen that is a fossil.||
|basisOfRecord|HUMAN OBSERVATION|An output of a human observation.||
|basisOfRecord|LIVING SPECIMEN|A specimen that is alive.||
|basisOfRecord|MACHINE OBSERVATION|An output of a machine observation process.||
|basisOfRecord|MATERIAL SAMPLE|A physical result of a sampling (or subsampling) event. In biological collections, the material sample is typically collected, and either preserved or destructively processed.||
|basisOfRecord|OCCURRENCE|An existence of an Organism (sensu http://rs.tdwg.org/dwc/terms/Organism) at a particular place at a particular time.||
|basisOfRecord|PRESERVED SPECIMEN|A specimen that has been preserved.||
|<a name="establishmentMeans-vocabularies"></a>establishmentMeans|INTRODUCED|Establishment of a taxon by numan agency into an area that is not part of its natural range.||
|establishmentMeans|INTRODUCED ASSISTED COLONISATION|Establishment of a taxon specifically with the intention of creating a self-sustaining wild population in an area that is not part of the taxon's natural range.|ASSISTED COLONISATION|
|establishmentMeans|NATIVE|A taxon occurring within its natural range.|NATIVE (INDIGENOUS)|
|establishmentMeans|NATIVE REINTRODUCED|A taxon re-established by direct introduction by humans into an area that is not part of its natural range, but from where it had become extinct.|NATIVE: REINTRODUCED|
|establishmentMeans|UNCERTAIN|The origin of the occurrence of the taxon in an area is obscure.|UNKNOWN, CRYPTOGENIC|
|establishmentMeans|VAGRANT|The temporary occurrence of a taxon far outside its natural or migratory range.|CASUAL|
|<a name="geodeticDatum-vocabularies"></a>geodeticDatum|AGD66|Australian Geodetic Datum 1966|EPSG:4202|
|geodeticDatum|AGD84|Australian Geodetic Datum 1984|EPSG:4203|
|geodeticDatum|GDA2020|Geocentric Datum of Australia 2020|EPSG:7844|
|geodeticDatum|GDA94|Geocentric Datum of Australia 1994|EPSG:4283|
|geodeticDatum|WGS84|World Geodetic System 1984, used in GPS|EPSG:4326|
|<a name="identificationMethod-vocabularies"></a>identificationMethod|TBC|TBC||
|<a name="identificationQualifier-vocabularies"></a>identificationQualifier|ANIMALIA CETERA|It groups all the unidentified specimens that are not listed as separate taxa. The term cetera (abbreviated c. or cet.) may be applied to a given high-rank taxon, meaning that identification at a lower taxonomic level has not been attempted (see also stetit) but explicitly not including subordinate taxa that may have been identified.|A.C.|
|identificationQualifier|CONFER|"Compare with". Specimens should be compared to reference material, since most of the diagnostic characters correspond to a given species but some are unclear. Also used in the sense of affinis and species incerta (these usages are discouraged).|CF., CFR., CONF., SP. CF.|
|identificationQualifier|EX GREGE|"Of the group including". The specimen has some affinity to a known species or it belongs to a species group or species complex; see also affinis and species proxima.|EX GR., GR.|
|identificationQualifier|FAMILIA GENUS SPECIES|The specimen has not been attributed to any known species nor family; see also species.|FAM. GEN. SP.|
|identificationQualifier|GENUS ET SPECIES NOVA|The specimen is considered to belong to a new species and a new genus; for more details, see species nova.|GEN. ET SP., GEN. NOV., SP. NOV., NOV. GEN. ET SP.|
|identificationQualifier|GENUS NOVUM|The specimen is considered to belong to a new species and a new genus; for more details, see species nova|GEN. NOV., G. NOV., GEN. N., G. N., NOV. GEN|
|identificationQualifier|GENUS SPECIES|The specimen has not been related to any known species nor genus; also species.|GEN. SP., G. SP.|
|identificationQualifier|SPECIES|The specimen has not been identified, nor it has been related to any known species; the uncertainty is potentially provisional: it could be due to the lack of suitable dichotomous keys, or to the occurrence of a species not previously described. Also used in the sense of species indeterminabilis and stetit (these usages are discouraged.|SP|
|identificationQualifier|SPECIES AFFINIS|"Has affinity with". The specimen has some affinity to a known species but it is not identical to it; it generally implies distinction more than a possible identity, in contrast with the qualifier confer; see also species Proxima and ex grege. It is often used in combination with the ON qualifier species nova. Also used in the sense of confer (this usage is discouraged).|AFF., SP. AFF.|
|identificationQualifier|SPECIES INCERTA|The identification is uncertain; it usually indicates a higher reliability with ?, sp. Inc respect to confer. The sign "sp. inc." is also used in the sense of species, species indeterminabilis and species inquirenda (these usages are discouraged).|SP. INC.|
|identificationQualifier|SPECIES INDETERMINABILIS|The specimen is indeterminable beyond a certain taxonomic level due to the deterioration or lack of diagnostic characters. Also used in the sense of species and stetit (these usages are discouraged.|INDET., IND., SP. INDET., SP. IND.|
|identificationQualifier|SPECIES NOVA|The specimen is considered to belong to a new, previously undescribed (1) When describing a new species, the use of the qualifier is required by the ICZN (1999) to explicitly indicate the taxa name as intentionally new. (2) Used as ON qualifier to refer to a new, still unnamed species before the formal publication of the description.|SP. NOV., SPEC. NOV., SP. N., NOV. SP., NOV. SPEC., N. SP.|
|identificationQualifier|SPECIES PROXIMA|The specimen is near to a known species but it is not identical to it; see also affinis and ex grege.|PROX., SP. PROX., NR., SP.NR.|
|identificationQualifier|STETIT|Identification at a lower taxonomic level has not been attempted, even if allowed by the sample conditions. It may also be used when more records with different ON qualifiers need to be merged at a safe taxonomic level.|STET.|
|identificationQualifier|SUBSPECIES|The only infraspecific rank regulated by the ICZN (1999). As ON qualifier, it indicates that the specimen probably belongs to a subspecies but it has not been related to any known one; see also species.|SSP., SUBSP.|
|<a name="kingdom-vocabularies"></a>kingdom|ANIMALIA|Kingdom Animalia||
|kingdom|FUNGI|Kingdom (taxonRank: Regnum) Fungi||
|kingdom|PLANTAE|Kingdom (taxonRank: Regnum) Plantae|PLANTAE HAECKEL|
|<a name="lifeStage-vocabularies"></a>lifeStage|ADULT|An adult is a plant, animal, or person who has reached full growth or alternatively is capable of reproduction.|IMAGO|
|lifeStage|EMBRYO|An embryo is a multicellular diploid eukaryote in its earliest stage of development, from the time of first cell division until birth, hatching, or germination.|EGG, SEED|
|lifeStage|GAMETE|A gamete is a cell that fuses with another gamete during fertilisation in organisms that reproduce sexually. In species that produce two morphologically distinct types of gametes, and in which each individual produces only one type, a female is any individual that produces the larger type of gamete — called an ovum (or egg) — and a male produces the smaller tadpole-like type — called a sperm. This is an example of anisogamy or heterogamy, the condition wherein females and males produce gametes of different sizes. In contrast, isogamy is the state of gametes from both sexes being the same size and shape, and given arbitrary designators for mating type. Gametes carry half the genetic information of an individual, one chromosome of each type.|OVUM, SPERM, POLLEN|
|lifeStage|GAMETOPHYTE|In plants and algae that undergo alternation of generations, a gametophyte is the multicellular structure, or phase, that is haploid, containing a single set of chromosomes. The gametophyte produces male or female gametes (or both), by a process of cell division called mitosis. In mosses, liverworts and hornworts (bryophytes), the gametophyte is the commonly known phase of the plant. An early developmental stage in the gametophyte of mosses (immediately following germination of the meiospore) is called the protonema. In most other land plants the gametophyte is very small (as in ferns and their relatives) or even reduced as in flowering plants (angiosperms), where the female gametophyte (ovule) is known as a megagametophyte and the male gametophyte (pollen) is called a microgametophyte.|GAMONT, PROTONEMA, POLLEN, OVULE|
|lifeStage|JUVENILE|A juvenile is an individual organism that has not yet reached its adult form, sexual maturity or size. Juveniles sometimes look very different from the adult form, particularly in terms of their colour. In many organisms the juvenile has a different name from the adult.|SEEDLING, EFT, CALF, HATCHLING, INFANT, FOAL, KITTEN, KIT, CHICK, NYMPH, FAWN, WHELP, PUP, ELVER, FRY|
|lifeStage|LARVA|A larva (Latin; plural larvae) is a young (juvenile) form of animal with indirect development, going through or undergoing metamorphosis (for example, insects, amphibians, or cnidarians). The larva can look completely different from the adult form, for example, a caterpillar differs from a butterfly. Larvae often have special (larval) organs which do not occur in the adult form. The larvae of some species can become pubescent and not further develop into the adult form (for example, in some newts). This is a type of neoteny. It is a misunderstanding that the larval form always reflects the group's evolutionary history. It could be the case, but often the larval stage has evolved secondarily, as in insects. In these cases the larval form might differ more from the group's common origin than the adult form. The early life stages of most fish species are considerably different from juveniles and adults of their species and are called larvae.|LARVAE, TADPOLE, POLLIWOG, POLLYWOG, POLLIWIG, POLEWIG, POLWIG, PLANULA, NAUPLIUS, ZOEA, NYMPH, CATERPILLAR|
|lifeStage|PUPA|A pupa is the life stage of some insects undergoing transformation between immature and mature stages. The pupal stage is found only in holometabolous insects, those that undergo a complete metamorphosis, with four life stages: egg (-> embryo), larva, pupa, and imago (-> adult).|PUPPE|
|lifeStage|SPORE|A spore is a reproductive structure that is adapted for dispersal and surviving for extended periods of time in unfavorable conditions. Spores form part of the life cycles of many bacteria, plants, algae, fungi and some protozoans. A chief difference between spores and seeds as dispersal units is that spores have very little stored food resources compared with seeds. Spores are usually haploid and unicellular and are produced by meiosis in the sporangium by the sporophyte. Once conditions are favorable, the spore can develop into a new organism using mitotic division, producing a multicellular gametophyte, which eventually goes on to produce gametes. Many ferns, especially those adapted to dry conditions, produce diploid spores. In this case spores are the units of asexual reproduction, because a single spore develops into a new organism. By contrast, gametes are the units of sexual reproduction, as two gametes need to fuse to create a new organism.||
|lifeStage|SPOROPHYTE|All land plants, and some algae, have life cycles in which a haploid gametophyte generation alternates with a diploid sporophyte, the generation of a plant or alga that has a double set of chromosomes. A multicellular sporophyte generation or phase is present in the life cycle of all land plants and in some green algae. For common flowering plants (Angiosperms), the sporophyte generation comprises almost their whole life cycle (that is whole green plant, roots etc), except phases of small reproductive structures (pollen and ovule).|AGAMONT|
|lifeStage|ZYGOTE|A zygote (or zygocyte) describes the first stage of a new unique organism blastomere when it consists of just a single cell. The term is also used more loosely to refer to the group of cells formed by the first few cell divisions, although this is properly referred to as a blastomere. A zygote is usually produced by a fertilisation event between two haploid cells - an ovum from a female and a sperm cell from a male - which combine to form the single diploid cell. Thus the zygote contains DNA originating from both mother and father and this provides all the genetic information necessary to form a new individual|BLASTOMERE|
|<a name="occurrenceStatus-vocabularies"></a>occurrenceStatus|ABSENT|The occurrence was not present at the location and time of the observation.||
|occurrenceStatus|PRESENT|The occurrence was present at the location and time of the observation.||
|<a name="organismQuantityType-vocabularies"></a>organismQuantityType|BIOMASS AFDG|A measurement type where the quantity of a species in a sample is recorded as the ash free dry weight biomass in grams (g).|BIOMASS ASH FREE DRY WEIGHT IN GRAMS, BIOMASS ASH FREE DRY WEIGHT GRAMS|
|organismQuantityType|BIOMASS G|A measurement type where the quantity of a species in a sample is recorded as the biomass in grams (g).|BIOMASS IN GRAMS, BIOMASS GRAMS|
|organismQuantityType|BIOMASS KG|A measurement type where the quantity of a species in a sample is recorded as the biomass in kilograms (kg).|BIOMASS IN KILOGRAMS, BIOMASS KILOGRAMS|
|organismQuantityType|BIOVOLUME CUBIC MICRONS|A measurement type where the quantity of a species in a sample is recorded as the biovolume in cubic microns (µ ^ 3).|BIOVOLUME IN CUBIC MICRONS|
|organismQuantityType|BIOVOLUME ML|A measurement type where the quantity of a species in a sample is recorded as the biovolume in millilitres (ml).|BIOVOLUME IN MILLILITRES, BIOVOLUME MILLILITRES|
|organismQuantityType|BRAUN BLANQUET SCALE|A measurement type where the cover of a species in a sample is recorded using the Braun-Blanquet scale.||
|organismQuantityType|DOMIN SCALE|A measurement type where the cover of a species in a sample is recorded using the Domin scale.||
|organismQuantityType|INDIVIDUALS|A measurement type where the quantity of a species in a sample is recorded as the number of individuals (e.g.per litre, per square metre, per cubic metre, per hour, per day).||
|organismQuantityType|PERCENTAGE COVERAGE|A measurement type where the quantity of a species in a sample is recorded as the percentage coverage of the total area being sampled.|% COVERAGE|
|organismQuantityType|PERCENTAGE OF BIOMASS|A measurement type where the quantity of a species in a sample is recorded as a percentage of the total biomass of all species.|% OF BIOMASS|
|organismQuantityType|PERCENTAGE OF BIOVOLUME|A measurement type where the quantity of a species in a sample is recorded as a percentage of the total biovolume of all species.|% OF BIOVOLUME|
|organismQuantityType|PERCENTAGE OF SPECIES|A measurement type where the quantity of a species in a sample is recorded as a percentage of the total individual count of all species.|% OF SPECIES|
|<a name="preparations-vocabularies"></a>preparations|ALCOHOL|Alcohol||
|preparations|DEEP FROZEN|Deep frozen||
|preparations|DRIED|Dried||
|preparations|DRIED AND PRESSED|Dried and pressed||
|preparations|FORMALIN|Formalin||
|preparations|FREEZE DRIED|Freeze-dried||
|preparations|GLYCERIN|Glycerin||
|preparations|GUM ARABIC|Gum arabic||
|preparations|MICROSCOPIC PREPARATION|Microscopic preparation||
|preparations|MOUNTED|Mounted||
|preparations|NO TREATMENT|No treatment||
|preparations|OTHER|Other||
|preparations|PINNED|Pinned||
|preparations|REFRIGERATED|Refrigerated||
|<a name="samplingProtocol-vocabularies"></a>samplingProtocol|ACOUSTIC RECORDING|An acoustic recorder is a device that emits a soundwave at a range of frequencies, and are used to detect and monitor biodiversity in a given area.||
|samplingProtocol|ANIMAL CARCASS (WHOLE)|Refers to the fauna observation method, i.e., any observations made on a carcass (whole), i.e., dead and or decaying animal., Refers to the type of voucher specimen sample, i.e., an animal carcass (full/complete).||
|samplingProtocol|ANIMAL DIGGINGS|The type of evidence of a pest animal presence in the form of 'diggings'.||
|samplingProtocol|ANIMAL GUT (WITHIN)|Animal gut is the portions of the alimentary canal, particularly the stomach and the intestines.||
|samplingProtocol|ANIMAL HAIR/FUR|Animal fur are densely packed hairs on the skin of mammals.||
|samplingProtocol|ANIMAL PELLET|Pellets are fecal droppings of animals such as goat, rats, rabbits, wombats, etc., and are often used as a sign/evidence of the presence of the species in the environment.||
|samplingProtocol|ANIMAL SKIN|Skin is the outermost protective layer and the largest organ covering the body of vertebrate animal.||
|samplingProtocol|ANIMAL TRACKING (STATELLITE)|A method of tracking the movements of fauna species facilitated by the assistance from satellite (i.e., imagery for example).||
|samplingProtocol|ANIMAL TRACKS|Animal tracks are signs in the form of marks or imprints left behind on soil, ground or any related surface indicating the presence of a fauna species., Refers to the fauna observation method, i.e., any signs of a fauna detected from observations of tracks.||
|samplingProtocol|BONE/TEETH|Bones/teeth are non-perishable remains of mammals that are often divided into skeleton (bones) and dentition (teeth).||
|samplingProtocol|BURROW|A burrow is a hole or tunnel excavated into the ground by an animal to create a space suitable for habitation, temporary refuge, or as a byproduct of locomotion., Burrow is a small tunnel or a hole made by certain ground-dwelling mammals as a place of refuge., Refers to the microhabitat where the targeted fauna was observed. A burrow is a hole or tunnel excavated into the ground by an animal to create a space suitable for habitation, temporary refuge, or as a byproduct of locomotion.||
|samplingProtocol|CAGE TRAP|A cage trap is a trap made of metal or galvanised mesh, normally used for trapping mammals., The equipment/method used during a passive, 'targeted fauna survey'. A cage trap is a trap made of metal or galvanised mesh and used in trapping mammals.||
|samplingProtocol|DNA|DNA, or deoxyribonucleic acid, is the hereditary material in almost all living organisms that carries the genetic instructions used in growth, development, functioning, and reproduction. It consists of two long chains of nucleotides twisted into a double helix, with sequences of four types of nitrogen bases (adenine, thymine, cytosine, and guanine) that encode genetic information.||
|samplingProtocol|EDNA|Environment DNA (eDNA) are the DNA that contains genetic information of living organisms representing a specific environmental and is usually sourced from soil, water, etc. , Refers to the method of identification of Vertebrate fauna. Taxon is identified using DNA sequencing techniques from environmental samples (eDNA).||
|samplingProtocol|EGGS/EGGSHELL|An animal egg, or ovum, is the female reproductive cell (gamete) in many animals and vay in shape, size and structure. Egg shells are outer protctive layer that surrounds the egg of many animals. The animal eggs/egg shells here represent particular life stage of animal and often used as a sign/evidence to detect their presence in its habitat.||
|samplingProtocol|ELLIOTT TRAP|The equipment/method used during a passive, 'fauna survey'. Elliott trapping is a technique used to trap small to medium sized mammals. The are usually hinged design that allows trapping to be conducted by folding into a compact panel and easy transport to field locations and storage., The equipment/method used during a passive, 'targeted fauna survey'. Elliott trapping is a technique used to trap small to medium sized mammals. The are usually hinged design that allows trapping to be conducted by folding into a compact panel and easy transport to field locations and storage.||
|samplingProtocol|EXOSKELETON|Exoskeleton is the outer rigid covering of an invertebrate fauna with its structural features generally intact.||
|samplingProtocol|FEATHER|Feathers are light, upright epidermal outgrowths that form the external covering of the body of birds. Feathers include the smaller down feathers and the larger contour and flight feathers., Refers to the type of voucher specimen sample. Feathers are one of the epidermal growths that form the distinctive outer covering, or plumage, on birds.||
|samplingProtocol|FOSSIL/SUBFOSSIL|Fossils are preserved remains of animal or plant parts, usually of a prehistoric origin. Whereas, a sub-fossil are remains (usually skeletal) of animals that are not ancient enough to qualify as a fossil.||
|samplingProtocol|FUNNEL TRAP|The equipment/method used in a 'fauna survey'. Funnel trap is a trapping method used in trapping insects/invertebrates. Funnel traps are made of nested black funnels (up to as many as 12). Insects fall through the funnels to a cup that is filled with a preservative., The equipment/method used in a 'targeted fauna survey'. Funnel trap is a trapping method used in trapping insects/invertebrates. Funnel traps are made of nested black funnels (up to as many as 12). Insects fall through the funnels to a cup that is filled with a preservative.||
|samplingProtocol|GPS TRACKING|Geospatial tracking devices are portable units designed to monitor and track location. They use satellite navigation to determine movement and establish geographic positions.||
|samplingProtocol|HAIR TUBE|Hair Tubes are short sections of PVC pipe lined with pieces of double-sided sticky-tape and useful to obtain hair/fur samples of animals., Refers to the targeted fauna observation method, i.e., any observations on a fauna made using 'Hair Tubes', which are short sections of PVC pipe lined with pieces of double-sided sticky-tape.||
|samplingProtocol|HARP TRAP|Refers to the fauna observation method, i.e., any observations made on a fauna captured in a 'Harp trap' (especially designed for bats). They are particularly useful in situations where bats in flight can be channeled through a natural funnel such as above a water course, a cave or mine entrance or a clear area within a forest.||
|samplingProtocol|HEARD|The method of bird sighting in the form of calls, or acoustic signals., The method of fauna sighting in the form of calls, or acoustic signals.||
|samplingProtocol|HUMAN OBSERVATION|An observation performed by a human.||
|samplingProtocol|LIGHT TRAP|Light trapping is designed for collecting flying insects attracted to ultra violet light and is useful for sampling insect populations., The equipment/method used during a passive, 'targeted fauna survey'. Light trapping is designed for collecting flying insects attracted to ultra violet light and is useful for sampling insect populations.||
|samplingProtocol|MALAISE TRAP|A Malaise trap is a type of insect trap primarily used to capture invertebrates. They are large, tent-like structure effective in capturing flying insects (e.g., members of Hymenoptera and Diptera)., Refers to the targeted fauna observation method, i.e., any observations on a fauna captured using a malaise trap. A Malaise trap is a type of insect trap primarily used to capture invertebrates. They are large, tent-like structure effective in capturing flying insects (e.g., members of Hymenoptera and Diptera).||
|samplingProtocol|MIST NET|Refers to the fauna observation method, i.e., any observations on a fauna captured using mist nets. The net is made of a very fine diameter cord, which is almost invisible when set up and is often used to capture birds, because they fail to see it, and fly straight into it., Refers to the targeted fauna observation method, i.e., any observations on a fauna captured using mist nets. The net is made of a very fine diameter cord, which is almost invisible when set up and is often used to capture birds, because they fail to see it, and fly straight into it.||
|samplingProtocol|NEST|A nest is a place of refuge to hold an animal's eggs or provide a place to live or raise offspring.||
|samplingProtocol|NO STATED METHOD|Refers to NO recognised method of observation stated for a target fauna.|UNSPECIFIED|
|samplingProtocol|NONE|Refers to No observation method of a target fauna., Refers to the targeted fauna observation method, i.e., 'No' standard observation methods were applied.||
|samplingProtocol|OBSERVATION METHOD - AFTER CALL PLAYBACK|After call playback, is a method used for fauna observations (usually birds) and involves pre-recorded call playback to detect the presence of a target species in the survey area.||
|samplingProtocol|OBSERVATION METHOD - ANIMAL DEN|A den is a place of refuge for many mammals and are usually either buried deep underground or built by the animal to create a secret shelter., Refers to the microhabitat where the fauna was observed. A den is a place of refuge for many mammals and are usually either buried deep underground or built by the animal to create a secret shelter.||
|samplingProtocol|OBSERVATION METHOD - ANIMAL ODOUR|Animal odour or pheromones are distinct secretions of animals, often used as a sign/evidence of their presence in its habitat., Refers to the type of fauna observation method, which involves detection of a fauna species via its odour or pheromones.||
|samplingProtocol|OTHER (SPECIFY)|Other types of liquid preservative used to store invertebrate samples., Refers to the any Other type of substrate/s used for fauna signs-based observation., Represents any 'Other' categorical collection NOT listed in the given collection., Represents any 'other' categorical collection NOT listed.||
|samplingProtocol|PAN TRAP|A pan trap is a type of insect trap primarily used to capture small invertebrates (e.g., members of Hymenoptera) and often used to sample the abundance and diversity of insects., Refers to the targeted fauna observation method, i.e., any observations made from fauna captures in a pan trap. A pan trap is a type of insect trap primarily used to capture small invertebrates (e.g., members of Hymenoptera) and often used to sample the abundance and diversity of insects., The type/method of invertebrate fauna sampling implemented. Pan trapping consists of small, coloured bowls placed on the ground, either filled with water and a small amount of dishwashing liquid for sampling over one day, or propylene glycol for sampling over a longer duration.||
|samplingProtocol|PELLET (WITHIN)|Pellets are fecal droppings of animals such as goat, rats, rabbits, wombats, etc., and are often used as a sign/evidence of the presence of the species in the environment. 'Within pellet' here represents an observation method (tier-2) that involves searching for any signs/evidence of a fauna species within a scat.||
|samplingProtocol|PITFALL TRAP|Refers to the fauna observation method, i.e., any observations made from fauna captures in a pitfall trap. A pitfall trap is a simple device used to catch small animals , particularly insects and other invertebrates , that spend most of their time on the ground., Refers to the targeted fauna observation method, i.e., any observations made from fauna captures in a pitfall trap. A pitfall trap is a simple device used to catch small animals , particularly insects and other invertebrates , that spend most of their time on the ground.||
|samplingProtocol|RADIO TRACKING|Refers to the fauna observation method, i.e., any signs of a fauna with the assistance of radio tracking device/s.||
|samplingProtocol|REMOTE CAMERA DEVICE|Remote camera device are special devices that can be programmed to capture media (picture, videos) in places where humans cannot be physically present, and can be controlled remotely over a wireless network.||
|samplingProtocol|SCATS|Faeces/faecal pellets/dung/droppings of animals. Often individual or scattered pellets (e.g. rabbit), or clumped pellet groups (e.g. deer). Their deposition will be influenced by diet (wet diet often causes clumping of pellets) and their size can reflect age (adult/juvenile). Scat surveys provide an estimate of relative abundances suitable for both herbivores and predators.||
|samplingProtocol|SCATS (WITHIN)|Scats are fecal droppings of animals and are often represented by most to mark their territory. 'Within scats' here represents an observation method (tier-2) that involves searching for any signs/evidence of a fauna species within a scat.||
|samplingProtocol|SCENT PAD|Scent pads are specific pads that are used as lures duing fauna observations.||
|samplingProtocol|SCRATCHINGS (ARBOREAL)|Refers to the fauna observation method, i.e., any signs of a fauna detected from observations of scratchings on a tree.||
|samplingProtocol|SCRATCHINGS (GROUND)|Scratchings are common traits of certain mammals leaving scars on trees, rocks etc.||
|samplingProtocol|SHELL|A shell is a hard, rigid outer layer, which has evolved in a very wide variety of different animals, including molluscs, crustaceans, turtles and tortoises.||
|samplingProtocol|SIGHTING|An observation method made by direct sighting of fauna in its habitat.||
|samplingProtocol|SPOTLIGHTING|Spotlighting technique is a method used for fauna observations during the night and assists surveyors target nocturnal animals, using off-road vehicles and high-powered lights, spotlights, lamps or flashlights.||
|samplingProtocol|SWEEP NET|Sweep nets are usually used for capturing insects using a number of sweeps. The net is made of fine diameter mesh fitted to a metal handle to trap invertebrates in air., The equipment/method used during a passive, 'targeted fauna survey'. Sweep nets are usually used for capturing insects using a number of sweeps. The net is made of fine diameter mesh fitted to a metal handle to trap invertebrates in air.||
|samplingProtocol|TRACKING PAD|A tracking pad is an artificial pad made of loose material (such as sand for example) that are used to study and observe animal tracks. These pads are often designed to be delpoyed in habitats where animal activity/movements are high., Refers to the type of substrate used for fauna signs-based observation. A tracking pad is an artificial pad made of loose material (such as sand for example) that are used to study animal tracks in a fauna survey.||
|samplingProtocol|ULTRASONIC RECORDING DEVICE|Ultrasound recorders are devices that send high-frequency sound waves in the environment to create images or detect objects and movements within various mediums, such as a mammalian body or other environments. They are popular for wildlife monitoring, biodiversity surveys, habitat assessments and echolocation studies (e.g., bats).||
|samplingProtocol|UNKNOWN|Refers to the fire history of the plot, unknown., Unknown (unable to be determined)., Unknown capture status., Unknown position., Unknown- unable to be determined., Unknown/unable to be determined.||
|samplingProtocol|UNKNOWN TRAP TYPE|Refers to the fire history of the plot, unknown., Unknown (unable to be determined)., Unknown capture status., Unknown position., Unknown, unable to be determined., Unknown/unable to be determined.||
|samplingProtocol|WALLOW|A wallow is a depression containing mud or shallow water, formed by wallowing of large mammals., Wallow is a depression containing mud or shallow water, formed by the wallowing of large mammals such as a buffallo for example.||
|samplingProtocol|WATER SAMPLE|Water samples are representative samples of a given habitat that serve as a source to study the chemical composition and detect the presence of fauna species (DNA).||
|samplingProtocol|WET PITFALL TRAP|Refers to the fauna observation method, i.e., any observations made from fauna captures using a wet pitfall trap.||
|<a name="sequencingMethod-vocabularies"></a>sequencingMethod|TBC|TBC||
|<a name="sex-vocabularies"></a>sex|FEMALE|Female (♀) is the sex of an organism, or a part of an organism, which produces mobile ova (egg cells).|F, ♀|
|sex|HERMAPHRODITE|One organism having both male and female sexual characteristics and organs; at birth an unambiguous assignment of male or female cannot be made|ZWITTER|
|sex|MALE|Male (♂) refers to the sex of an organism, or part of an organism, which produces small mobile gametes, called spermatozoa.|M, ♂|
|sex|UNDETERMINED|If the sex of an organism can't be determined for some reason.|UNDET., UNKNOWN|
|<a name="taxonRank-vocabularies"></a>taxonRank|CLASS|Class||
|taxonRank|CULTIVAR|The epithet is usually output in single quotes and may contain multiple words, see ICBN §28. Examples: Taxus baccata 'Variegata', Juniperus ×pfitzeriana 'Wilhelm Pfitzer'; Magnolia 'Elizabeth' (= a hybrid, no species epithet).||
|taxonRank|CULTIVAR GROUP|Cultivar group|GREX|
|taxonRank|FAMILY|Family||
|taxonRank|FORM|Form|FORMA|
|taxonRank|GENUS|Genus||
|taxonRank|INFORMAL|Informal||
|taxonRank|INFRAGENERIC NAME|Used for any other unspecific rank below genera and above species.||
|taxonRank|INFRAORDER|Infraorder||
|taxonRank|INFRASPECIFIC NAME|Used for any other unspecific rank below genera and above species.||
|taxonRank|INFRASUBSPECIFIC NAME|Used for any other unspecific rank below subspecies.||
|taxonRank|KINGDOM|Kingdom|REGNUM|
|taxonRank|ORDER|Order|ALLIANCE|
|taxonRank|PHYLUM|Phylum|DIVISION|
|taxonRank|SECTION|Section within a genus. In Zoology a section sometimes refers to a group above family level, this is NOT meant||
|taxonRank|SERIES|Series within a genus.||
|taxonRank|SPECIES|Species||
|taxonRank|SPECIES AGGREGATE|A loosely defined group of species. Zoology: 'Aggregate - a group of species, other than a subgenus, within a genus. An aggregate may be denoted by a group name interpolated in parentheses.' -- The Berlin/MoreTax model notes:'[these] aren't taxonomic ranks but circumscriptions because on the one hand they are necessary for the concatenation of the fullname and on the other hand they are necessary for distinguishing the aggregate or species group from the microspecies.' Compare subspecific aggregate for a group of subspecies within a species.|AGGREGATE, SPECIES GROUP, SPECIES COMPLEX|
|taxonRank|SUBFAMILY|Subfamily||
|taxonRank|SUBFORM|Subform|SUBFORMA|
|taxonRank|SUBGENUS|Subgenus||
|taxonRank|SUBKINGDOM|Subkingdom||
|taxonRank|SUBORDER|Suborder||
|taxonRank|SUBSECTION|Subsection within a genus.||
|taxonRank|SUBSERIES|Subseries within a genus.||
|taxonRank|SUBSPECIES|Subspecies||
|taxonRank|SUBSPECIFIC AGGREGATE|A loosely defined group of subspecies. Zoology:'Aggregate - a group of subspecies within a species. An aggregate may be denoted by a group name interpolated in parentheses.'||
|taxonRank|SUBTRIBE|Subtribe||
|taxonRank|SUBVARIETY|Subvariety|SUBVARIETAS|
|taxonRank|SUPERFAMILY|Superfamily||
|taxonRank|SUPRAGENERIC NAME|Used for any other unspecific rank above genera.||
|taxonRank|TRIBE|Tribe||
|taxonRank|UNRANKED|Unranked||
|taxonRank|VARIETY|Variety|VARIETAS|
|<a name="threatStatusCheckProtocol-vocabularies"></a>threatStatusCheckProtocol|UNSPECIFIED|Unspecified||


<a name="threatStatus-vocabularies"></a><a name="conservationJurisdiction-vocabularies"></a>
<ins>Table 2b: Suggested values for conditionally mandatory values for the `threatStatus` and
`conservationJurisdiction` fields in the template. State and Territory `conservationJurisdictions` 
spelt out as words are also valid. For some `threatStatus` terms, alternative labels are provided
that are also valid for that `conservationJurisdiction`.

|conservationJurisdiction|threatStatus|threatStatus alternative labels|
|:---:|:---|:---|
|ACT|CRITICALLY ENDANGERED||
|ACT|ENDANGERED||
|ACT|EXTINCT||
|ACT|EXTINCT IN THE WILD||
|ACT|REGIONALLY CONSERVATION DEPENDENT||
|ACT|VULNERABLE||
|EPBC|CAMBA||
|EPBC|CD|CONSERVATION DEPENDENT|
|EPBC|CE|CRITICALLY ENDANGERED, CR|
|EPBC|CITES||
|EPBC|E|ENDANGERED, EN|
|EPBC|EX|EXTINCT|
|EPBC|JAMBA||
|EPBC|KAMBA||
|EPBC|V|VULNERABLE, VU|
|EPBC|XW|EXTINCT IN THE WILD, EW|
|NSW|CE|CRITICALLY ENDANGERED|
|NSW|EN|ENDANGERED|
|NSW|EX|EXTINCT|
|NSW|V|VULNERABLE|
|NT|CE|CRITICALLY ENDANGERED|
|NT|DD|DATA DEFICIENT|
|NT|EN|ENDANGERED|
|NT|EN EXTINCT IN NT|ENDANGERED EXTINCT IN NT|
|NT|EN EXTINCT IN WILD IN NT|ENDANGERED EXTINCT IN WILD IN NT|
|NT|EW|CRITICALLY ENDANGERED POSSIBLY EXTINCT|
|NT|EX|EXTINCT|
|NT|LC|LEAST CONCERN|
|NT|LC EXTINCT IN NT|LEAST CONCERN EXTINCT IN NT|
|NT|NE|NOT EVALUATED|
|NT|NT|NEAR THREATENED|
|NT|VU|VULNERABLE|
|NT|VU EXTINCT IN NT|VULNERABLE EXTINCT IN NT|
|QLD|C|LEAST CONCERN WILDLIFE|
|QLD|CR|CRITICALLY ENDANGERED WILDLIFE|
|QLD|E|ENDANGERED WILDLIFE|
|QLD|EX|EXTINCT WILDLIFE|
|QLD|I|INTERNATIONAL WILDLIFE|
|QLD|NT|NEAR THREATENED WILDLIFE|
|QLD|PE|EXTINCT IN THE WILD WILDLIFE|
|QLD|SL|SPECIAL LEAST CONCERN WILDLIFE|
|QLD|V|VULNERABLE WILDLIFE|
|SA|E|ENDANGERED|
|SA|R|RARE|
|SA|SP|INDICATES THAT A RATING HAS BEEN APPLIED TO THE SPECIES LEVEL THE STATUS HAS NOT BEEN ASSESSED AT THE SUBSPECIES LEVEL|
|SA|SSP|INDICATES THAT AT LEAST ONE SUBSPECIES FOR THIS SPECIES HAS BEEN GIVEN A CONSERVATION RATING|
|SA|V|VULNERABLE|
|TAS|E|ENDANGERED|
|TAS|R|RARE|
|TAS|V|VULNERABLE|
|TAS|X|EXTINCT|
|VIC|CONSERVATION DEPENDENT||
|VIC|CRITICALLY ENDANGERED||
|VIC|ENDANGERED||
|VIC|ENDANGERED EXTINCT IN VICTORIA||
|VIC|EXTINCT||
|VIC|EXTINCT IN THE WILD||
|VIC|RESTRICTED||
|VIC|VULNERABLE||
|WA|CD|SPECIES OF SPECIAL CONSERVATION INTEREST CONSERVATION DEPENDENT FAUNA, CONSERVATION DEPENDENT|
|WA|CR|CRITICALLY ENDANGERED, CRITICALLY ENDANGERED SPECIES|
|WA|EN|ENDANGERED SPECIES, ENDANGERED|
|WA|EW|EXTINCT IN THE WILD|
|WA|EX|EXTINCT SPECIES, EXTINCT|
|WA|MI|MIGRATORY SPECIES, MIGRATORY|
|WA|OS|OTHER SPECIFICALLY PROTECTED FAUNA|
|WA|P1|PRIORITY 1 POORLY KNOWN, PRIORITY 1 POORLY KNOWN SPECIES|
|WA|P2|PRIORITY 2 POORLY KNOWN SPECIES, PRIORITY 2 POORLY KNOWN|
|WA|P3|PRIORITY 3 POORLY KNOWN, PRIORITY 3 POORLY KNOWN SPECIES|
|WA|P4|PRIORITY 4 RARE NEAR THREATENED AND OTHER SPECIES IN NEED OF MONITORING|
|WA|SPECIALLY PROTECTED|SPECIALLY PROTECTED SPECIES|
|WA|T|THREATENED, THREATENED SPECIES|
|WA|VU|VULNERABLE SPECIES, VULNERABLE|


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

For assistance, please contact: <bdr-support@dcceew.gov.au>

