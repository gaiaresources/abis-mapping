---
title: Systematic Survey Site Data Template - v1.0.0
 - Archived

summary: A template for systematic survey site data
---
<small>
**survey_site_data** v1.0.0
</small>


!!! failure "Template Archived"

    This Template is archived, and is no longer available for use.


# SYSTEMATIC SURVEY SITE DATA TEMPLATE INSTRUCTIONS

## Intended Usage
This Systematic Survey Site Data template should be used to record data about a 
Site area where species occurrences have been sampled during a systematic survey.

This Systematic Survey Site template **must be used in combination** with the
`Systematic Survey Occurrence` template and the `Systematic Survey Metadata` template.

Templates have been provided to facilitate integration of data into the Biodiversity Data
Repository (BDR) database. Not all types of data have been catered for in the available
templates at this stage - if you are unable to find a suitable template, please
contact <bdr-support@dcceew.gov.au> to make us aware of your data needs.

#### Data Validation Requirements:
For data validation, you will need your data file to:

- be the correct **file format**,
- have **fields that match the template downloaded** (do not remove, or 
  change the order of fields),
- have extant values for **mandatory fields** (see Table 1), and
- comply with all **data value constraints**; for example the geographic coordinates are
  consistent with a [geodeticDatum](#geodeticDatum-vocabularies) type of the 
  ***5*** available options.

Additional fields may be added **after the templated fields** (noting that the data type 
is not assumed and values will be encoded as strings).

### FILE FORMAT
- The systematic survey site data template is a [UTF-8](#appendix-iv-utf-8) encoded csv (not Microsoft
  Excel Spreadsheets). Be sure to save this file with your data as a .csv (UTF-8) as follows,
  otherwise it will not pass the csv validation step upon upload.
  <br>`[MS Excel: Save As > More options > Tools > Web options > Save this document as >
  Unicode (UTF-8)]`<br>
  otherwise it will not pass the csv validation step upon upload.
- **Do not include empty rows**.

#### FILE SIZE
MS Excel imposes a limit of 1,048,576 rows on a spreadsheet, limiting a CSV file to the
header row followed by 1,048,575 occurrences. Furthermore, MS Excel has a 32,767 character
limit on individual cells in a spreadsheet. These limits may be overcome by using or
editing CSV files with other software.

Larger datasets may be more readily ingested using the API interface. Please contact
<bdr-support@dcceew.gov.au> to make us aware of your data needs.

## TEMPLATE FIELDS
The template contains the field names in the top row. Table 1 will assist you in transferring
your data to the template indicating:

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
Data that does not match the existing template fields may be added as additional columns in
the CSV files after the templated fields.
For example, `fieldNotes`, `continent`, `country`, `countryCode`, `stateProvince`, `georeferencedDate`,
`landformPattern`, `landformElement`, `aspect`, `slope`, `visitNo`.

<ins>Table 1: Systematic Survey Site data template fields with descriptions, conditions, datatype format, and examples.</ins>

|Field #|Name|Description|Mandatory / Optional|Datatype Format|Examples|
|:---:|:---|:---|:---:|:---:|:---|
|1|<a name="siteID-field"></a>siteID|A unique within dataset string identifier for the site. Valid values include strings that are used specifically for this survey or URIs from BDR Sites that have been established in previous surveys.|**<font color="Crimson">Mandatory</font>**|String|P1|
|2|<a name="siteIDSource-field"></a>siteIDSource|The organisation that assigned the SiteID to this Site|Optional|String|TERN|
|3|<a name="siteType-field"></a>siteType|The type of site that relates to its sampling type and/or dimensions.|Optional|String|Plot<br>([Vocabulary link](#siteType-vocabularies))|
|4|<a name="siteName-field"></a>siteName|A name for the site that may be more descriptive than the siteID.|Optional|String|Plot 1|
|5|<a name="siteDescription-field"></a>siteDescription|The site (plot) description covers important aspects of the site (generally of the land surface). Some overlap in collected information does occur due to the modular nature of the survey processes. The description provides significant background information to gain an appreciation of the plot history, topography, position in the landscape and for understanding the likely relationship between the soils, vegetation and fauna.|Optional|String|Fine woody debris.|
|6|<a name="habitat-field"></a>[habitat](https://dwc.tdwg.org/terms/#dwc:habitat)|A collection of habitat types representing the dominant vegetation structural formation class adopted by the National Vegetation Information System (NVIS).|Optional|List|Chenopod Shrubland \| Closed Fernland<br>([Vocabulary link](#habitat-vocabularies))|
|7|<a name="relatedSiteID-field"></a>relatedSiteID|Identifier of a related site to the specified site e.g. parent site, same site with different identifier.|**<font color="DarkGoldenRod">Conditionally mandatory with relationshipToRelatedSite</font>**|String|Same as within dataset or existing URI|
|8|<a name="relationshipToRelatedSite-field"></a>relationshipToRelatedSite|Relationship between the site and the related site. This field can be used to record Site identifiers for the same site from different custodians through the use of URIs.|**<font color="DarkGoldenRod">Conditionally mandatory with relatedSiteID</font>**|String|Same as within dataset or existing URI<br>([Vocabulary link](#relationshipToRelatedSite-vocabularies))|
|9|<a name="decimalLatitude-field"></a>[decimalLatitude](https://dwc.tdwg.org/terms/#dwc:decimalLatitude)|The geographic latitude (in decimal degrees, using the spatial reference system given in geodeticDatum) of the geographic origin of a Site. Positive values are north of the Equator, negative values are south of it. Legal values lie between -90 and 0, inclusive for Southern hemisphere.|Optional|Number|-34.036|
|10|<a name="decimalLongitude-field"></a>[decimalLongitude](https://dwc.tdwg.org/terms/#dwc:decimalLongitude)|The geographic longitude (in decimal degrees, using the spatial reference system given in geodeticDatum) of the geographic origin of a Site. Positive values are east of the Greenwich Meridian, negative values are west of it. Legal values lie between 0 and 180, inclusive for the BDR use case.|Optional|Number|146.363|
|11|<a name="footprintWKT-field"></a>[footprintWKT](https://dwc.tdwg.org/terms/#dwc:footprintWKT)|A Well-Known Text (WKT) representation of the shape (footprint, geometry) that defines the Site. A Site may have both a point-radius representation and a footprint representation, and they may differ from each other.|Optional|WKT|LINESTRING (146.363 -34.036, 146.363 -34.037)<br>([WKT notes](#appendix-ii-well-known-text-wkt))|
|12|<a name="geodeticDatum-field"></a>[geodeticDatum](https://dwc.tdwg.org/terms/#dwc:geodeticDatum)|The geodetic datum, or spatial reference system (SRS) upon which the geographic coordinates given for the Site are based.|Optional|String|WGS84<br>([Vocabulary link](#geodeticDatum-vocabularies))|
|13|<a name="coordinateUncertaintyInMeters-field"></a>[coordinateUncertaintyInMeters](https://dwc.tdwg.org/terms/#dwc:coordinateUncertaintyInMeters)|The horizontal distance (in metres) from the given decimalLatitude and decimalLongitude describing the smallest circle containing the whole of the Site. Leave the value empty if the uncertainty is unknown, cannot be estimated, or is not applicable (because there are no coordinates). Zero is not a valid value for this term.|Optional|Integer|50|
|14|<a name="dataGeneralizations-field"></a>dataGeneralizations|Actions taken to make the shared data less specific or complete than in its original form.|Optional|String|Coordinates given in decimalLatitude, decimalLongitude, easting and northing have been rounded to 0.1 DEG. The observer name has been changed to a unique User ID.|
|15|<a name="surveyID-field"></a>surveyID|The identifier of the Survey that the Site is related to in this dataset.|Optional|String|AR220-01|
|16|<a name="siteVisitID-field"></a>siteVisitID|The unique key assigned to a visit. A visit is a time distinct assessment conducted within a survey at a designated site.|Optional|String|CPXEI0000001|
|17|<a name="siteVisitStart-field"></a>siteVisitStart|The temporal start of when the Site was being used to collect data for the survey. Expected values include date, dateTime, dateTimeStamp.|**<font color="Crimson">Mandatory</font>**|Timestamp|2016-02-28|
|18|<a name="siteVisitEnd-field"></a>siteVisitEnd|The temporal end of when the Site was being used to collect data for the survey. Expected values include date, dateTime, dateTimeStamp.|Optional|Timestamp|2016-02-28|
|19|<a name="visitOrgs-field"></a>visitOrgs|The names of the organisations responsible for recording the original Occurrence.|Optional|List|NSW Dept of Planning, Industry and Environment.|
|20|<a name="visitObservers-field"></a>visitObservers|A list (concatenated and separated using \|) of names of people, groups, or organisations responsible for recording the original Occurrence.|Optional|List|Oliver P. Pearson \| Anita K. Pearson|
|21|<a name="condition-field"></a>condition|The state of a patch of vegetation at the time of sampling relative to some specified standard or benchmark (where available).|Optional|String|Burnt|


## APPENDICES
### APPENDIX-I: VOCABULARY LIST
With the exception of `geodeticDatum` and `relationshipToRelatedSite`, data validation
does not require adherence to the vocabularies for the various vocabularied fields.
These vocabularies are merely provided as a means of assistance in developing consistent language
within the database. New terms may be added to more appropriately describe your data that goes 
beyond the current list.

<ins>Table 2: Suggested values for controlled vocabulary fields in the template. Each term has a preferred label with a definition to aid understanding
of its meaning. For some terms, alternative
labels with similar semantics are provided. </ins>
<br>**Note:** <font color="red">The values for `geodeticDatum` and `relationshipToRelatedSite` must come from one of the Preferred labels or Alternate Labels in this
table.</font>

|Template field name|Preferred label|Definition|Alternate label|
|:---|:---|:---|:---|
|<a name="geodeticDatum-vocabularies"></a>geodeticDatum|AGD66|Australian Geodetic Datum 1966|EPSG:4202|
|geodeticDatum|AGD84|Australian Geodetic Datum 1984|EPSG:4203|
|geodeticDatum|GDA2020|Geocentric Datum of Australia 2020|EPSG:7844|
|geodeticDatum|GDA94|Geocentric Datum of Australia 1994|EPSG:4283|
|geodeticDatum|WGS84|World Geodetic System 1984, used in GPS|EPSG:4326|
|<a name="habitat-vocabularies"></a>habitat|BEACH|Type of Landform Element, which is usually short; low; very wide slope; gently or moderately inclined; built up or eroded by waves; forming the shore of a lake or sea.||
|habitat|BILLABONG OR SWAMP|A swamp is a wetland that features temporary or permanent inundation of large areas of land by shallow bodies of water, generally with a substantial number of hammocks, or dry-land protrusions, and covered by aquatic vegetation, or vegetation that tolerates periodical inundation.||
|habitat|CAVE|The type of habitat representative of a naturally formed, subterranean open area or chamber.||
|habitat|CHENOPOD SHRUBLAND|Refers to the NVIS dominant vegetation structural formation class, with a percent cover of about 50-80% members of Chenopodiaceae.||
|habitat|CLOSED CHENOPOD SHRUBLAND|Refers to the NVIS dominant vegetation structural formation class, with a percent cover of about >80% members of Chenopodiaceae.||
|habitat|CLOSED FERNLAND|Refers to the NVIS dominant vegetation structural formation class, with a percent cover of about >80% members of Fern and Fern-allies.||
|habitat|CLOSED FORBLAND|Refers to the NVIS dominant vegetation structural formation class, with a percent cover of about >80% members of Forbs or herbs other than grasses.||
|habitat|CLOSED FOREST|Refers to the NVIS dominant vegetation structural formation class, with a percent cover of about >80% members of Forbs or herbs other than grasses.||
|habitat|CLOSED HEATHLAND|Refers to the NVIS dominant vegetation structural formation class, with a percent cover of about >80% members of heath shrubs (e.g., members of Ericaceae, Myrtaceae).||
|habitat|CLOSED HUMMOCK GRASSLAND|Refers to the NVIS dominant vegetation structural formation class, with a percent cover of about >80% members of hummock (e.g., Triodia) grasses.||
|habitat|CLOSED LICHENLAND|Refers to the type of habitat characterised by lichenised tree trunks and rocks.||
|habitat|CLOSED LIVERWORTLAND|Refers to the type of habitat characterised by lower plant groups such as moss, liverworts and bryophytes.||
|habitat|CLOSED MALLEE FOREST|Refers to the NVIS dominant vegetation structural formation class, with a percent cover of about >80% members of tree mallee (e.g., some members of Eucalyptus).||
|habitat|CLOSED MALLEE SHRUBLAND|Refers to the NVIS dominant vegetation structural formation class, with a percent cover of about >80% members of mallee shrubs (e.g., some members of Eucalyptus).||
|habitat|CLOSED MOSSLAND|Refers to the type of habitat characterised by lower plant groups such as moss, liverworts and bryophytes.||
|habitat|CLOSED RUSHLAND|Refers to the NVIS dominant vegetation structural formation class, with a percent cover of about >80% members of Rushes (e.g., Juncaceae).||
|habitat|CLOSED SEDGELAND|Refers to the NVIS dominant vegetation structural formation class, with a percent cover of about >80% members of sedges (e.g., Cyperaceae).||
|habitat|CLOSED SHRUBLAND|Refers to the NVIS dominant vegetation structural formation class, with a percent cover of about >80% members of sedges (e.g., Cyperaceae).||
|habitat|CLOSED SOD GRASSLAND|Refers to the type of habitat representative of a characteristic sod-like (turf) grass.||
|habitat|CLOSED TUSSOCK GRASSLAND|Refers to the NVIS dominant vegetation structural formation class, with a percent cover of about >80% members of tussock grasses (e.g., Poa).||
|habitat|CLOSED VINELAND|Refers to the type of habitat represented by a closed vegetation dominated by stragglers and woody climbers.||
|habitat|COASTAL WATERS|Refers to the type of habitat representative of an aquatic body typically characterized by a shallow continental shelf, gently sloping seaward to a continental slope, which drops relatively abruptly to the deep ocean.||
|habitat|CROP LAND|Refers to the type of habitat representative of a cultivated land or land on which agricultural crops are grown or land that is set aside or temporarily not being used for crop production.||
|habitat|ESTUARY|Type of Landform Element which has a stream channel close to its junction with a sea or lake; where the action of channelled stream flow is modified by tide and waves. The width typically increases downstream.||
|habitat|FERNLAND|Refers to the NVIS dominant vegetation structural formation class, with a percent cover of about 50-80% members of Fern and Fern-allies.||
|habitat|FORBLAND|Refers to the NVIS dominant vegetation structural formation class, with a percent cover of about 50-80% members of Forbs or herbaceous plants other than grasses.||
|habitat|FRESHWATER LAKE|Refers to the type of habitat representative of an enclosed aquatic body having a relatively low mineral content, generally less than 500 mg/l of dissolved solids.||
|habitat|GRAZING LAND|Refers to the type of habitat representative of a land predominantly used for grazing.||
|habitat|HEATHLAND|Refers to the NVIS dominant vegetation structural formation class, with a percent cover of about 50-80% members of Heath (e.g., Ericaceae, Myrtaceae).||
|habitat|HUMMOCK GRASSLAND|Refers to the NVIS dominant vegetation structural formation class, with a percent cover of about 50-80% members of hummock grasses (e.g., Triodia).||
|habitat|ISOLATED CHENOPOD SHRUBS|Refers to the NVIS dominant vegetation structural formation class, with a percent cover of about <0.25% members of Chenopodiaceae.||
|habitat|ISOLATED CLUMP OF CHENOPOD SHRUBS|Refers to the type of habitat characterised by isolated clumps of chenopod shrubs.||
|habitat|ISOLATED CLUMP OF HEATH SHRUBS|Refers to the type of habitat characterised by isolated clumps of heath or heath-like shrubs.||
|habitat|ISOLATED CLUMP OF HUMMOCK GRASSES|Refers to the type of habitat characterised by isolated clumps of hummocky grass (e.g., Triodia spp., Spinifex spp.).||
|habitat|ISOLATED CLUMP OF LIVERWORTS|Refers to the type of habitat characterised by isolated clumps of bryophytes, moss and liverworts.||
|habitat|ISOLATED CLUMP OF MALLEE SHRUBS|Refers to the type of habitat characterised by isolated clumps of mallee shrubs (members of Eucalyptus spp., multistemmed from base).||
|habitat|ISOLATED CLUMP OF MALLEE TREES|Refers to the type of habitat characterised by isolated clumps of tree mallee (members of Eucalyptus spp., multistemmed from base).||
|habitat|ISOLATED CLUMP OF MOSSES|Refers to the type of habitat characterised by isolated clumps of bryophytes, moss and liverworts.||
|habitat|ISOLATED CLUMP OF RUSHES|Refers to the type of habitat characterised by isolated clumps of rushes.||
|habitat|ISOLATED CLUMP OF SEDGES|Refers to the type of habitat characterised by isolated clumps of sedges.||
|habitat|ISOLATED CLUMP OF SHRUBS|Refers to the type of habitat characterised by isolated clumps of shrubs.||
|habitat|ISOLATED CLUMP OF SOD GRASSES|Refers to the type of habitat characterised by isolated clumps of sod grass.||
|habitat|ISOLATED CLUMP OF TREES|Refers to the type of habitat characterised by isolated clumps of trees.||
|habitat|ISOLATED CLUMP OF TUSSOCK GRASSES|Refers to the type of habitat characterised by isolated clumps of tussock grasses (e.g., Poa spp).||
|habitat|ISOLATED CLUMP OF VINES|Refers to the type of habitat characterised by isolated clumps of vines.||
|habitat|ISOLATED CLUMPS OF FERNS|Refers to the NVIS dominant vegetation structural formation class, with a percent cover of about 0-5% members of Fern and Fern-allies.||
|habitat|ISOLATED CLUMPS OF FORBS|Refers to the NVIS dominant vegetation structural formation class, with a percent cover of about 0-5% members of Forbs or herbs other than grasses.||
|habitat|ISOLATED CLUP OF LICHENS|Refers to the type of habitat characterised by isolated clumps of lichens.||
|habitat|ISOLATED FERNS|Refers to the NVIS dominant vegetation structural formation class, with a percent cover of about <0.25% of fern and fern allies.||
|habitat|ISOLATED FORBS|Refers to the NVIS dominant vegetation structural formation class, with a percent cover of about <0.25% of forbs or herbs other than grasses.||
|habitat|ISOLATED HEATH SHRUBS|Refers to the NVIS dominant vegetation structural formation class, with a percent cover of about <0.25% of heath shrubs (e.g., Ericaceae, Myrtaceae).||
|habitat|ISOLATED HUMMOCK GRASSES|Refers to the NVIS dominant vegetation structural formation class, with a percent cover of about <0.25% of hummock grasses (e.g., Triodia).||
|habitat|ISOLATED LICHENS|Refers to the type of habitat characterised by isolated or sparse lichens.||
|habitat|ISOLATED LIVERWORTS|Refers to the type of habitat characterised by isolated or sparse liverworts.||
|habitat|ISOLATED MALLEE SHRUBS|Refers to the NVIS dominant vegetation structural formation class, with a percent cover of about <0.25% of mallee shrubs (e.g., some multistemmed individuals from base of Eucalyptus).||
|habitat|ISOLATED MALLEE TREES|Refers to the NVIS dominant vegetation structural formation class, with a percent cover of about <0.25% of tree mallee (e.g., some multistemmed individuals from base of Eucalyptus).||
|habitat|ISOLATED MOSSES|Refers to the type of habitat characterised by isolated mosses, including bryophytes and liverworts.||
|habitat|ISOLATED RUSHES|Refers to the NVIS dominant vegetation structural formation class, with a percent cover of about <0.25% of rushes (e.g., Juncaceae).||
|habitat|ISOLATED SEDGES|Refers to the NVIS dominant vegetation structural formation class, with a percent cover of about <0.25% of sedges (e.g., Cyperaceae).||
|habitat|ISOLATED SHRUBS|Refers to the NVIS dominant vegetation structural formation class, with a percent cover of about <0.25% of shrubs including cycads, grass-tree and tree-fern.||
|habitat|ISOLATED SOD GRASSES|Refers to the type of habitat characterised by isolated or sparse sod or turf-like grasses.||
|habitat|ISOLATED TREES|Refers to the NVIS dominant vegetation structural formation class, with a percent cover of about <0.25% of trees including palms.||
|habitat|ISOLATED TUSSOCK GRASSES|Refers to the NVIS dominant vegetation structural formation class, with a percent cover of about <0.25% of tussock grass (e.g. Poa species).||
|habitat|ISOLATED VINES|Refers to the type of habitat characterised by isolated or sparse stragglers or climbing woody vines.||
|habitat|LICHENLAND|Refers to the type of habitat predominated by lichens on rocks, trees or tree stumps, etc.||
|habitat|LIVERWORTLAND|Refers to the type of habitat predominated by liverworts.||
|habitat|MALLEE SHRUBLAND|Refers to the NVIS dominant vegetation structural formation class, with a percent cover of about 50-80% of shrub mallee (e.g., individuals of some Eucalypts multistemmed from base).||
|habitat|MALLEE WOODLAND|Refers to the dominant vegetation structural formation, with a percent cover of about 20-50% of Tree Mallee.||
|habitat|MOSSLAND|Refers to the type of habitat dominated by mosses.||
|habitat|MUDFLAT|Refers to the type of habitat characterised by a wetland that forms when mud is deposited by the tides, rivers, sea or oceans.||
|habitat|OPEN CHENOPOD SHRUBLAND|Refers to the NVIS dominant vegetation structural formation class, with a percent cover of about 20-50% of members of Chenopodiaceae.||
|habitat|OPEN FERNLAND|Refers to the NVIS dominant vegetation structural formation class, with a percent cover of about 20-50% of ferns and fern allies.||
|habitat|OPEN FORBLAND|Refers to the NVIS dominant vegetation structural formation class, with a percent cover of about 20-50% of forbs or herbs other than grasses.||
|habitat|OPEN FOREST|Refers to the NVIS dominant vegetation structural formation class, with a percent cover of about 20-50% of trees including palms.||
|habitat|OPEN HEATH|Refers to the NVIS dominant vegetation structural formation class, with a percent cover of about 20-50% of heaths (e.g., Ericaceae, Myrtaceae).||
|habitat|OPEN HUMMOCK GRASSLAND|Refers to the NVIS dominant vegetation structural formation class, with a percent cover of about 20-50% of hummock grasses (e.g., Triodia).||
|habitat|OPEN LICHENLAND|Refers to the type of habitat represented by open or sparse (i.e., 10-30%) hummocky grasses (e.g., Spinifex spp., Triodia spp.).||
|habitat|OPEN LIVERWORTLAND|Refers to the type of habitat characterised by open or sparse lichenised tree trunks and rocks.||
|habitat|OPEN MALLEE FOREST|Refers to the NVIS dominant vegetation structural formation class, with a percent cover of about 50-80% of tree Mallee (e.g., certain individuals of Eucalypts multistemmed from base).||
|habitat|OPEN MALLEE SHRUBLAND|Refers to the NVIS dominant vegetation structural formation class, with a percent cover of about 20-50% of Mallee shrubs (e.g., certain individuals of Eucalypts multistemmed from base).||
|habitat|OPEN MALLEE WOODLAND|Refers to the NVIS dominant vegetation structural formation class, with a percent cover of about 0.25-20% of tree mallee (e.g., certain individuals of Eucalypts multistemmed from base).||
|habitat|OPEN MOSSLAND|Refers to the type of habitat characterised by open or sparse members of lower plant groups such as moss, liverworts and bryophytes.||
|habitat|OPEN OCEAN|Refers to the type of habitat surrounded by ocean, i.e., a continuous saline-water bodies that surround the continents and fill the Earth's great depressions.||
|habitat|OPEN RUSHLAND|Refers to the NVIS dominant vegetation structural formation class, with a percent cover of about 20-50% of rushes (e.g. Juncaceae).||
|habitat|OPEN SEDGELAND|Refers to the NVIS dominant vegetation structural formation class, with a percent cover of about 20-50% of sedges (e.g. Cyperaceae).||
|habitat|OPEN SHRUBLAND|Refers to the NVIS dominant vegetation structural formation class, with a percent cover of about 20-50% of shrubs (e.g. shrubs, cycads, grass-tree, tree-fern).||
|habitat|OPEN SOD GRASSLAND|Refers to the type of habitat characterised by open or sparse (10-30% ground cover) of a characteristic sod-like (turf) grass.||
|habitat|OPEN TUSSOCK GRASSLAND|Refers to the NVIS dominant vegetation structural formation class, with a percent cover of about 20-50% of tussock grasses (e.g. Poa species).||
|habitat|OPEN VINELAND|Refers to the type of habitat represented by a closed vegetation dominated by stragglers and woody climbers.||
|habitat|OPEN WOODLAND|Refers to the NVIS dominant vegetation structural formation class, with a percent cover of about 0.25-20% of trees including palms.||
|habitat|ROCK OUTCROP|Refers to the type of habitat characterised by rocks, which protrudes through the surface layer.||
|habitat|RUSHLAND|Refers to the NVIS dominant vegetation structural formation class, with a percent cover of about 50-80% of rushes (e.g. Juncaceae).||
|habitat|SALTWATER LAKE|Refers to the type of habitat representative of an aquatic body filled with water (with high salinity) of considerable size contained in a depression on a landmass.||
|habitat|SEDGELAND|Refers to the NVIS dominant vegetation structural formation class, with a percent cover of about 50-80% of sedges (e.g., Cyperaceae).||
|habitat|SHRUBLAND|Refers to the NVIS dominant vegetation structural formation class, with a percent cover of about 50-80% of shrubs (e.g., shrub, cycad, grass-tree, tree-fern).||
|habitat|SOD GRASSLAND|Refers to the type of habitat characterised by mid-dense (30-70% cover) sod or turf-like grasses.||
|habitat|SPARSE CHENOPOD SHRUBLAND|Refers to the NVIS dominant vegetation structural formation class, with a percent cover of about 0.25-20% of members of Chenopodiaceae.||
|habitat|SPARSE FERNLAND|Refers to the NVIS dominant vegetation structural formation class, with a percent cover of about 0.25-20% of members of fern and fern-allies.||
|habitat|SPARSE FORBLAND|Refers to the NVIS dominant vegetation structural formation class, with a percent cover of about 0.25-20% of members of forbs and herbs other than grasses.||
|habitat|SPARSE GRASSLAND|Refers to the NVIS dominant vegetation structural formation class, with a percent cover of about 0.25-20% of grasses.||
|habitat|SPARSE HEATH|Refers to the NVIS dominant vegetation structural formation class, with a percent cover of about 0.25-20% of members of heath (e.g., Ericaceae, Myrtaceae).||
|habitat|SPARSE LICHENLAND|Refers to the type of habitat characterised by very sparse (<10% cover) lichens.||
|habitat|SPARSE LIVERWORTLAND|Refers to the type of habitat characterised by very sparse (<10% cover) liverworts.||
|habitat|SPARSE MALLEE SHRUBLAND|Refers to the NVIS dominant vegetation structural formation class, with a percent cover of about 0.25-20% of members of shrub Mallee.||
|habitat|SPARSE MOSSLAND|Refers to the type of habitat characterised by very sparse (<10% cover) mosses.||
|habitat|SPARSE RUSHLAND|Refers to the NVIS dominant vegetation structural formation class, with a percent cover of about 0.25-20% of rushes (e.g., Juncaceae).||
|habitat|SPARSE SEDGELAND|Refers to the NVIS dominant vegetation structural formation class, with a percent cover of about 0.25-20% of sedges (e.g., Cyperaceae).||
|habitat|SPARSE SHRUBLAND|Refers to the NVIS dominant vegetation structural formation class, with a percent cover of about 0.25-20% of shrubs, including cycad, grass-tree, tree-fern.||
|habitat|SPARSE SOD GRASSLAND|Refers to the type of habitat characterised by very sparse (<10% cover) sod or turf-like grasses.||
|habitat|SPARSE TUSSOCK GRASSLAND|Refers to the NVIS dominant vegetation structural formation class, with a percent cover of about 0.25-20% of tussock grass (e.g., Poa species).||
|habitat|SPARSE VINELAND|Refers to the type of habitat characterised by well separated or very sparse crown stragglers or woody vines.||
|habitat|STREAM OR RIVER|Refers to the type of habitat representative of an aquatic body with a watercourse which is linear and flows across the solid portion of a planetary surface.||
|habitat|TUSSOCK GRASSLAND|Refers to the NVIS dominant vegetation structural formation class, with a percent cover of about 50-80% of tussock grass (e.g., Poa species).||
|habitat|URBAN|Refers to the type of habitat relating to, located in, or characteristic of a city or densely populated area.||
|habitat|VINELAND|Refers to the type of habitat characterised by woody climbers/straggling vines.||
|habitat|WOODLAND|Refers to the type of habitat characterised by a low-density forest forming open habitats with plenty of sunlight and limited shade.||
|<a name="relationshipToRelatedSite-vocabularies"></a>relationshipToRelatedSite|PART OF|When a site is a subset of another site.||
|relationshipToRelatedSite|SAME AS|When two sites are the same.||
|<a name="siteType-vocabularies"></a>siteType|PARENT SITE|Parent site.||
|siteType|PLOT|Land area selected from within a survey region which abiotic and biotic properties are sampled.||
|siteType|QUADRAT|A transportable frame (usually a square made out of PVC tube, metal rod or wood) used to isolate a standard unit of area for study of the distribution of item(s) over a large area (e.g. a plot).||
|siteType|SITE|A place in which study/protocol/sampling activities are conducted.||
|siteType|TRANSECT|A line along which biotic and abiotic characteristics are sampled||


### APPENDIX-II: Well Known Text (WKT)
For general information on how WKT coordinate reference data is formatted is available [here](https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry).
The length of a WKT string or of its components is not prescribed; however, MS Excel *does* has a
32,767 (32K) character limit on individual cells in a spreadsheet.

It is possible to edit CSV files outside of Excel in order to include more than 32K characters.

![Multipart geometries (2D) WKT](../assets/multipart_geometries_2d_wkt.png)
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

For assistance, please contact: <bdr-support@dcceew.gov.au>

