#!/usr/bin/env bash

uwsgi --http-socket 0.0.0.0:5003 --master --workers 1 --module service.test.service:app --vacuum --die-on-term