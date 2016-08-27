import time
from celery import chord, shared_task


# ----------------------------------------------------------------------------------------------------------------------
class Pipeline(object):

    def run(self, params):
        raise NotImplementedError()

    @staticmethod
    @shared_task
    def get_task_result_ids(ids):
        return ids


# ----------------------------------------------------------------------------------------------------------------------
class ClassifierTrainingPipeline(Pipeline):
    """
    Trains a classifier and returns its ID as well as some additional meta-
    information about its accuracy.
    """
    def run(self, params):
        print('Running classifier training pipeline')
        self.validate_params(params)
        # Create training task for each file ID (here only 1)
        tasks = []
        for file_id in params['file_ids']:
            tasks.append(self.train_classifier.subtask((file_id, params)))
        # Create chord task that collects the file IDs
        job = chord(header=tasks, body=self.get_task_result_ids.subtask())
        result = job.apply_async()
        # Return callback task ID
        return result.task_id

    @staticmethod
    @shared_task
    def train_classifier(file_id, params):
        print('Training classifier on file {} with parameters {}'.format(file_id, params))
        time.sleep(5)
        return file_id + 100

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
