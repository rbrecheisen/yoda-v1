import time
from celery import Celery, group, chord

celery = Celery('compute')
celery.config_from_object('service.compute.settings')


# ----------------------------------------------------------------------------------------------------------------------
@celery.task(name='classification')
def run_classification_pipeline(params):
    print('Running classification pipeline with parameters {}'.format(params))
    time.sleep(1)
    return True


# ----------------------------------------------------------------------------------------------------------------------
@celery.task(name='smoothing')
def run_smoothing(file_id, params):
    print('Running smoothing of file {} with parameters {}'.format(file_id, params))
    time.sleep(1)
    return file_id + 100


# ----------------------------------------------------------------------------------------------------------------------
@celery.task(name='ids')
def get_ids(file_ids):
    return file_ids


# ----------------------------------------------------------------------------------------------------------------------
@celery.task(name='smoothing')
def run_smoothing_pipeline(params):

    tasks = []
    for file_id in params['file_ids']:
        tasks.append(run_smoothing.s(file_id, params))
    task = chord(tasks)(get_ids.s())
    return task.apply_async()


# ----------------------------------------------------------------------------------------------------------------------
def task_status(func, task_id):
    result = func.AsyncResult(task_id)
    return result.status


# ----------------------------------------------------------------------------------------------------------------------
def task_result(func, task_id):
    result = func.AsyncResult(task_id)
    return result.result


if __name__ == '__main__':
    celery.worker_main()
