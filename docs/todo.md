# TODO

 - Figure out where duplicate auth calls come from
 
 - Setup workflow where users can upload CSV file and train a classifier
   on it and then save the classifier for predictions
   
 - Setup workflow where users can upload multiple MR images and perform
   segmentation on each one. Each image should be submitted to a different
   worker for parallel processing
   
 - Test resumable uploads
 - Clear out postgres database and files volumes when testing (not working)
 - Figure out how to version URIs
 - Setup SSL connection
 - Setup logging
 - Setup permission checking in each service
 - Load files from S3 or EBS (look into volume drivers like flocker)
 - Move back to Alpine Linux images
 
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


# Pipelines

From the /tasks endpoint we call a Celery task 'run_pipeline' which internally
retrieves a pipeline object and has it execute. The pipeline object may start
additional sub-tasks, e.g., to process multiple MR images.