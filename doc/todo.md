# TODO

 - Implement simple web UI
 - Setup file upload testing without Kubernetes
 - Setup Celery compute service
 
 - [DONE] Implement correlation IDs (put them in headers?)
 - [DONE] Add other services to compound run configuration for debugging
 - [DONE] Setup debugging facilities
    - Provision environment variables to each service
    - Use compound run configuration

# Directories

    - flask-microservices
        - backend
            - services
                - auth
                    - auth
                        - service.py
                        - service-settings.py
                    - Dockerfile
                    - requirements.txt
                    - run.sh
                    - service.yaml
                - compute
                    - compute
                        - service.py
                        - service-settings.py
                    - Dockerfile
                    - requirements.txt
                    - run.sh
                    - service.yaml
                - storage
                    - storage
                        - service.py
                        - service-settings.py
                    - Dockerfile
                    - requirements.txt
                    - run.sh
                    - service.yaml
            - lib
                - lib
                    - http.py
                    - util.py
                - Dockerfile
                - requirements.txt                    
        - nginx
            - nginx-big-upload
            - Dockerfile
