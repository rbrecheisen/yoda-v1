from celery import Celery
from celery.result import AsyncResult
from service.compute.pipelines.base import PipelineRegistry

celery = Celery('compute')
celery.config_from_object('service.compute.settings')


# ----------------------------------------------------------------------------------------------------------------------
@celery.task(name='pipeline')
def run_pipeline(pipeline_id, params):

    # Use pipeline ID to lookup the corresponding pipeline specification in the
    # database. This specification will also contain a module/class name so we
    # can instantiate the pipeline.
    registry = PipelineRegistry()

    pipeline = registry.get(pipeline_id=pipeline_id)
    if pipeline is None:
        print('Pipeline {} not found'.format(pipeline_id))
        return None

    task_id = pipeline.run(params)
    return task_id


# ----------------------------------------------------------------------------------------------------------------------
def task_status(task_id):
    result = AsyncResult(task_id)
    return result.status


# ----------------------------------------------------------------------------------------------------------------------
def task_result(task_id):
    result = AsyncResult(task_id)
    return result.result


if __name__ == '__main__':

    # TODO: This doesn't work, Celery can't register the tasks
    celery.autodiscover_tasks([
        'service.compute.pipelines',
        'service.compute.pipelines.statistics',
        'service.compute.pipelines.statistics.classification',
        'service.compute.pipelines.statistics.classification.training',
        'service.compute.pipelines.statistics.classification.prediction',
    ])

    celery.worker_main()
