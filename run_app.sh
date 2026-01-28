#!/usr/bin/env bash

source venv/bin/activate &&
python3 app.py configs/config_test.json &&
deactivate
