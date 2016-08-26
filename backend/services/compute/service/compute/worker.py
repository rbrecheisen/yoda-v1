from celery import Celery
from celery.result import AsyncResult
from pipelines import ClassifierTrainingPipeline

celery = Celery('compute')
celery.config_from_object('service.compute.settings')


# ----------------------------------------------------------------------------------------------------------------------
@celery.task(name='pipeline')
def run_pipeline(pipeline_id, params):

    if pipeline_id == 1:
        pipeline = ClassifierTrainingPipeline()
        task_id = pipeline.run(params)
        return task_id
    else:
        return None


# ----------------------------------------------------------------------------------------------------------------------
def task_status(task_id):
    result = AsyncResult(task_id)
    return result.status


# ----------------------------------------------------------------------------------------------------------------------
def task_result(task_id):
    result = AsyncResult(task_id)
    return result.result


if __name__ == '__main__':
    celery.autodiscover_tasks(['pipelines'])
    celery.worker_main()
