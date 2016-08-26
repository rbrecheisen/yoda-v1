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

### Classification pipeline

The classification pipeline allows clients to classify objects. This assumes
a previously trained classifier created using the classifier training pipeline.
When the training pipeline is finished, clients can retrieve meta information
specifying classification accuracy, training time, etc.

POST /tasks {
    'pipeline_id': 1, 
    'params': {
        'file_ids': [1],
    }
} => {
    'id': <task id>,
    'status': <task status>,
}

GET /tasks/{id} => {
    'id': <task id>,
    'status': <task status>,
    'result': <task result ID(s)>,
}

GET /task-results/{id} => {
    'id': <task result id>,
    'params': {
        'classifier_id': <classifier id>,
    }
}

POST /tasks {
    'pipeline_id': 2,
    'params': {
        'file_ids': [2],
        'classifier_id': <classifier id>,
    }
} => {
    'id': <task id>,
    'status': <task status>,
}