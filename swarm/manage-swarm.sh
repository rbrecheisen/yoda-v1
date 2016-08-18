#!/usr/bin/env bash

# ----------------------------------------------------------------------------------------------------------------------
if [ "${1}" == "setup" ]; then

    vm=$(docker-machine ls | grep "virtualbox" | awk '{print $1}' | grep "consul")
    if [ "${vm}" == "" ]; then
        docker-machine create -d virtualbox consul
    fi

    eval $(docker-machine env consul)
    consul=$(docker ps | grep "consul")
    if [ "${consul}" == "" ]; then
        docker run -d -p 8500:8500 -h consul --restart always gliderlabs/consul-server -bootstrap
    fi

    vm=$(docker-machine ls | grep "virtualbox" | awk '{print $1}' | grep "manager")
    if [ "${vm}" == "" ]; then
        docker-machine create -d virtualbox \
            --swarm \
            --swarm-master \
            --swarm-discovery="consul://$(docker-machine ip consul):8500" \
            --engine-opt="cluster-store=consul://$(docker-machine ip consul):8500" \
            --engine-opt="cluster-advertise=eth1:2376" \
            --engine-label host=manager \
            manager
    fi

    vm=$(docker-machine ls | grep "virtualbox" | awk '{print $1}' | grep "worker1")
    if [ "${vm}" == "" ]; then
        docker-machine create -d virtualbox \
            --swarm \
            --swarm-discovery="consul://$(docker-machine ip consul):8500" \
            --engine-opt="cluster-store=consul://$(docker-machine ip consul):8500" \
            --engine-opt="cluster-advertise=eth1:2376" \
            --engine-label host=worker1 \
            worker1
    fi

    vm=$(docker-machine ls | grep "virtualbox" | awk '{print $1}' | grep "worker2")
    if [ "${vm}" == "" ]; then
        docker-machine create -d virtualbox \
            --swarm \
            --swarm-discovery="consul://$(docker-machine ip consul):8500" \
            --engine-opt="cluster-store=consul://$(docker-machine ip consul):8500" \
            --engine-opt="cluster-advertise=eth1:2376" \
            --engine-label host=worker2 \
            worker2
    fi

    for host in manager worker1 worker2; do

        eval $(docker-machine env ${host})

        registrator=$(docker ps | grep "registrator")
        if [ "${registrator}" == "" ]; then
            docker run -d --name registator -h $(docker-machine ip ${host}) \
                -v /var/run/docker.sock:/tmp/docker.sock \
                gliderlabs/registrator:latest consul://$(docker-machine ip consul):8500
        fi

        docker build -t brecheisen/base:v1 ./backend
        docker build -t brecheisen/ngx-base:v1 ./ngx/base
        docker build -t brecheisen/ngx:v1 ./ngx
        docker build -t brecheisen/auth:v1 ./backend/services/auth
        docker build -t brecheisen/compute:v1 ./backend/services/compute
        docker build -t brecheisen/storage:v1 ./backend/services/storage

        dangling=$(docker images -qf "dangling=true")
        if [ "${dangling}" != "" ]; then
            docker rmi -f ${dangling}
        fi

    done

# ----------------------------------------------------------------------------------------------------------------------
elif [ "${1}" == "up" ]; then

    echo "Starting services"

    tmp=$(docker ps -a | grep "files")
    if [ "${tmp}" == "" ]; then
        docker create -v /mnt/shared/files --name files brecheisen/base:v1 /bin/true
    fi

    docker run -d --name ngx -p 80:80 \
        --volumes-from files \
        -v $(pwd)/ngx/big-upload:/usr/local/nginx/modules/nginx-big-upload \
        -v $(pwd)/ngx/nginx.conf:/usr/local/nginx/conf/nginx.conf \
        brecheisen/ngx:v1

    docker run -d --name storage -p 5002:5002 \
        -v $(pwd)/backend/services/storage:/var/www/backend \
        -v$(pwd)/backend/lib:/var/www/backend/lib \
        -w /var/www/backend \
        brecheisen/storage:v1 ./run.sh

# ----------------------------------------------------------------------------------------------------------------------
elif [ "${1}" == "down" ]; then

    echo "Shutting down services"

    container_id=$(docker ps | grep "brecheisen/ngx:v1" | awk '{print $1}')
    if [ "${container_id}" != "" ]; then
        docker stop ${container_id}; docker rm -f ${container_id}
    fi

    container_id=$(docker ps | grep "brecheisen/storage:v1" | awk '{print $1}')
    if [ "${container_id}" != "" ]; then
        docker stop ${container_id}; docker rm -f ${container_id}
    fi

# ----------------------------------------------------------------------------------------------------------------------
elif [ "${1}" == "clean" ]; then

    for host in $(docker-machine ls | awk '{print $1}'); do
        if [ "${host}" != "default" ] && [ "${host}" != "NAME" ]; then
            docker-machine stop ${host}; docker-machine rm ${host}
        fi
    done

# ----------------------------------------------------------------------------------------------------------------------
elif [ "${1}" == "" ] || [ "${1}" == "help" ]; then

    echo ""
    echo "Usage: manage.sh <command>"
    echo ""
    echo "Commands:"
    echo ""
    echo "setup  Creates VMs to simulate swarm hosts and builds Docker images"
    echo "up     Starts Docker services using Docker Compose"
    echo "down   Shuts down Docker services"
    echo "clean  Cleans Docker swarm cluster and deletes VMs"
    echo "logs   Shows logs for a given service (and container)"
    echo "help   Shows this help"
    echo ""

fi