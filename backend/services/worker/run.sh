#!/usr/bin/env bash

queue=celery

if [ "${1}" != "" ]; then
    queue=${1}
fi

celery worker -A service.compute.worker.celery --loglevel=INFO --queue=${queue}
