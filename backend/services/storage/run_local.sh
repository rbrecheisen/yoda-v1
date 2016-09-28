#!/usr/bin/env bash

eval $(docker-machine env manager)

container=$(docker ps | grep brecheisen/storage:v1 | awk '{print $1}')
if [ "${container}" != "" ]; then
    docker stop ${container}; docker rm ${container}
fi

docker run -d \
    -e "STORAGE_APP_SERVICE_HOST=192.168.99.1" \
    -e "STORAGE_APP_SERVICE_PORT=5003" \
    brecheisen/storage:v1 ./run.sh