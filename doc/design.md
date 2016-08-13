# Microservices with Flask and Kubernetes

This document describes how to set up a simple Flask microservices 
application and run it on a Kubernetes cluster. 

## Authentication

Handled in a centralized authentication service.

## Access control

Handled in each microservice separately because it's tightly coupled to
the specific endpoints a microservice exposes, that is, permission
checking requires knowledge about the URIs of a microservice. 