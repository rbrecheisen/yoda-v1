#!/usr/bin/env bash

export PYTHON=$HOME/.virtualenvs/flask-microservices/bin/python
export PYTEST=$HOME/.virtualenvs/flask-microservices/bin/py.test
export PYTHONPATH=$(pwd)

# ----------------------------------------------------------------------------------------------------------------------
if [ "${1}" == "setup" ]; then

    vm=$(docker-machine ls | grep "virtualbox" | awk '{print $1}' | grep "manager")
    if [ "${vm}" == "" ]; then
        docker-machine create -d virtualbox manager
    fi

    vm=$(docker-machine ls | grep "virtualbox" | awk '{print $1}' | grep "worker1")
    if [ "${vm}" == "" ]; then
        docker-machine create -d virtualbox worker1
    fi

    vm=$(docker-machine ls | grep "virtualbox" | awk '{print $1}' | grep "worker2")
    if [ "${vm}" == "" ]; then
        docker-machine create -d virtualbox worker2
    fi

    eval $(docker-machine env manager)
    manager=$(docker swarm join-token --quiet manager)

    if [ "${manager}" == "" ]; then

        eval $(docker-machine env manager)
        docker swarm init --advertise-addr $(docker-machine ip manager)

        token=$(docker swarm join-token --quiet worker)

        eval $(docker-machine env worker1)
        docker swarm join --token ${token} $(docker-machine ip manager):2377

        eval $(docker-machine env worker2)
        docker swarm join --token ${token} $(docker-machine ip manager):2377
    fi

    eval $(docker-machine env manager)
    network=$(docker network ls | awk '{print $2,$3}' | grep "my-network")
    if [ "${network}" == "" ]; then
        docker network create --driver overlay --opt secure my-network
    fi

    for host in manager worker1 worker2; do

        eval $(docker-machine env ${host})

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

    eval $(docker-machine env manager)

    files=$(docker volume ls | awk '{print $2}' | grep "files")
    if [ "${files}" == "" ]; then
        docker volume create -d local --name files
    fi

    postgres=$(docker volume ls | awk '{print $2}' | grep "postgres")
    if [ "${postgres}" == "" ]; then
        docker volume create -d local --name postgres
    fi

# ----------------------------------------------------------------------------------------------------------------------
elif [ "${1}" == "up" ]; then

    eval $(docker-machine env manager)

    if [ "${2}" == "" ] || [ "${2}" == "auth" ]; then

        service=$(docker service ls | awk '{print $2,$4}' | grep "brecheisen/auth" | awk '{print $1}')
        if [ "${service}" != "" ]; then
            docker service rm auth auth-ngx
            sleep 1
        fi

        docker service create \
            --name auth \
            --network my-network \
            --workdir /var/www/backend \
            --mount type=volume,source=postgres,target=/var/lib/postgres/data \
            --publish 8000:5000 \
            --replicas 1 \
            brecheisen/auth:v1

#        sleep 3
#
#        docker service create \
#            --name auth-ngx \
#            --network my-network \
#            --mount type=volume,source=files,target=/mnt/shared/files \
#            --mount type=bind,source=$(pwd)/ngx/nginx-auth.conf,target=/usr/local/nginx/conf/nginx.conf \
#            --mount type=bind,source=$(pwd)/ngx/big-upload,target=/usr/local/nginx/modules/nginx-big-upload \
#            --publish 8000:80 \
#            --replicas 1 \
#            brecheisen/ngx:v1
    fi

    if [ "${2}" == "" ] || [ "${2}" == "compute" ]; then

        service=$(docker service ls | awk '{print $2,$4}' | grep "brecheisen/compute" | awk '{print $1}')
        if [ "${service}" != "" ]; then
            docker service rm compute compute-ngx
            sleep 1
        fi

        docker service create \
            --name compute \
            --network my-network \
            --workdir /var/www/backend \
            --mount type=volume,source=postgres,target=/var/lib/postgres/data \
            --publish 8001:5001 \
            --replicas 1 \
            brecheisen/compute:v1

#        sleep 3
#
#        docker service create \
#            --name compute-ngx \
#            --network my-network \
#            --mount type=volume,source=files,target=/mnt/shared/files \
#            --mount type=bind,source=$(pwd)/ngx/nginx-compute.conf,target=/usr/local/nginx/conf/nginx.conf \
#            --mount type=bind,source=$(pwd)/ngx/big-upload,target=/usr/local/nginx/modules/nginx-big-upload \
#            --publish 8001:80 \
#            --replicas 1 \
#            brecheisen/ngx:v1
    fi

    if [ "${2}" == "" ] || [ "${2}" == "storage" ]; then

        service=$(docker service ls | awk '{print $2,$4}' | grep "brecheisen/storage" | awk '{print $1}')
        if [ "${service}" != "" ]; then
            docker service rm storage storage-ngx
            sleep 1
        fi

        docker service create \
            --name storage \
            --network my-network \
            --workdir /var/www/backend \
            --mount type=volume,source=postgres,target=/var/lib/postgres/data \
            --replicas 1 \
            brecheisen/storage:v1
        sleep 3

        docker service create \
            --name storage-ngx \
            --network my-network \
            --mount type=volume,source=files,target=/mnt/shared/files \
            --mount type=bind,source=$(pwd)/ngx/nginx-storage.conf,target=/usr/local/nginx/conf/nginx.conf \
            --mount type=bind,source=$(pwd)/ngx/big-upload,target=/usr/local/nginx/modules/nginx-big-upload \
            --publish 8002:80 \
            --replicas 1 \
            brecheisen/ngx:v1
    fi

# ----------------------------------------------------------------------------------------------------------------------
elif [ "${1}" == "down" ]; then

    eval $(docker-machine env manager)

    service=$(docker service ls | awk '{print $2,$4}' | grep "brecheisen/storage" | awk '{print $1}')
    if [ "${service}" != "" ]; then
        docker service rm storage storage-ngx
    fi

    service=$(docker service ls | awk '{print $2,$4}' | grep "brecheisen/auth" | awk '{print $1}')
    if [ "${service}" != "" ]; then
        docker service rm auth auth-ngx
    fi

    service=$(docker service ls | awk '{print $2,$4}' | grep "brecheisen/compute" | awk '{print $1}')
    if [ "${service}" != "" ]; then
        docker service rm compute compute-ngx
    fi

# ----------------------------------------------------------------------------------------------------------------------
elif [ "${1}" == "service" ] || [ "${1}" == "sv" ]; then

    eval $(docker-machine env manager)

    if [ "${2}" == "" ]; then
        docker service ls
    elif [ "${2}" == "more" ]; then
        for service in $(docker service ls | awk '{print $2}'); do
            if [ "${service}" != "NAME" ]; then
                docker service ps ${service}
            fi
        done
    else
        docker service ps ${2}
    fi

# ----------------------------------------------------------------------------------------------------------------------
elif [ "${1}" == "test" ]; then

    eval $(docker-machine env manager)

    if [ "${2}" == "" ] || [ "${2}" == "auth" ]; then
        curl $(docker-machine ip manager):8000
        echo ""
    fi

    if [ "${2}" == "" ] || [ "${2}" == "compute" ]; then
        curl $(docker-machine ip manager):8001
        echo ""
    fi

    if [ "${2}" == "" ] || [ "${2}" == "storage" ]; then
        curl $(docker-machine ip manager):8002
        echo ""
    fi

# ----------------------------------------------------------------------------------------------------------------------
elif [ "${1}" == "clean" ]; then

    for host in manager worker1 worker2; do
        docker-machine stop ${host}; docker-machine rm -y ${host}
    done

# ----------------------------------------------------------------------------------------------------------------------
elif [ "${1}" == "logs" ]; then

    service=${2}
    eval $(docker-machine env manager)
    node=$(docker service ps ${service} | awk '{print $2,$4,$5}' | grep "${service}" | grep "Running" | awk '{print $2}')

    eval $(docker-machine env ${node})
    container=$(docker ps | awk '{print $1,$2}' | grep "${service}" | awk '{print $1}')

    docker logs ${container}

# ----------------------------------------------------------------------------------------------------------------------
elif [ "${1}" == "" ] || [ "${1}" == "help" ]; then

    echo ""
    echo "Usage: manage.sh <command>"
    echo ""
    echo "Commands:"
    echo ""
    echo "setup    Creates VMs to simulate swarm hosts and builds Docker images"
    echo "up       Starts Docker services using Docker Compose"
    echo "down     Shuts down Docker services"
    echo "service  Shows list of running services or single service if <name> is given"
    echo "test     Performs basic tests"
    echo "clean    Cleans Docker swarm cluster and deletes VMs"
    echo "logs     Shows logs for a given service (and container)"
    echo "help     Shows this help"
    echo ""

fi