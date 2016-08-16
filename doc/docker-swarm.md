# Docker Swarm

 - https://docs.docker.com/swarm/install-w-machine
 
## VMs

 - docker-machine stop default
 - docker-machine create -d virtualbox manager
 - docker-machine create -d virtualbox agent1
 - docker-machine create -d virtualbox agent2
 
## Discovery token

 - eval $(docker-machine env manager)
 - docker run --rm swarm create
 - echo "<token>" > tokens/discovery.txt
 
## Swarm manager

 - token=$(more tokens/discovery.txt)
 - docker run -d -p 3376:3376 -t -v /var/lib/boot2docker:/certs:ro swarm manage -H 0.0.0.0:3376 --tlsverify --tlscacert=/certs/ca.pem --tlscert=/certs/server.pem --tlskey=/certs/server-key.pem token://${token}
     
## Agents

 - token=$(more tokens/discovery.txt)
 - eval $(docker-machine env agent1)
 - docker run -d swarm join --addr=$(docker-machine ip agent1):2376 token://${token} 
 - eval $(docker-machine env agent2)
 - docker run -d swarm join --addr=$(docker-machine ip agent2):2376 token://${token}
 
## Cleanup

 - docker-machine stop agent2
 - docker-machine stop agent1
 - docker-machine stop manager