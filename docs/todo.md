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


# File sets and schemas

A file set contains one or more files. Users can add or remove files from
a file set. A file set can be associated with a schema that specifies a
number of rules, e.g.,

 - The minimum or maximum number of files
 - The type of files 
 - The minimum or maximum size of files
 
When a file is added to a file set, the schema checks whether the file 
complies with the rules. If not, an error is raised. Rules can be file-
level or file set-level, that is, some rules apply to individual files.
For example, the maximum size of a file or its type. Other rules apply 
to the file set itself, e.g., the maximum number of files is may contain.

class FileSetSchema(object):
    def check():
        # Checks file set rules
        pass
    def check_file(file):
        # Checks file
        pass
