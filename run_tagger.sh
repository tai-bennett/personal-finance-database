#!/usr/bin/env bash

source venv/bin/activate &&
python3 manual_tagger.py configs/config_test.json 2025-10-01 2025-10-30 &&
deactivate
