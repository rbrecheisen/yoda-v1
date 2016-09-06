# TODO
    
 - Implement parameter specification (and check) in settings.py
 
 - Setup R-compatible worker
     - We can create a worker service based on a Docker image that has R
       installed and also create a Celery queue 'R' to which we can redirect
       tasks meant for R. Use the rpy2 library.
       
 - Setup workflow where users can upload multiple MR images and perform
   segmentation on each one. Each image should be submitted to a different
   worker for parallel processing

 - Use RabbitMQ as Celery broker and Redis as result backend
 - Test resumable uploads
 - Clear out postgres database and files volumes when testing (not working)
 - Figure out how to version URIs
 - Setup SSL connection
 - Setup logging
 - Setup permission checking in each service
 - Load files from S3 or EBS (look into volume drivers like flocker)
 - Move back to Alpine Linux images
 
 - [DONE] Refactor pipeline code
 - [DONE] Implement classifier training pipeline
 - [DONE] Handle all storage-related requests via Nginx file service
 - [DONE] Setup PostgreSQL
 - [DONE] Use response() and error_response() in each resource
 - [DONE] Setup Celery compute service with Docker swarm mode
 - [DONE] Use alpine linux images as much as possible
   - [DONE] Solve Lua errors (cannot find libgcc library)
 - [DONE] Setup Docker Engine in swarm mode   
 - [DONE] Get Nginx running with storage container in a single pod
   - [DONE] Get Nginx to connect to storage container
   - [DONE] Setup file volumes
   - [DONE] Get file upload running
     - [DONE] File upload directly to Flask service
     - [DONE] File upload via Nginx
     - [DONE] Resumable file upload via Nginx
 - [DONE] Refactored authentication to wrapper in BaseResource
 - [DONE] Moved logging to BaseResource
 - [DONE] Implement correlation IDs (put them in headers?)
 - [DONE] Add other services to compound run configuration for debugging
 - [DONE] Setup debugging facilities
