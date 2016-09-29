#!/usr/bin/env bash

state=$(docker-machine ls | grep default | awk '{print $4}')
if [ "${state}" != "Running" ]; then
    docker-machine start default
fi

eval $(docker-machine env default)

docker run -i --rm --name rabbitmq --hostname my-rabbitmq -p 5672:5672 rabbitmq:3.6