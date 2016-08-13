#!/bin/bash

export PYTHON=$HOME/.virtualenvs/flask-microservices/bin/python
export PYTHONPATH=$(pwd)

if [ "${1}" == "up" ]; then

    kubectl create -f ./backend --recursive

elif [ "${1}" == "down" ]; then

    kubectl delete -f ./backend --recursive

elif [ "${1}" == "build" ]; then

    docker build -t brecheisen/base:v1 ./backend
    docker build -t brecheisen/auth:v1 ./backend/auth
    docker build -t brecheisen/compute:v1 ./backend/compute
    docker build -t brecheisen/storage:v1 ./backend/storage

fi
