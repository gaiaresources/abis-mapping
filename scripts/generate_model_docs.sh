#!/bin/bash

set -ex  # (e) exit on error (x) print commands

python docs/model_json.py abis_mapping.models.schema.Schema | \
	jsonschema-markdown --no-empty-columns --no-footer - > docs/models/markdown/Schema.schema.md
