from celery import Celery

celery = Celery('compute')
celery.config_from_object('service.compute.settings')


@celery.task
def run_task():
    print('Executing task....')


if __name__ == '__main__':
    celery.worker_main()
