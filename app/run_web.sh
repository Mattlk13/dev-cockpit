#!/bin/bash
set -e
pip install -r /app/requirements.txt
export APP_SETTINGS=config.ProductionConfig
cd /app/cockpit / && gunicorn --reload -b 0.0.0.0:8000 app:app
