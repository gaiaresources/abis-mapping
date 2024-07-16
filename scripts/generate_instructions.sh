#!/bin/bash

python docs/instructions.py -o docs/pages/incidental_occurrence_data_v2.md incidental_occurrence_data-v2.0.0.csv
python docs/instructions.py -o docs/pages/survey_occurrence_data_v1.md survey_occurrence_data-v1.0.0.csv
python docs/instructions.py -o docs/pages/survey_metadata_v1.md survey_metadata-v1.0.0.csv
python docs/instructions.py -o docs/pages/survey_site_data_v1.md survey_site_data-v1.0.0.csv
