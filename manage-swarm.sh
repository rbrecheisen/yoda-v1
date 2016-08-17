#!/bin/bash

if [ "${1}" == "up" ]; then

    # Figure out if default machine is running. If it is, stop it
    running=$(docker-machine ls | grep "virtualbox" | awk '{print $1,$4}' | grep "default" | awk '{print $2}' | grep "Running")
    if [ "${running}" != "" ]; then
        echo "Stopping host (VM) default"
        docker-machine stop default
    fi

    # Create VMs for manager and workers
    vm=$(docker-machine ls | grep "virtualbox" | awk '{print $1}' | grep "manager")
    if [ "${vm}" == "" ]; then
        echo "Creating host manager"
        docker-machine create -d virtualbox manager
    fi

    vm=$(docker-machine ls | grep "virtualbox" | awk '{print $1}' | grep "worker1")
    if [ "${vm}" == "" ]; then
        echo "Creating host worker1"
        docker-machine create -d virtualbox worker1
    fi

    vm=$(docker-machine ls | grep "virtualbox" | awk '{print $1}' | grep "worker2")
    if [ "${vm}" == "" ]; then
        echo "Creating host worker2"
        docker-machine create -d virtualbox worker2
    fi

    # Figure out if swarm nodes already exist. We do this by asking for the
    # manager node's join token. If the manager node is not part of the swarm
    # yet, this will print an error and result in an empty variable.
    eval $(docker-machine env manager)
    manager=$(docker swarm join-token --quiet manager)

    # Initialize swarm on manager node
    if [ "${manager}" == "" ]; then
        echo "Creating node manager"
        eval $(docker-machine env manager)
        docker swarm init --advertise-addr $(docker-machine ip manager)
    fi

    # Get worker join token
    token=$(docker swarm join-token --quiet worker)

    # Add node worker1
    if [ "${manager}" == "" ]; then
    echo "Creating node worker1"
        eval $(docker-machine env worker1)
        docker swarm join --token ${token} $(docker-machine ip manager):2377
    fi

    # Add node worker2
    if [ "${manager}" == "" ]; then
        echo "Creating node worker2"
        eval $(docker-machine env worker2)
        docker swarm join --token ${token} $(docker-machine ip manager):2377
    fi

    # Switch to manager node and create encrypted overlay network. On older kernels
    # you may have to specify the --subnet option in order to ensure there are no
    # conflicts with existing sub nets. Here, we let Docker automatically assign
    # a sub network.
    # TODO: Figure out why the documentation says "--opt encrypted" which doesn't work....
    eval $(docker-machine env manager)
    network=$(docker network ls | awk '{print $2,$3}' | grep "my-network")
    if [ "${network}" == "" ]; then
        echo "Creating network my-network"
        docker network create --driver overlay --opt secure my-network
    fi

    # Build images for each node. This is a workaround because we don't have a
    # central image registry yet
    for node in manager worker1 worker2; do

        # Switch to node's Docker environment
        eval $(docker-machine env ${node})

        # Build images (if necessary)
        docker build -t brecheisen/base:v1 ./backend
        docker build -t brecheisen/ngx-base:v1 ./ngx/base
        docker build -t brecheisen/ngx:v1 ./ngx
        docker build -t brecheisen/auth:v1 ./backend/services/auth
        docker build -t brecheisen/compute:v1 ./backend/services/compute
        docker build -t brecheisen/storage:v1 ./backend/services/storage

        # Clean up resulting dangling images
        dangling=$(docker images -qf "dangling=true")
        if [ "${dangling}" != "" ]; then
            docker rmi -f ${dangling}
        fi
    done

    # Switch to manager node
    eval $(docker-machine env manager)

    # Create 'files' volume if it does not already exists
    files=$(docker volume ls | awk '{print $2}' | grep "files")
    if [ "${files}" == "" ]; then
        docker volume create -d local --name files
    fi

    # Create 'postgres' volume
    postgres=$(docker volume ls | awk '{print $2}' | grep "postgres")
    if [ "${postgres}" == "" ]; then
        docker volume create -d local --name postgres
    fi

    # Create storage service mounting the same volume. This service must
    # be started first otherwise the Nginx service won't find it.
    service=$(docker service ls | awk '{print $2,$4}' | grep "brecheisen/storage" | awk '{print $1}')
    if [ "${service}" != "" ]; then
        docker service rm storage
    fi

    docker service create --name storage --network my-network --workdir /var/www/backend \
        --mount type=volume,source=files,target=/mnt/shared/files \
        --mount type=volume,source=postgres,target=/var/lib/postgres/data \
        --replicas 1 brecheisen/storage:v1

    # Wait a few seconds
    sleep 3

    # Create Nginx service mounting our volume. This service must be started
    # after the storage service
    service=$(docker service ls | awk '{print $2,$4}' | grep "brecheisen/ngx" | awk '{print $1}')
    if [ "${service}" != "" ]; then
        docker service rm ngx
    fi

    docker service create --name ngx --network my-network \
        --mount type=volume,source=files,target=/mnt/shared/files \
        --mount type=bind,source=$(pwd)/ngx/nginx.conf,target=/usr/local/nginx/conf/nginx.conf \
        --mount type=bind,source=$(pwd)/ngx/big-upload,target=/usr/local/nginx/modules/nginx-big-upload \
        --replicas 1 --publish 80:80 brecheisen/ngx:v1

elif [ "${1}" == "test" ]; then

    echo "Not implemented yet"

elif [ "${1}" == "clean" ]; then

    vm=$(docker-machine ls | grep "virtualbox" | awk '{print $1,$4}' | grep "manager")
    running=$(echo ${vm} | awk '{print $2}' | grep "Running")

    if [ "${vm}" != "" ]; then
        if [ "${running}" != "" ]; then
            docker-machine stop manager worker1 worker2
        fi
        docker-machine rm -y manager worker1 worker2
    fi

elif [ "${1}" == "logs" ]; then

    service=${2}
    eval $(docker-machine env manager)
    node=$(docker service ps ${service} | awk '{print $2,$4,$5}' | grep "${service}" | grep "Running" | awk '{print $2}')
    eval $(docker-machine env ${node})
    container=$(docker ps | awk '{print $1,$2}' | grep "${service}" | awk '{print $1}')
    docker logs ${container}
    eval $(docker-machine env manager)

elif [ "${1}" == "" ] || [ "${1}" == "help" ]; then

    echo ""
    echo "Usage: manage-swarm.sh <command> [<options>]"
    echo ""
    echo "Commands:"
    echo ""
    echo "up    Starts swarm cluster (sets up VM environment if necessary)"
    echo "test  Creates simple Nginx and BusyBox services and have them communicate"
    echo "clean Cleans Docker swarm cluster and deletes VMs"
    echo "logs  Shows logs for a given service (and container)"
    echo "help  Shows this help"
    echo ""
fi
