#!/bin/bash

export PYTHON=$HOME/.virtualenvs/flask-microservices/bin/python
export PYTHONPATH=$(pwd)

if [ "${1}" == "up" ]; then

    kubectl create -f ./backend --recursive

elif [ "${1}" == "down" ]; then

    kubectl delete -f ./backend --recursive

elif [ "${1}" == "restart" ]; then

    ./manage.sh down
    ./manage.sh build
    ./manage.sh up

elif [ "${1}" == "build" ]; then

    docker build -t brecheisen/base:v1 ./backend
    docker build -t brecheisen/auth:v1 ./backend/auth
    docker build -t brecheisen/compute:v1 ./backend/compute
    docker build -t brecheisen/storage:v1 ./backend/storage
    docker build -t brecheisen/test:v1 ./backend/test

elif [ "${1}" == "update" ]; then

    kubectl delete -f ./backend/${2}
    docker build -t brecheisen/${2}:v1 ./backend/${2}
    kubectl create -f ./backend/${2}

elif [ "${1}" == "logs" ]; then

    SERVICE=${2}
    POD=$(kc list ps | awk '{print $1,$3}' | grep "Running" | awk '{print $1}' | grep ${SERVICE})
    kc logs ${POD}

elif [ "${1}" == "test" ]; then

    curl $(minikube service test --url)/tests

fi
