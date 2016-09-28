#!/usr/bin/env bash

eval $(docker-machine env default)

docker build -t brecheisen/storage-base:v1 ./base
docker build -t brecheisen/storage:v1 .

docker rmi -f $(docker images -qf "dangling=true")

docker run -it --rm \
    -e "STORAGE_APP_HOST=0.0.0.0" \
    -e "STORAGE_APP_PORT=5003" \
    brecheisen/storage:v1 bash