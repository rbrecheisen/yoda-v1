#!/usr/bin/env bash

# ----------------------------------------------------------------------------------------------------------------------
if [ "${1}" == "setup" ]; then

    vm=$(docker-machine ls | grep "virtualbox" | awk '{print $1}' | grep "keystore")
    if [ "${vm}" == "" ]; then
        echo "creating keystore host"
        docker-machine create -d virtualbox --virtualbox-memory "2000" --engine-opt="label=com.function=consul" keystore
    fi

    eval $(docker-machine env keystore)

    keystore=$(docker ps | grep "progrium/consul")
    if [ "${keystore}" == "" ]; then
        echo "running keystore"
        docker run --restart=unless-stopped -d -p 8500:8500 -h consul --restart always progrium/consul -server -bootstrap
    fi

    vm=$(docker-machine ls | grep "virtualbox" | awk '{print $1}' | grep "manager")
    if [ "${vm}" == "" ]; then
        echo "creating manager host"
        docker-machine create -d virtualbox --virtualbox-memory "2000" \
            --engine-opt="label=com.function=manager" \
            --engine-opt="cluster-store=consul://$(docker-machine ip keystore):8500" \
            --engine-opt="cluster-advertise=eth1:2376" manager
    fi

    eval $(docker-machine env manager)

    manager=$(docker ps | awk '{print $2}' | grep "swarm")
    if [ "${manager}" == "" ]; then
        echo "running manager"
        docker run --restart=unless-stopped -d -p 3376:2375 -v /var/lib/boot2docker:/certs:ro \
            swarm manage \
                --tlscacert=/certs/ca.pem \
                --tlscert=/certs/server.pem \
                --tlskey=/certs/server-key.pem \
            consul://$(docker-machine ip keystore):8500
    fi

    echo "ListenAddr = \":8080\"" > config.toml
    echo "DockerURL = \"tcp://SWARM_MANAGER_IP:3376\"" >> config.toml
    echo "TLSCACert = \"/var/lib/boot2docker/ca.pem\"" >> config.toml
    echo "TLSCert = \"/var/lib/boot2docker/server.pem\"" >> config.toml
    echo "TLSKey = \"/var/lib/boot2docker/server-key.pem\"" >> config.toml
    echo "" >> config.toml
    echo "[[Extensions]]" >> config.toml
    echo "Name = \"nginx\"" >> config.toml
    echo "ConfigPath = \"/etc/conf/nginx.conf\"" >> config.toml
    echo "PidPath = \"/etc/conf/nginx.pid\"" >> config.toml
    echo "MaxConn = 1024" >> config.toml
    echo "Port = 80" >> config.toml

    vm=$(docker-machine ls | grep "virtualbox" | awk '{print $1}' | grep "lb")
    if [ "${vm}" == "" ]; then
        echo "creating lb host"
        docker-machine create -d virtualbox --virtualbox-memory "2000" \
            --engine-opt="label=com.function=interlock" lb
    fi

    eval $(docker-machine env lb)

    lb=$(docker ps | grep "ehazlett/interlock")
    if [ "${lb}" == "" ]; then
        echo "running load balancer"
        docker run -P -d -ti \
            -v nginx:/etc/conf \
            -v /var/lib/boot2docker:/var/lib/boot2docker:ro \
            -v /var/run/docker.sock:/var/run/docker.sock \
            -v $(pwd)/config.toml:/etc/config.toml \
            --name interlock ehazlett/interlock:1.0.1 -D run -c /etc/config.toml
    fi

    eval $(docker-machine env lb)

    nginx=$(docker ps | awk '{print $2}' | grep "nginx")
    if [ "${nginx}" == "" ]; then
        echo "running nginx"
        # TODO: nginx.conf is missing!!!!!!
        docker run -d -ti -p 80:80 \
            --label=interlock.ext.name=nginx \
            --link=interlock:interlock \
            -v nginx:/etc/conf \
            --name nginx \
            nginx nginx -g "daemon off;" -c /etc/conf/nginx.conf
        docker ps -a
    fi

    rm -f config.toml
fi