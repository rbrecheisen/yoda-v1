#!/usr/bin/env bash

state=$(docker-machine ls | grep default | awk '{print $4}')
if [ "${state}" != "Running" ]; then
    docker-machine start default
fi

eval $(docker-machine env default)

docker run -i --rm --name redis -p 6379:6379 redis:3.0-alpine