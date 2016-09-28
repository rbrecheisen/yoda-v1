#!/usr/bin/env bash

eval $(docker-machine env manager)

container=$(docker ps | grep brecheisen/ui:v1 | awk '{print $1}')
if [ "${container}" != "" ]; then
    docker stop ${container}; docker rm ${container}
fi

docker run -d \
    -e "AUTH_SERVICE_HOST=192.168.99.1" \
    -e "AUTH_SERVICE_PORT=5000" \
    -e "COMPUTE_SERVICE_HOST=192.168.99.1" \
    -e "COMPUTE_SERVICE_PORT=5001" \
    -e "STORAGE_SERVICE_HOST=192.168.99.1" \
    -e "STORAGE_SERVICE_PORT=5002" \
    -e "UI_SERVICE_HOST=192.168.99.1" \
    -e "UI_SERVICE_PORT=5004" \
    -p 80:80 \
    brecheisen/ui:v1 ./run.sh
