# TODO

 - Get Nginx running with storage container in a single pod
   - Get Nginx to connect to storage container
   - Get file upload running
   - Get file upload (simulated) running without Kubernetes
 - Setup Celery compute service
 
# DONE

 - Implement correlation IDs (put them in headers?)
 - Add other services to compound run configuration for debugging
 - Setup debugging facilities

# Directories

    - flask-microservices
        - backend
            - services
                - auth
                    - service
                        - auth
                            - service.py
                            - service_settings.py
                    - Dockerfile
                    - requirements.txt
                    - run.sh
                    - service.yaml
                - compute
                    - service
                        - compute
                            - service.py
                            - service_settings.py
                    - Dockerfile
                    - requirements.txt
                    - run.sh
                    - service.yaml
                - storage
                    - service
                        - storage
                            - service.py
                            - service_settings.py
                    - Dockerfile
                    - requirements.txt
                    - run.sh
                    - service.yaml
                - test
                    - service
                        - test
                            - service.py
                            - service_settings.py
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
