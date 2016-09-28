# User manual

## 1. Installation and deployment

### 1.1 Local

When developing, I prefer to use Docker as little as possible because it's hard (or practically impossible) to debug applications while their running inside a Docker container. So, the Flask applications are simply run using their internal development servers, for example,

    app.run(host='0.0.0.0', post=5000)
    
There are two services which we will keep running as Docker containers, namely, the UI service and the storage service. The UI service serves the web UI to the user, which could also be done with Flask directly. However, it also serves as a gateway to the other services. We're normally using Nginx's URI rewrite functionality for that and this is hard to simulate with Flask. So, we ARE actually going to use Nginx in our local development environment. Because we don't want to install Nginx on the local system we run it inside a Docker container. This raises an issue though. The containerized Nginx server acts like a API gateway and contains upstream blocks pointing to the other services. These services are not running on Docker, however, and it's not entirely trivial to connect to a server that's running outside of the container, or even outside the Docker VM. 

Ref: http://stackoverflow.com/questions/34458455/allow-a-container-running-via-docker-machine-to-connect-with-mysql-or-xdebug-por

### 1.2 Docker Swarm in test

### 1.3 Docker Swarm in production