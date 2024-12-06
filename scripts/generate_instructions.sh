#!/bin/bash

set -ex  # (e) exit on error (x) print commands

# incidental
python docs/instructions.py -i -o docs/pages/incidental_occurrence_data-v3.0.0.csv.md incidental_occurrence_data-v3.0.0.csv

# survey v2
python docs/instructions.py -o docs/pages/survey_metadata-v2.0.0.csv.md survey_metadata-v2.0.0.csv
python docs/instructions.py -o docs/pages/survey_occurrence_data-v2.0.0.csv.md survey_occurrence_data-v2.0.0.csv
python docs/instructions.py -o docs/pages/survey_site_data-v2.0.0.csv.md survey_site_data-v2.0.0.csv
python docs/instructions.py -o docs/pages/survey_site_visit_data-v2.0.0.csv.md survey_site_visit_data-v2.0.0.csv
