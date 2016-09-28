#!/usr/bin/env bash

eval $(docker-machine env default)

docker build -t brecheisen/ui:v1 .

docker rmi -f $(docker images -qf "dangling=true")

docker run -d \
    -e "AUTH_SERVICE_HOST=0.0.0.0" \
    -e "AUTH_SERVICE_PORT=5000" \
    -e "COMPUTE_SERVICE_HOST=0.0.0.0" \
    -e "COMPUTE_SERVICE_PORT=5001" \
    -e "STORAGE_SERVICE_HOST=0.0.0.0" \
    -e "STORAGE_SERVICE_PORT=5002" \
    -e "UI_SERVICE_HOST=0.0.0.0" \
    -e "UI_SERVICE_PORT=5004" \
    brecheisen/ui:v1 ./run.sh
