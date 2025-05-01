#!/bin/bash
set -e

if [ ! -f /opt/powerview/banco/banco_de_dados.yap ]; then
    cp /opt/db/database.yap /opt/powerview/banco/banco_de_dados.yap
fi

/opt/powerview/powerview start --no-gui
source /opt/app/venv/bin/activate
exec python /opt/app/polling_endpoint.py