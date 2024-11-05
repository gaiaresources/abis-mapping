# October 2024
## Templates
### Incidental Occurrence v3.0.0
#### [Schema v3.0.0](https://github.com/gaiaresources/abis-mapping/blob/main/abis_mapping/templates/incidental_occurrence_data_v3/schema.json) changes (by column order).
* The field `eventDate` is renamed `eventDateStart`.
* The field `eventDateEnd` is added. It is an optional field with type Timestamp.
* The field `conservationJurisdiction` is replaced by `conservationAuthority`.
* `sensitivityCategory` and `sensitivityAuthority` are added fields. Both are type string.
They are mutually inclusive, both must be provided or both must be blank.

For more details on the Incidental Occurrence v3.0.0 template,
see the [Incidental Occurrence v3.0.0 instruction manual](https://gaiaresources.github.io/abis-mapping/dev/incidental_occurrence_data-v3.0.0.csv/)

### Systematic Survey Metadata v2.0.0
#### [Schema v2.0.0](https://github.com/gaiaresources/abis-mapping/blob/main/abis_mapping/templates/survey_metadata_v2/schema.json) changes (by column order).
* `samplingPerformedBy` is removed.
* `samplingEffortValue` was moved to the Systematic Survey Site Visit Data Template
* `samplingEffortUnit` was moved to the Systematic Survey Site Visit Data Template

For more details on the Systematic Survey Metadata v2.0.0 template,
see the [Systematic Survey Metadata v2.0.0 instruction manual](https://gaiaresources.github.io/abis-mapping/dev/survey_metadata-v2.0.0.csv/)

### Systematic Survey Occurrence Data v2.0.0
#### [Schema v2.0.0](https://github.com/gaiaresources/abis-mapping/blob/main/abis_mapping/templates/survey_occurrence_data_v2/schema.json) changes (by column order).
* The field `eventDate` is renamed `eventDateStart`.
* The field `eventDateEnd` is added. It is an optional field with type Timestamp.
* The field `conservationJurisdiction` is replaced by `conservationAuthority`.
* `sensitivityCategory` and `sensitivityAuthority` are added fields. Both are type string.
They are mutually inclusive, both must be provided or both must be blank.
* Swapped positions of fields `surveyID` and `siteID` so that `surveyID` is first.
* Add field `siteVisitID`. Type is string, can be blank. 
If provided, should match a `siteVisitID` in the `survey_site_visit_data.csv` template.

For more details on the Systematic Survey Occurrence Data v2.0.0 template,
see the [Systematic Survey Occurrence Data v2.0.0 instruction manual](https://gaiaresources.github.io/abis-mapping/dev/survey_occurrence_data-v2.0.0.csv/)

### Systematic Survey Site Data v2.0.0
#### [Schema v2.0.0](https://github.com/gaiaresources/abis-mapping/blob/main/abis_mapping/templates/survey_site_data_v2/schema.json) changes (by column order).
* Add field `locality`. Type is string, can be blank.
* Moved fields `surveyID`, `siteVisitID`, `siteVisitStart`, `siteVisitEnd`, `visitOrgs`, `visitObservers`, `condition` 
to the Systematic Survey Site Visit Data Template.

For more details on the Systematic Survey Site Data v2.0.0 template,
see the [Systematic Survey Site Data v2.0.0 instruction manual](https://gaiaresources.github.io/abis-mapping/dev/survey_site_data-v2.0.0.csv/)

### Systematic Survey Site Visit Data v2.0.0
This is a new Template for Systematic Survey v2. When provided, the `survey_site_data.csv` template must also be provided.
#### [Schema v2.0.0](https://github.com/gaiaresources/abis-mapping/blob/main/abis_mapping/templates/survey_site_visit_data_v2/schema.json) changes (by column order).
* `surveyID` was moved to this template from the `survey_site_data.csv` template.
* `siteID` is a new field. Type is string, **mandatory**.
* `siteIDSource` is a new field. Type is string, can be blank.
* Fields `siteVisitID`, `siteVisitStart`, `siteVisitEnd`, `visitOrgs`, `visitObservers`, `condition`
were moved to this template from the `survey_site_data.csv` template.
Fields `siteVisitID` and `siteVisitStart` are **mandatory**.
* `targetTaxonomicScope` is a new field. Type is string, can be blank.
* `protocolName` is a new field. Type is string, can be blank.
* `protocolDescription` is a new field. Type is string, can be blank.
* Fields `samplingEffortValue` and `samplingEffortUnit` were moved to this template
from the `survey_metadata.csv` template.

For more details on the Systematic Survey Site Visit Data v2.0.0 template,
see the [Systematic Survey Site Visit Data v2.0.0 instruction manual](https://gaiaresources.github.io/abis-mapping/dev/survey_site_visit_data-v2.0.0.csv/)

# April 2024
## Templates
### Incidental Occurrence v2.0.0
#### [Schema v2.0.0](https://github.com/gaiaresources/abis-mapping/blob/main/abis_mapping/templates/incidental_occurrence_data_v2/schema.json) changes (by column order).
* `recordID` is renamed `providerRecordID` and its value is now **mandatory**
* `providerRecordIDSource` is an added field. Its type is string and its value is **mandatory**.
* `organismQuantity` is an added field. Its type is number. Can be blank.
* `organismQuantityType` is an added field. Its type is string. Can be blank.
* `occurrenceID` is renamed `ownerRecordID`. Can be blank.
* `ownerInstitutionCode` is renamed `ownerRecordIDSource`. Can be blank.
* `institutionCode` is replaced by `catalogNumberSource`. Can be blank.
* `otherCatalogNumbersSource` is an added field. Its type is string. Can be blank.

For more details on the Incidental Occurrence v2.0.0 template,
see the [Incidental Occurrence v2.0.0 instruction manual](https://gaiaresources.github.io/abis-mapping/dev/incidental_occurrence_data-v2.0.0.csv/)
