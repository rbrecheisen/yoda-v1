#!/usr/bin/env bash

export PYTHONPATH=/var/www/backend:${PYTHONPATH}
uwsgi --http-socket 0.0.0.0:5003 --master --workers 1 --module service.storage.app:app --vacuum --die-on-term