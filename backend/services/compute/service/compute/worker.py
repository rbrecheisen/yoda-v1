import time
from celery import Celery

celery = Celery('compute')
celery.config_from_object('service.compute.settings')


# --------------------------------------------------------------------------------------------------------------------
@celery.task(name='worker.run_task')
def run_task(pipeline_id, params, duration):
    print('Running pipeline {} with parameters {} for {} seconds'.format(pipeline_id, params, duration))
    time.sleep(duration)
    return 1


# --------------------------------------------------------------------------------------------------------------------
def get_task_status(task_id):
    result = run_task.AsyncResult(task_id)
    return result.state


# --------------------------------------------------------------------------------------------------------------------
def get_task_result(task_id):
    result = run_task.AsyncResult(task_id)
    return result.result


# --------------------------------------------------------------------------------------------------------------------
def cancel_task(task_id):
    celery.control.revoke(task_id)


if __name__ == '__main__':
    celery.worker_main()
