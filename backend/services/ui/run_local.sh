#!/usr/bin/env bash

eval $(docker-machine env default)

docker build -t brecheisen/ui:v1 .

container=$(docker ps | grep brecheisen/ui:v1 | awk '{print $1}')
if [ "${container}" != "" ]; then
    docker stop ${container}; docker rm ${container}
fi

# Note: the storage service is also running inside a Docker container and, for this
# reason, has a different IP address than the other services!

docker run -i --rm \
    -e "AUTH_SERVICE_HOST=192.168.99.1" \
    -e "AUTH_SERVICE_PORT=5000" \
    -e "COMPUTE_SERVICE_HOST=192.168.99.1" \
    -e "COMPUTE_SERVICE_PORT=5001" \
    -e "STORAGE_SERVICE_HOST=192.168.99.101" \
    -e "STORAGE_SERVICE_PORT=5002" \
    -e "UI_SERVICE_HOST=192.168.99.1" \
    -e "UI_SERVICE_PORT=5004" \
    -p 80:80 \
    brecheisen/ui:v1 ./run.sh
