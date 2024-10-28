# ABIS Templates

This repository contains a set of template files (Excel, CSV, Geopackage) used to translate tabular data into RDF 
representation conforming to the Australia Biodiversity Information Standard (ABIS)

## ABIS Links
* [GitHub](https://github.com/surroundaustralia/abis)
* [Specification Document]()

## Templates

A template is at its core a CSV document that is used to take tabular data from an outside source and transform
it into ABIS conformant RDF.

A template is defined through a set of key files

* A CSV file containing a single header row, each cell containing a field name (**required**).
* A `schema.json` file, containing schema definitions for each of the fields declared in the CSV (**required**).
* A `metadata.json` file, containing overall descriptions and other key values (**required**). See the detailed definition [here](docs/markdown/Schema.schema.md).
* A `mapping.py` file, containing the logic for the validation of input CSV data and performing CSV-to-RDF mapping (**required**).
* An `examples/` directory, containing example input CSV data and resulting output serialised RDF files (*optional*).
* A `validators/` directory, containing serialised RDF files defining shapes used in the template's mapping, using SHACL (*optional*).

### Schema

## Documentation

### Build the Template Instructions Site
To build all the templates' instructions, first run the script
```shell
./scripts/generate_instructions.sh
```
or using Poe the Poet
```shell
poe generate-instructions
```
This will programmatically build a markdown instructions document per Template,
from the Template source code and a Jinja2 template.
The script will place these instruction documents in `<docs/pages/>`.

Then use `mkdocs` to build the instructions' site from the `<docs/pages/>` directory.
This includes the previously generated pages plus some static pages in that directory.

To just build the site:
```shell
mkdocs build
```
Or to build and serve the site:
```shell
mkdocs serve
```

### Build the Model Markdown Documentation
To build selected models' schema documentation e.g. those used in a template's `schema.json`
file
```shell
./scripts/generate_model_docs.sh
```
or using Poe the Poet
```shell
poe generate-model-docs
```
The resulting markdown documents will be stored in `<docs/models/markdown>`

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
