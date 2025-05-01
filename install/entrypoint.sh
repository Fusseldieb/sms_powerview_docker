#!/bin/bash
set -e

/opt/powerview/powerview start --no-gui
source /opt/app/venv/bin/activate
exec python /opt/app/polling_endpoint.py