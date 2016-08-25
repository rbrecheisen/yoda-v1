import time
from celery import Celery

celery = Celery('compute')
celery.config_from_object('service.compute.settings')


# ----------------------------------------------------------------------------------------------------------------------
@celery.task(name='classification')
def run_classification(params):
    print('Running classification pipeline with parameters {}'.format(params))
    time.sleep(1)
    return True


# ----------------------------------------------------------------------------------------------------------------------
@celery.task(name='smoothing-single')
def run_smoothing_single(file_id):
    print('Running smoothing of file {}'.format(file_id))
    time.sleep(1)
    return file_id + 100


# ----------------------------------------------------------------------------------------------------------------------
@celery.task(name='smoothing')
def run_smoothing(params):

    print('Running smoothing with parameters {}'.format(params))
    task_ids = []
    for file_id in params['file_ids']:
        result = run_smoothing_single.apply_async((file_id,), queue='subtasks')
        task_ids.append(result.task_id)

    print('Waiting for smoothing to finish')
    while True:
        finished = True
        for task_id in task_ids:
            status = run_smoothing_single.AsyncResult(task_id).status
            if status != 'SUCCESS':
                finished = False
                break
        if finished:
            break
        time.sleep(2)

    print('Finished smoothing')
    return True


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
