# October 2024
## Templates
### Incidental Occurrence v3.0.0
#### [Schema v3.0.0](https://github.com/gaiaresources/abis-mapping/blob/main/abis_mapping/templates/incidental_occurrence_data_v3/schema.json) changes (by column order).
* `conservationJurisdiction` is renamed `conservationAuthority`.
* `sensitivityCategory` and `sensitivityAuthority` are added fields. Both are type string.
They are mutually inclusive, both must be provided or both must be blank.

For more details on the Incidental Occurrence v3.0.0 template,
see the [Incidental Occurrence v3.0.0 instruction manual](https://gaiaresources.github.io/abis-mapping/dev/incidental_occurrence_data-v3.0.0.csv/)


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
