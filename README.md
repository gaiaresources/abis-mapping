# ABIS Templates

This repository contains a set of template files (Excel, CSV, Geopackage) used to translate tabular data into RDF 
representation conforming to the Australia Biodiversity Information Standard (ABIS)

## ABIS Links
* [GitHub](https://github.com/surroundaustralia/abis)
* [Specification Document]()

## Documentation

### Build the Documentation Site
To build all the documentation, first run the script
```shell
$ ./scripts/generate_instructions.sh
```
This will programmatically build a markdown instructions document per Template,
from the Template source code and a Jinja2 template.
The script will place these instruction documents in `docs/pages/`.

Then use `mkdocs` to build the docs site from the `docs/pages/` directory.
This includes the previously generated pages plus some static pages in that directory.

To just build the site:
```shell
mkdocs build
```
Or to build and serve the site:
```shell
mkdocs serve
```

### Markdown Instruction Generation
To generate an instruction document, perform the following
```sh
poetry shell
python docs/instructions.py incidental_occurrence_data-v2.0.0.csv [-o] <output_file>
```
This is normally done as part of the `scripts/generate_instructions.sh` script.

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
