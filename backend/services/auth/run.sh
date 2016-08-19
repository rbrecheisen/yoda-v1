#!/usr/bin/env bash

uwsgi --http-socket 0.0.0.0:5000 --master --workers 4 --module service.auth.service:app --vacuum --die-on-term