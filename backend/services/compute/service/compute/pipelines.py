import os
import shutil
import requests
from flask import Config
from celery import chord, shared_task
from lib.util import generate_string, service_uri
from lib.authentication import login_header, token_header

config = Config(None)
config.from_object('service.compute.settings')


# ----------------------------------------------------------------------------------------------------------------------
class Pipeline(object):

    def run(self, params):
        raise NotImplementedError()


# ----------------------------------------------------------------------------------------------------------------------
class ClassifierTrainingPipeline(Pipeline):
    """
    Trains a classifier and returns its ID as well as some additional meta-
    information about its accuracy.
    """
    def run(self, params):

        # Validate the pipeline parameters
        self.validate_params(params)

        # Create training task for each file ID (here only 1)
        tasks = []
        for file_id in params['file_ids']:
            tasks.append(self.train_classifier.subtask((file_id, params)))

        # Create chord job that trains a classifier for each file ID and at the
        # end builds a task result object containing the output results.
        job = chord(header=tasks, body=self.build_task_result.subtask())
        result = job.apply_async()

        return result.task_id

    @staticmethod
    @shared_task
    def train_classifier(file_id, params):

        # - Create /tmp folder for storing intermediate files
        # - Get access token from auth service
        # - Get file storage ID from storage service
        # - Send download request to storage service with file's storage ID (store in /tmp)
        # - Instantiate classifier and set its parameters
        # - Train classifier and test its performance using cross-validation
        # - Train classifier on all data and save it to file
        # - Upload classifier file to storage service
        # - Create task result and store any relevant data in its parameters
        # - Clean up local files

        # Create temporary folder for storing a local copy of the input file(s) as
        # well as any intermediate files that are generated by the pipeline.
        task_dir = create_task_dir()

        try:
            # Request access token from authentication service
            response = requests.post(
                '{}/tokens'.format(service_uri('auth')), headers=login_header(
                    config['WORKER_USERNAME'],
                    config['WORKER_PASSWORD']))
            token = response.json()['token']

            # Send file retrieve request to storage service providing the file ID
            # as a parameter. The response will tell which storage ID is associated
            # with the file. We can then download the file to the local /tmp folder
            response = requests.get('{}/files/{}'.format(service_uri('storage'), file_id), headers=token_header(token))
            storage_id = response.json()['storage_id']

            # Download file with storage ID to local task folder. We use the storage ID
            # also as a filename for this file.
            response = requests.get(
                '{}/downloads/{}'.format(service_uri('storage'), storage_id), headers=token_header(token))
            file_path = os.path.join(task_dir, storage_id)
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(1024*1024):
                    f.write(chunk)

        finally:
            # Even if errors occur, we should clean up the task directory
            delete_task_dir(task_dir)

        return 1

    @staticmethod
    @shared_task
    def build_task_result(file_ids):
        return file_ids

    @staticmethod
    def validate_params(params):
        assert 'file_ids' in params.keys()
        assert len(params['file_ids']) == 1
        assert params['file_ids'][0] > 0
        assert 'classifier' in params.keys()
        assert 'name' in params['classifier'].keys()
        assert params['classifier']['name'] in ['svm-lin', 'svm-rbf']


# ----------------------------------------------------------------------------------------------------------------------
class ClassificationPipeline(Pipeline):
    """
    Runs a trained classifier on one or more test observations. The classifier
    must have been trained previously via the ClassifierTrainingPipeline. This
    pipeline will have saved a classifier to disk.
    """
    def run(self, params):
        print('Running classification')
        return True


# ----------------------------------------------------------------------------------------------------------------------
def create_task_dir():
    task_dir = '/tmp/workers/task-{}'.format(generate_string())
    if os.path.isdir(task_dir):
        raise RuntimeError('Directory {} already exists'.format(task_dir))
    print('Creating directory {}'.format(task_dir))
    os.makedirs(task_dir)
    return task_dir


# ----------------------------------------------------------------------------------------------------------------------
def delete_task_dir(task_dir):
    if not os.path.isdir(task_dir):
        raise RuntimeError('Directory {} does not exist'.format(task_dir))
    print('Deleting directory {}'.format(task_dir))
    shutil.rmtree(task_dir)
