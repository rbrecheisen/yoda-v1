#!/bin/bash

export PYTHON=$HOME/.virtualenvs/flask-microservices/bin/python
export PYTHONPATH=$(pwd)

if [ "${1}" == "up" ]; then

    kc create -f ./backend/services --recursive

elif [ "${1}" == "down" ]; then

    kc delete -f ./backend/services --recursive

elif [ "${1}" == "restart" ]; then

    ./manage.sh down
    ./manage.sh build
    ./manage.sh up

elif [ "${1}" == "list" ]; then

    kc list ${2}

elif [ "${1}" == "build" ]; then

    docker build -t brecheisen/base:v1 ./backend
    docker build -t brecheisen/ngx-base:v1 ./ngx/base
    docker build -t brecheisen/ngx:v1 ./ngx
    docker build -t brecheisen/auth:v1 ./backend/services/auth
    docker build -t brecheisen/compute:v1 ./backend/services/compute
    docker build -t brecheisen/storage:v1 ./backend/services/storage
    docker build -t brecheisen/test:v1 ./backend/services/test

    dangling=$(docker images -qf "dangling=true")
    if [ "${dangling}" != "" ]; then
        docker rmi -f ${dangling}
    fi

elif [ "${1}" == "update" ]; then

    kc delete -f ./backend/services/${2}
    docker build -t brecheisen/${2}:v1 ./backend/services/${2}
    kc create -f ./backend/services/${2}

    kc delete -f ./backend/services/test
    docker build -t brecheisen/test:v1 ./backend/services/test
    kc create -f ./backend/services/test

elif [ "${1}" == "describe" ]; then

    SERVICE=${2}
    POD=$(kc list ps | awk '{print $1,$3}' | grep "Running" | awk '{print $1}' | grep ${SERVICE})
    kc describe pod ${POD}

elif [ "${1}" == "logs" ]; then

    SERVICE=${2}
    CONTAINER=${3}
    POD=$(kc list ps | awk '{print $1,$3}' | grep "Running" | awk '{print $1}' | grep ${SERVICE})
    if [ "${CONTAINER}" != "" ]; then
        kc logs ${POD} -c ${CONTAINER}
    else
        kc logs ${POD}
    fi

elif [ "${1}" == "exec" ]; then

    SERVICE=${2}
    CONTAINER_ID=$(docker ps | awk '{print $1,$2}' | grep "brecheisen/${SERVICE}" | awk '{print $1}')
    docker exec -it ${CONTAINER_ID} bash

elif [ "${1}" == "test" ]; then

    curl $(minikube service test --url)/tests

elif [ "${1}" == "clean" ]; then

    docker stop $(docker ps -q)
    docker rm -f $(docker ps -aq)
    docker rmi -f $(docker images -q)

fi
