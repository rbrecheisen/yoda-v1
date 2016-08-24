# TODO

 - Figure out how to version URIs
 - Setup SSL connection
 - Setup permission checking in each service
 - Setup PostgreSQL
 - Load files from S3 or EBS (look into volume drivers like flocker)
 
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
