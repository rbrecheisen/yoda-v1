#!/usr/bin/env bash

export PYTHON=$HOME/.virtualenvs/flask-microservices/bin/python
export PYTEST=$HOME/.virtualenvs/flask-microservices/bin/py.test
export PYTHONPATH=$(pwd)

# ----------------------------------------------------------------------------------------------------------------------
if [ "${1}" == "setup" ]; then

    nodes="manager worker1 worker2"
    if [ "${2}" != "" ]; then
        shift; nodes="$@"
    fi

    first=1; manager=
    for node in ${nodes}; do
        vm=$(docker-machine ls | grep "virtualbox" | awk '{print $1}' | grep "${node}")
        if [ "${vm}" == "" ]; then
            docker-machine create -d virtualbox ${node}
            if [ ${first} == 1 ]; then
                manager=${node}
                first=0
            fi
        fi
    done

    if [ ${first} == 0 ]; then
        token=
        for node in ${nodes}; do
            eval $(docker-machine env ${node})
            if [ "${node}" == "${manager}" ]; then
                docker swarm init --advertise-addr $(docker-machine ip ${manager})
                token=$(docker swarm join-token --quiet worker)
            else
                docker swarm join --token ${token} $(docker-machine ip ${manager}):2377
            fi
        done
    fi

    network=$(docker network ls | awk '{print $2,$3}' | grep "my-network")
    if [ "${network}" == "" ]; then
        docker network create --driver overlay --opt secure my-network
    fi

    files=$(docker volume ls | awk '{print $2}' | grep "files")
    if [ "${files}" == "" ]; then
        docker volume create -d local --name files
    fi

    postgres=$(docker volume ls | awk '{print $2}' | grep "postgres")
    if [ "${postgres}" == "" ]; then
        docker volume create -d local --name postgres
    fi

    echo "Finished setting up environment for the following nodes:"
    echo ""
    for node in ${nodes}; do
        echo " - ${node}"
    done
    echo ""
    echo "Next steps:"
    echo ""
    echo " - ./manage.sh build"
    echo " - ./manage.sh push (optional)"
    echo ""

# ----------------------------------------------------------------------------------------------------------------------
elif [ "${1}" == "build" ]; then

    eval $(docker-machine env manager)

    docker build -t brecheisen/base:v1 ./backend
    docker build -t brecheisen/file-base:v1 ./backend/services/file/base
    docker build -t brecheisen/file:v1 ./backend/services/file
    docker build -t brecheisen/auth:v1 ./backend/services/auth
    docker build -t brecheisen/compute:v1 ./backend/services/compute
    docker build -t brecheisen/storage:v1 ./backend/services/storage

    dangling=$(docker images -qf "dangling=true")
    if [ "${dangling}" != "" ]; then
        docker rmi -f ${dangling}
    fi

# ----------------------------------------------------------------------------------------------------------------------
elif [ "${1}" == "push" ]; then

    eval $(docker-machine env manager)

    docker login --username=brecheisen

    docker push brecheisen/base:v1
    docker push brecheisen/file-base:v1
    docker push brecheisen/file:v1
    docker push brecheisen/auth:v1
    docker push brecheisen/compute:v1
    docker push brecheisen/storage:v1

# ----------------------------------------------------------------------------------------------------------------------
elif [ "${1}" == "up" ]; then

    eval $(docker-machine env manager)

    ./manage.sh down ${2}

    if [ "${2}" == "" ] || [ "${2}" == "redis" ]; then
        docker service create \
            --name redis \
            --network my-network \
            --publish 6379:6379 \
            --replicas 1 \
            redis:3.2.3
    fi

    if [ "${2}" == "" ] || [ "${2}" == "auth" ]; then
        docker service create \
            --name auth \
            --network my-network \
            --workdir /var/www/backend \
            --mount type=volume,source=postgres,target=/var/lib/postgres/data \
            --mount type=bind,source=$(pwd)/backend/lib,target=/var/www/backend/lib \
            --mount type=bind,source=$(pwd)/backend/services/auth/service,target=/var/www/backend/service \
            --mount type=bind,source=$(pwd)/backend/services/auth/run.sh,target=/var/www/backend/run.sh \
            --env AUTH_SERVICE_SETTINGS=/var/www/backend/service/auth/settings.py \
            --publish 8000:5000 \
            --replicas 1 \
            brecheisen/auth:v1
    fi

    if [ "${2}" == "" ] || [ "${2}" == "compute" ]; then

        docker service create \
            --name worker \
            --network my-network \
            --workdir /var/www/backend \
            --mount type=bind,source=$(pwd)/backend/lib,target=/var/www/backend/lib \
            --mount type=bind,source=$(pwd)/backend/services/compute/service,target=/var/www/backend/service \
            --mount type=bind,source=$(pwd)/backend/services/compute/run_worker.sh,target=/var/www/backend/run_worker.sh \
            --env COMPUTE_SERVICE_SETTINGS=/var/www/backend/service/compute/settings.py \
            --env BROKER_URL=redis://redis:6379/0 \
            --env AUTH_SERVICE_HOST=auth \
            --env AUTH_SERVICE_PORT=5000 \
            --env C_FORCE_ROOT=1 \
            --replicas 1 \
            brecheisen/compute:v1 ./run_worker.sh

        docker service create \
            --name compute \
            --network my-network \
            --workdir /var/www/backend \
            --mount type=volume,source=postgres,target=/var/lib/postgres/data \
            --mount type=bind,source=$(pwd)/backend/lib,target=/var/www/backend/lib \
            --mount type=bind,source=$(pwd)/backend/services/compute/service,target=/var/www/backend/service \
            --mount type=bind,source=$(pwd)/backend/services/compute/run.sh,target=/var/www/backend/run.sh \
            --env COMPUTE_SERVICE_SETTINGS=/var/www/backend/service/compute/settings.py \
            --env BROKER_URL=redis://redis:6379/0 \
            --env AUTH_SERVICE_HOST=auth \
            --env AUTH_SERVICE_PORT=5000 \
            --publish 8001:5001 \
            --replicas 1 \
            brecheisen/compute:v1
    fi

    if [ "${2}" == "" ] || [ "${2}" == "storage" ]; then
        docker service create \
            --name storage \
            --network my-network \
            --workdir /var/www/backend \
            --mount type=volume,source=postgres,target=/var/lib/postgres/data \
            --mount type=bind,source=$(pwd)/backend/lib,target=/var/www/backend/lib \
            --mount type=bind,source=$(pwd)/backend/services/storage/service,target=/var/www/backend/service \
            --mount type=bind,source=$(pwd)/backend/services/storage/run.sh,target=/var/www/backend/run.sh \
            --env STORAGE_SERVICE_SETTINGS=/var/www/backend/service/storage/settings.py \
            --env AUTH_SERVICE_HOST=auth \
            --env AUTH_SERVICE_PORT=5000 \
            --publish 8002:5002 \
            --replicas 1 \
            brecheisen/storage:v1
    fi

    if [ "${2}" == "" ] || [ "${2}" == "file" ]; then
        docker service create \
            --name file \
            --network my-network \
            --mount type=volume,source=files,target=/mnt/shared/files \
            --mount type=bind,source=$(pwd)/backend/services/file/nginx.conf,target=/usr/local/nginx/conf/nginx.conf \
            --mount type=bind,source=$(pwd)/backend/services/file/big-upload,target=/usr/local/nginx/modules/nginx-big-upload \
            --publish 8003:80 \
            --replicas 1 \
            brecheisen/file:v1
    fi

# ----------------------------------------------------------------------------------------------------------------------
elif [ "${1}" == "down" ]; then

    eval $(docker-machine env manager)

    wait=0

    if [ "${2}" == "" ] || [ "${2}" == "auth" ]; then
        service=$(docker service ls | awk '{print $2,$4}' | grep "brecheisen/auth:v1" | awk '{print $1}')
        if [ "${service}" != "" ]; then
            docker service rm auth
            wait=1
        fi
    fi

    if [ "${2}" == "" ] || [ "${2}" == "compute" ] || [ "${2}" == "worker" ]; then
        service=$(docker service ls | awk '{print $2,$4}' | grep "brecheisen/compute:v1" | awk '{print $1}')
        if [ "${service}" != "" ]; then
            docker service rm compute worker
            wait=1
        fi
    fi

    if [ "${2}" == "" ] || [ "${2}" == "storage" ]; then
        service=$(docker service ls | awk '{print $2,$4}' | grep "brecheisen/storage:v1" | awk '{print $1}')
        if [ "${service}" != "" ]; then
            docker service rm storage
            wait=1
        fi
    fi

    if [ "${2}" == "" ] || [ "${2}" == "file" ]; then
        service=$(docker service ls | awk '{print $2,$4}' | grep "brecheisen/file:v1" | awk '{print $1}')
        if [ "${service}" != "" ]; then
            docker service rm file
            wait=1
        fi
    fi

    if [ "${2}" == "" ] || [ "${2}" == "redis" ]; then
        service=$(docker service ls | awk '{print $2,$4}' | grep "redis:3" | awk '{print $1}')
        if [ "${service}" != "" ]; then
            docker service rm redis
            wait=1
        fi
    fi

    if [ ${wait} == 1 ]; then
        sleep 20
    fi

# ----------------------------------------------------------------------------------------------------------------------
elif [ "${1}" == "service" ] || [ "${1}" == "sv" ]; then

    eval $(docker-machine env manager)

    if [ "${2}" == "" ]; then
        docker service ls
    elif [ "${2}" == "more" ]; then
        for service in $(docker service ls | awk '{print $2}'); do
            if [ "${service}" != "NAME" ]; then
                echo "------------------------------------------------------------------------------"
                echo " ${service}"
                echo "------------------------------------------------------------------------------"
                docker service ps ${service}
                echo ""
            fi
        done
    else
        docker service ps ${2}
    fi

# ----------------------------------------------------------------------------------------------------------------------
elif [ "${1}" == "test" ]; then

    eval $(docker-machine env manager)

    export AUTH_SERVICE_HOST=$(docker-machine ip manager)
    export AUTH_SERVICE_PORT=8000
    export COMPUTE_SERVICE_HOST=$(docker-machine ip manager)
    export COMPUTE_SERVICE_PORT=8001
    export STORAGE_SERVICE_HOST=$(docker-machine ip manager)
    export STORAGE_SERVICE_PORT=8002
    export FILE_SERVICE_HOST=$(docker-machine ip manager)
    export FILE_SERVICE_PORT=8003

    ${PYTHON} ./backend/tests/run.py

    unset AUTH_SERVICE_HOST
    unset AUTH_SERVICE_PORT
    unset COMPUTE_SERVICE_HOST
    unset COMPUTE_SERVICE_PORT
    unset STORAGE_SERVICE_HOST
    unset STORAGE_SERVICE_PORT
    unset FILE_SERVICE_HOST
    unset FILE_SERVICE_PORT

# ----------------------------------------------------------------------------------------------------------------------
elif [ "${1}" == "clean" ]; then

    nodes=$(docker-machine ls | grep "virtualbox" | awk '{print $1}')
    for node in ${nodes}; do
        if [ "${node}" != "default" ]; then
            docker-machine stop ${node}; docker-machine rm -y ${node}
        fi
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
    echo "build    Builds all Docker images"
    echo "push     Pushes Docker images to Docker Hub"
    echo "up       Starts Docker services using Docker Compose"
    echo "down     Shuts down Docker services"
    echo "service  Shows list of running services or single service if <name> is given"
    echo "test     Runs python test scripts"
    echo "clean    Cleans Docker swarm cluster and deletes VMs"
    echo "logs     Shows logs for a given service (and container)"
    echo "help     Shows this help"
    echo ""

fi