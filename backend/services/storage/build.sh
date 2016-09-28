#!/usr/bin/env bash

eval $(docker-machine env manager)

docker build -t brecheisen/nginx-base:v1 ../base/nginx
docker build -t brecheisen/storage:v1 .

x=$(docker images -qf "dangling=true")
if [ "${x}" != "" ]; then
    docker rmi -f $(docker images -qf "dangling=true")
fi