import os
from celery import Celery

celery = Celery('compute')
celery.config_from_object('service.compute.settings')
celery.conf['BROKER_URL'] = os.getenv('BROKER_URL', 'redis://localhost:6379/0')


@celery.task(name='worker.run_task')
def run_task():
    print('Executing task....')


if __name__ == '__main__':
    celery.worker_main()
