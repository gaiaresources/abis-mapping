#!/usr/bin/env bash
set -e
set -x
pytest tests --cov=abis_mapping --cov-report=term-missing "${@}"