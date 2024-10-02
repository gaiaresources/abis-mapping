#!/bin/bash

python docs/instructions.py -i -o docs/pages/incidental_occurrence_data-v2.0.0.csv.md incidental_occurrence_data-v2.0.0.csv
python docs/instructions.py -o docs/pages/survey_occurrence_data-v1.0.0.csv.md survey_occurrence_data-v1.0.0.csv
python docs/instructions.py -o docs/pages/survey_metadata-v1.0.0.csv.md survey_metadata-v1.0.0.csv
python docs/instructions.py -o docs/pages/survey_site_data-v1.0.0.csv.md survey_site_data-v1.0.0.csv
