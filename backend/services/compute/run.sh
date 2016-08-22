#!/usr/bin/env bash

uwsgi --http-socket 0.0.0.0:5001 --master --workers 4 --module service.compute.app:app --vacuum --die-on-term