#!/bin/bash

if [ "${1}" == "up" ]; then

    token=$(more tokens/discovery.txt)
    eval $(docker-machine env manager)
    docker run -d -p 3376:3376 -t -v /var/lib/boot2docker:/certs:ro swarm manage -H 0.0.0.0:3376 \
        --tlsverify \
        --tlscacert=/certs/ca.pem \
        --tlscert=/certs/server.pem \
        --tlskey=/certs/server-key.pem token://${token}
    eval $(docker-machine env agent1)
    docker run -d swarm join --addr=$(docker-machine ip agent1):2376 token://${token}
    eval $(docker-machine env agent2)
    docker run -d swarm join --addr=$(docker-machine ip agent2):2376 token://${token}
    eval $(docker-machine env manager)
    docker-machine ls

elif [ "${1}" == "down" ]; then

    eval $(docker-machine env agent2)
    docker stop $(docker ps -q); docker rm -f $(docker ps -aq);
    eval $(docker-machine env agent1)
    docker stop $(docker ps -q); docker rm -f $(docker ps -aq);
    eval $(docker-machine env manager)
    docker stop $(docker ps -q); docker rm -f $(docker ps -aq);
    eval $(docker-machine env manager)
    docker-machine ls

fi
