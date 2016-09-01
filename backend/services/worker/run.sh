#!/usr/bin/env bash

export PYTHONPATH=/var/www/backend:${PYTHONPATH}

queue=celery

if [ "${1}" != "" ]; then
    queue=${1}
fi

celery worker -A service.compute.worker.celery --loglevel=INFO --queue=${queue}
