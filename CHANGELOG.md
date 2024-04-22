
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
* `otherCatalogNumbers` was previously of type list, it is now a string. Can be blank.

For details on the schema, check the [Incidental Occurrence v2.0.0 instruction manual](https://raw.githubusercontent.com/gaiaresources/abis-mapping/main/abis_mapping/templates/incidental_occurrence_data_v2/instructions.pdf)

