#!/usr/bin/env bash

uwsgi --http-socket 0.0.0.0:5002 --master --workers 4 --module service.storage.service:app --vacuum --die-on-term