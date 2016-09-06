from celery import Celery
from celery.result import AsyncResult
from service.compute.pipelines.base import PipelineRegistry

celery = Celery('compute')
celery.config_from_object('service.compute.settings')
tasks = []
for key in celery.conf['PIPELINES']:
    tasks.append(celery.conf['PIPELINES'][key]['tasks_module_path'])
celery.autodiscover_tasks(tasks)


# ----------------------------------------------------------------------------------------------------------------------
@celery.task(name='run_pipeline')
def run_pipeline(pipeline_name, params):

    # Use pipeline name to lookup the corresponding pipeline in the pipeline
    # registry. Each pipeline contains its own parameter specification.
    registry = PipelineRegistry()
    pipeline = registry.get(pipeline_name)
    if pipeline is None:
        print('Pipeline {} not found'.format(pipeline_name))
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
    celery.worker_main()
