#!/usr/bin/env bash

export PYTHON=$HOME/.virtualenvs/flask-microservices/bin/python
export PYTEST=$HOME/.virtualenvs/flask-microservices/bin/py.test
export PYTHONPATH=$(pwd)

nodes="manager worker1 worker2"

# ----------------------------------------------------------------------------------------------------------------------
if [ "${1}" == "setup" ]; then

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

    eval $(docker-machine env manager)

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

    docker build -t brecheisen/python-base:v1 ./backend/services/base/python
    docker build -t brecheisen/nginx-base:v1 ./backend/services/base/nginx
    docker build -t brecheisen/storage-app-base:v1 ./backend/services/storage-app/base
    docker build -t brecheisen/storage-app:v1 ./backend/services/storage-app
    docker build -t brecheisen/storage:v1 ./backend/services/storage
    docker build -t brecheisen/auth-base:v1 ./backend/services/auth/base
    docker build -t brecheisen/auth:v1 ./backend/services/auth
    docker build -t brecheisen/compute-base:v1 ./backend/services/compute/base
    docker build -t brecheisen/compute:v1 ./backend/services/compute
    docker build -t brecheisen/worker:v1 ./backend/services/worker
    docker build -t brecheisen/database:v1 ./backend/services/database
    docker build -t brecheisen/ui:v1 ./backend/services/ui

    dangling=$(docker images -qf "dangling=true")
    if [ "${dangling}" != "" ]; then
        docker rmi -f ${dangling}
    fi


# ----------------------------------------------------------------------------------------------------------------------
elif [ "${1}" == "push" ]; then

    eval $(docker-machine env manager)

#    docker login --username=brecheisen

    docker push brecheisen/base:v1
    docker push brecheisen/storage-app-base:v1
    docker push brecheisen/storage-app:v1
    docker push brecheisen/storage-base:v1
    docker push brecheisen/storage:v1
    docker push brecheisen/auth-base:v1
    docker push brecheisen/auth:v1
    docker push brecheisen/compute-base:v1
    docker push brecheisen/compute:v1
    docker push brecheisen/worker:v1
    docker push brecheisen/database:v1
    docker push brecheisen/ui:v1

    for node in ${nodes}; do
        if [ "${node}" != "manager" ]; then
            docker pull brecheisen/base:v1
        fi
    done

# ----------------------------------------------------------------------------------------------------------------------
elif [ "${1}" == "pull" ]; then

    for node in ${nodes}; do
    
        eval $(docker-machine env ${node})

        docker pull brecheisen/base:v1
        docker pull brecheisen/storage-app-base:v1
        docker pull brecheisen/storage-app:v1
        docker pull brecheisen/storage-base:v1
        docker pull brecheisen/storage:v1
        docker pull brecheisen/auth-base:v1
        docker pull brecheisen/auth:v1
        docker pull brecheisen/compute-base:v1
        docker pull brecheisen/compute:v1
        docker pull brecheisen/worker:v1
        docker pull brecheisen/database:v1
        docker pull brecheisen/ui:v1
    done

# ----------------------------------------------------------------------------------------------------------------------
elif [ "${1}" == "up" ]; then

    eval $(docker-machine env manager)

    ./manage.sh down ${2}

    if [ "${2}" == "" ] || [ "${2}" == "redis" ]; then
        docker service create \
            --name redis \
            --network my-network \
            --replicas 1 \
            redis:3.2.3
#            --publish 6379:6379 \
    fi

    if [ "${2}" == "" ] || [ "${2}" == "auth" ]; then
        docker service create \
            --name auth \
            --network my-network \
            --workdir /var/www/backend \
            --mount type=volume,source=postgres,target=/var/lib/postgres/data \
            --env AUTH_SERVICE_SETTINGS=/var/www/backend/service/auth/settings.py \
            --env DB_NAME=postgres \
            --env DB_USER=postgres \
            --env DB_PASS=postgres \
            --env DB_HOST=database \
            --env DB_PORT=5432 \
            --replicas 1 \
            brecheisen/auth:v1
#            --publish 5000:5000 \
    fi

    if [ "${2}" == "" ] || [ "${2}" == "worker" ]; then

        docker service create \
            --name worker \
            --network my-network \
            --workdir /var/www/backend \
            --env COMPUTE_SERVICE_SETTINGS=/var/www/backend/service/compute/settings.py \
            --env BROKER_URL=redis://redis:6379/0 \
            --env CELERY_RESULT_BACKEND=redis://redis:6379/0 \
            --env AUTH_SERVICE_HOST=auth \
            --env AUTH_SERVICE_PORT=5000 \
            --env STORAGE_SERVICE_HOST=storage \
            --env STORAGE_SERVICE_PORT=5002 \
            --env C_FORCE_ROOT=1 \
            --env DB_NAME=postgres \
            --env DB_USER=postgres \
            --env DB_PASS=postgres \
            --env DB_HOST=database \
            --env DB_PORT=5432 \
            --replicas 2 \
            brecheisen/worker:v1
    fi

    if [ "${2}" == "" ] || [ "${2}" == "compute" ]; then
        docker service create \
            --name compute \
            --network my-network \
            --workdir /var/www/backend \
            --mount type=volume,source=postgres,target=/var/lib/postgres/data \
            --env COMPUTE_SERVICE_SETTINGS=/var/www/backend/service/compute/settings.py \
            --env BROKER_URL=redis://redis:6379/0 \
            --env CELERY_RESULT_BACKEND=redis://redis:6379/0 \
            --env AUTH_SERVICE_HOST=auth \
            --env AUTH_SERVICE_PORT=5000 \
            --env DB_NAME=postgres \
            --env DB_USER=postgres \
            --env DB_PASS=postgres \
            --env DB_HOST=database \
            --env DB_PORT=5432 \
            --replicas 1 \
            brecheisen/compute:v1
#            --publish 5001:5001 \
    fi

    if [ "${2}" == "" ] || [ "${2}" == "storage-app" ]; then
        docker service create \
            --name storage-app \
            --network my-network \
            --workdir /var/www/backend \
            --mount type=volume,source=postgres,target=/var/lib/postgres/data \
            --env STORAGE_SERVICE_SETTINGS=/var/www/backend/service/storage/settings.py \
            --env AUTH_SERVICE_HOST=auth \
            --env AUTH_SERVICE_PORT=5000 \
            --env STORAGE_SERVICE_HOST=storage \
            --env STORAGE_SERVICE_PORT=5002 \
            --env DB_NAME=postgres \
            --env DB_USER=postgres \
            --env DB_PASS=postgres \
            --env DB_HOST=database \
            --env DB_PORT=5432 \
            --replicas 1 \
            brecheisen/storage-app:v1
    fi

    if [ "${2}" == "" ] || [ "${2}" == "storage" ]; then
        docker service create \
            --name storage \
            --network my-network \
            --mount type=volume,source=files,target=/mnt/shared/files \
            --replicas 1 \
            brecheisen/storage:v1
#            --publish 5002:5002 \
    fi

    if [ "${2}" == "" ] || [ "${2}" == "database" ]; then
        docker service create \
            --name database \
            --network my-network \
            --mount type=volume,source=postgres,target=/var/lib/postgres/data \
            --replicas 1 \
            brecheisen/database:v1
#            --publish 5432:5432 \
    fi

    if [ "${2}" == "" ] || [ "${2}" == "ui" ]; then
        docker service create \
            --name ui \
            --network my-network \
            --env UI_SERVICE_HOST=$(docker-machine ip manager) \
            --env UI_SERVICE_PORT=80 \
            --publish 80:80 \
            --replicas 1 \
            brecheisen/ui:v1
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

    if [ "${2}" == "" ] || [ "${2}" == "worker" ]; then
        service=$(docker service ls | awk '{print $2,$4}' | grep "brecheisen/worker:v1" | awk '{print $1}')
        if [ "${service}" != "" ]; then
            docker service rm worker
            wait=1
        fi
    fi

    if [ "${2}" == "" ] || [ "${2}" == "compute" ]; then
        service=$(docker service ls | awk '{print $2,$4}' | grep "brecheisen/compute:v1" | awk '{print $1}')
        if [ "${service}" != "" ]; then
            docker service rm compute
            wait=1
        fi
    fi

    if [ "${2}" == "" ] || [ "${2}" == "storage-app" ]; then
        service=$(docker service ls | awk '{print $2,$4}' | grep "brecheisen/storage-app:v1" | awk '{print $1}')
        if [ "${service}" != "" ]; then
            docker service rm storage-app
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

    if [ "${2}" == "" ] || [ "${2}" == "redis" ]; then
        service=$(docker service ls | awk '{print $2,$4}' | grep "redis:3" | awk '{print $1}')
        if [ "${service}" != "" ]; then
            docker service rm redis
            wait=1
        fi
    fi

    if [ "${2}" == "" ] || [ "${2}" == "database" ]; then
        service=$(docker service ls | awk '{print $2,$4}' | grep "brecheisen/database:v1" | awk '{print $1}')
        if [ "${service}" != "" ]; then
            docker service rm database
            wait=1
        fi
    fi

    if [ "${2}" == "" ] || [ "${2}" == "ui" ]; then
        service=$(docker service ls | awk '{print $2,$4}' | grep "brecheisen/ui:v1" | awk '{print $1}')
        if [ "${service}" != "" ]; then
            docker service rm ui
            wait=1
        fi
    fi

    if [ ${wait} == 1 ]; then
        sleep 10
    fi

# ----------------------------------------------------------------------------------------------------------------------
elif [ "${1}" == "restart" ]; then

    ./manage.sh down ${2}
    ./manage.sh build ${2}
    ./manage.sh push ${2}
    ./manage.sh pull ${2}
    ./manage.sh up ${2}

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

    export UI_SERVICE_HOST=$(docker-machine ip manager)
    export DATA_DIR=$HOME/download

    ${PYTHON} ./backend/tests/run.py

    unset UI_SERVICE_HOST
    unset DATA_DIR

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
    for n in ${node}; do
        node=${n}
        break
    done
    eval $(docker-machine env ${node})
    container=$(docker ps | awk '{print $1,$2}' | grep "${service}:v1" | awk '{print $1}')
    for c in ${container}; do
        echo " - ${service} - ${c} -----------------------------------------"
        docker logs ${c}
        echo ""
    done

# ----------------------------------------------------------------------------------------------------------------------
elif [ "${1}" == "ls" ]; then

    service=${2}
    eval $(docker-machine env manager)
    node=$(docker service ps ${service} | awk '{print $2,$4,$5}' | grep "${service}" | grep "Running" | awk '{print $2}')
    for n in ${node}; do
        node=${n}
        break
    done
    eval $(docker-machine env ${node})
    container=$(docker ps | awk '{print $1,$2}' | grep "${service}:v1" | awk '{print $1}')
    for c in ${container}; do
        echo " - ${service} - ${c} -----------------------------------------"
        docker exec -it ${c} ls -l ${3}
        echo ""
    done

# ----------------------------------------------------------------------------------------------------------------------
elif [ "${1}" == "bash" ]; then

    service=${2}
    eval $(docker-machine env manager)
    node=$(docker service ps ${service} | awk '{print $2,$4,$5}' | grep "${service}" | grep "Running" | awk '{print $2}')
    for n in ${node}; do
        node=${n}
        break
    done
    eval $(docker-machine env ${node})
    if [ "${service}" == "database" ]; then
        service="postgres"
    fi
    container=$(docker ps | awk '{print $1,$2}' | grep "${service}:v1" | awk '{print $1}')
    first=1
    for c in ${container}; do
        if [ ${first} == 0 ]; then
            read -n1 -r -p "Press any key to continue..."
        fi
        echo " - ${service} - ${c} -----------------------------------------"
        cmd=bash
        if [ "${service}" == "ui" ]; then
            cmd=sh
        fi
        docker exec -it ${c} ${cmd}
        echo ""
        first=0
    done

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
    echo "ls       Lists directory contents in container of given service"
    echo "bash     Opens bash shell in container of given service"
    echo "help     Shows this help"
    echo ""

fi