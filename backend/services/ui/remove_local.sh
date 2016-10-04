#!/usr/bin/env bash

eval $(docker-machine env default)

container=$(docker ps | grep rabbitmq:3.6 | awk '{print $1}')
if [ "${container}" != "" ]; then
    echo "Terminating rabbit-mq..."
    docker stop ${container}; docker rm ${container}
fi

container=$(docker ps | grep redis:3.0-alpine | awk '{print $1}')
if [ "${container}" != "" ]; then
    echo "Terminating redis..."
    docker stop ${container}; docker rm ${container}
fi

container=$(docker ps -a | grep busybox:1.25 | awk '{print $1}')
if [ "${container}" != "" ]; then
    echo "Terminating file storage..."
    docker rm ${container}
fi
rm -rf ./files

container=$(docker ps | grep brecheisen/storage:v1 | awk '{print $1}')
if [ "${container}" != "" ]; then
    echo "Terminating storage service..."
    docker stop ${container}; docker rm ${container}
fi

container=$(docker ps | grep brecheisen/ui:v1 | awk '{print $1}')
if [ "${container}" != "" ]; then
    echo "Terminating UI service..."
    docker stop ${container}; docker rm ${container}
fi

docker ps -a