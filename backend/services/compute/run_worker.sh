#!/usr/bin/env bash

celery worker -A service.compute.worker.celery --loglevel=INFO --queue=celery
