#!/usr/bin/env bash

state=$(docker-machine ls | grep default | awk '{print $4}')
if [ "${state}" != "Running" ]; then
    docker-machine start default
fi

eval $(docker-machine env default)

docker build -t brecheisen/storage:v1 .

container=$(docker ps | grep brecheisen/storage:v1 | awk '{print $1}')
if [ "${container}" != "" ]; then
    docker stop ${container}; docker rm ${container}
fi

docker run -i --rm \
    -e "STORAGE_APP_SERVICE_HOST=192.168.99.1" \
    -e "STORAGE_APP_SERVICE_PORT=5003" \
    -p 5002:80 \
    brecheisen/storage:v1 ./run.sh