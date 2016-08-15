#!/bin/bash

export PYTHON=$HOME/.virtualenvs/flask-microservices/bin/python
export PYTHONPATH=$(pwd)

if [ "${1}" == "up" ]; then

    kubectl create -f ./backend/services --recursive

elif [ "${1}" == "down" ]; then

    kubectl delete -f ./backend/services --recursive

elif [ "${1}" == "restart" ]; then

    ./manage.sh down
    ./manage.sh build
    ./manage.sh up

elif [ "${1}" == "build" ]; then

    docker build -t brecheisen/nginx:v1 ./nginx
    docker build -t brecheisen/base:v1 ./backend
    docker build -t brecheisen/auth:v1 ./backend/services/auth
    docker build -t brecheisen/compute:v1 ./backend/services/compute
    docker build -t brecheisen/storage:v1 ./backend/services/storage
    docker build -t brecheisen/storage-nginx:v1 ./backend/services/storage/ngx
    docker build -t brecheisen/test:v1 ./backend/services/test

elif [ "${1}" == "update" ]; then

    kubectl delete -f ./backend/services/${2}
    docker build -t brecheisen/${2}:v1 ./backend/services/${2}
    kubectl create -f ./backend/services/${2}

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

fi
