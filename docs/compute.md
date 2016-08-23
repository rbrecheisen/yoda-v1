# Compute service

## API

### Overview

The basic workflow is as follows. The client starts by retrieving a list of
pipeline resources. The client selects a pipeline ID and retrieve pipeline
details including a specification of the pipeline's parameters.

### /pipelines

 - GET /pipelines
 - GET /pipelines/{}
 - PUT /pipelines/{}
 - DEL /pipelines/{}
