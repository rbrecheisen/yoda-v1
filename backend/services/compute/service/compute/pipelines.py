import time
from celery import chord, shared_task
from celery.result import AsyncResult


@shared_task
def get_task_result_ids(ids):
    return ids


@shared_task
def train_classifier(file_id, params):
    print('Training classifier on file {} with parameters {}'.format(file_id, params))
    time.sleep(5)
    return file_id + 100


# ----------------------------------------------------------------------------------------------------------------------
class Pipeline(object):

    @staticmethod
    def task_status(task_id):
        return AsyncResult(task_id).status

    @staticmethod
    def task_result(task_id):
        return AsyncResult(task_id).result

    def run(self, params):
        raise NotImplementedError()


# ----------------------------------------------------------------------------------------------------------------------
class ClassifierTrainingPipeline(Pipeline):
    """
    Trains a classifier and returns its ID as well as some additional meta-
    information about its accuracy.
    """
    def run(self, params):

        print('Running classifier training pipeline')

        # Check mandatory parameters are valid and complete
        assert 'file_ids' in params.keys()
        assert len(params['file_ids']) == 1
        assert params['file_ids'][0] > 0
        assert 'classifier' in params.keys()
        assert 'name' in params['classifier'].keys()
        assert params['classifier']['name'] in ['svm-lin', 'svm-rbf']

        # Run classifier training
        tasks = []
        for file_id in params['file_ids']:
            tasks.append(train_classifier.subtask((file_id, params)))
        job = chord(header=tasks, body=get_task_result_ids.subtask())
        result = job.apply_async()

        # Return callback task ID
        print('Pipeline finished')
        return result.task_id


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
