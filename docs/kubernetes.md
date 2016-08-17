# Kubernetes

## VM

 - minikube start
 - eval $(minikube docker-env)
 
## Start and test services

 - kubectl create -f ./backend/services --recursive
 - curl $(minikube service test --url)/tests
 
## Stop services

 - kubectl delete -f ./backend/services --recursive