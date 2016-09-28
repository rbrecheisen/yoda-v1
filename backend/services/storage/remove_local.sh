#!/usr/bin/env bash

eval $(docker-machine env default)

container=$(docker ps | grep brecheisen/storage:v1 | awk '{print $1}')
if [ "${container}" != "" ]; then
    echo "Stopping container ${container}..."
    docker stop ${container}
fi