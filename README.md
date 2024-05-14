# ABIS Templates

This repository contains a set of template files (Excel, CSV, Geopackage) used to translate tabular data into RDF 
representation conforming to the Australia Biodiversity Information Standard (ABIS)

### ABIS Links
* [GitHub](https://github.com/surroundaustralia/abis)
* [Specification Document]()

### Field Schema Documentation
To generate a csv of the underlying schema of a template `template_id`
```sh
poetry shell
python tools/fields.py <template_id> [-o] <output_file>
```
where `output_file` (optional) corresponds to a location to store the resulting csv. Default output is standard out 
if no `output_file` argument provided.
