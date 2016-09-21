# TODO
    
 - Implement basic UI
 
 - Give each service its own user account
 
   When the storage service checks a client token it should provide its own
   token in the header
      
 - Move database initialization out of the Python code
 
   The python code is running on multiple workers to the database initialization
   code is executed multiple times
   
 - Implement log service with correlation IDs
   
 - Implement pipeline parameter specification (and check) in settings.py
 
 - Try out S3 storage driver Docker (or use volume plugin like Flocker)
 
 - Setup R-compatible worker
 
     - We can create a worker service based on a Docker image that has R
       installed and also create a Celery queue 'R' to which we can redirect
       tasks meant for R. Use the rpy2 library.
       
 - Setup pipeline for segmenting brain images using FSL (Nipype)
 
 - Setup pipeline for extracting brain features using FreeSurfer (Nipype)

 - Use RabbitMQ as Celery broker and Redis as result backend
 
 - Test resumable uploads
 
 - Clear out postgres database and files volumes when testing (not working)

 - Figure out how to version URIs

 - Setup SSL connection

 - Setup permission checking in each service

 - Move back to Alpine Linux images
 
 - [DONE] Test Yoda with multiple uWSGI workers (now only 1 worker used)
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
