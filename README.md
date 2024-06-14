# ABIS Templates

This repository contains a set of template files (Excel, CSV, Geopackage) used to translate tabular data into RDF 
representation conforming to the Australia Biodiversity Information Standard (ABIS)

### ABIS Links
* [GitHub](https://github.com/surroundaustralia/abis)
* [Specification Document]()

### Markdown Instruction Generation
To generate incidental occurrence data instruction document, the only template currently
supported, then perform the following
```sh
poetry shell
python docs/instructions.py incidental_occurrence_data-v2.0.0.csv [-o] <output_file>
```

### Field Schema Table Generation
To generate a csv of the underlying schema of a template `template_id`
```sh
poetry shell
python docs/tables/fields.py <template_id> [-o] <output_file>
```
where `output_file` (optional) corresponds to a location to store the resulting csv.
Default output is standard out 
if no `output_file` argument provided.

### Controlled Vocabulary Table Generation
To generate a csv of the underlying controlled vocabularies corresponding  to a template 
`template_id`
```sh
poetry shell
python docs/tables/vocabs.py <template_id> [-o] <output_file>
```
where `output_file` (optional) corresponds to a location to store the resulting csv. 
Default output is standard out
if no `output_file` argument provided.
