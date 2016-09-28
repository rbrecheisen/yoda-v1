import os
import shutil

import requests
from flask import Config

from python.lib import login_header, token_header
from python.lib import uri, generate_string


# ----------------------------------------------------------------------------------------------------------------------
def get_worker_username_and_password():
    config = Config(None)
    config.from_object('service.compute.settings')
    return config['SERVICE_WORKER_USERNAME'], config['SERVICE_WORKER_PASSWORD']


# ----------------------------------------------------------------------------------------------------------------------
def get_access_token():
    username, password = get_worker_username_and_password()
    response = requests.post(uri('auth', '/tokens'), headers=login_header(username, password))
    return response.json()['token']


# ----------------------------------------------------------------------------------------------------------------------
def get_storage_id_for_file(file_id, token):
    response = requests.get(uri('storage', '/files/{}'.format(file_id)), headers=token_header(token))
    storage_id = response.json()['storage_id']
    return storage_id


# ----------------------------------------------------------------------------------------------------------------------
def create_task_dir():
    task_dir = '/tmp/workers/task-{}'.format(generate_string())
    if os.path.isdir(task_dir):
        raise RuntimeError('Directory {} already exists'.format(task_dir))
    os.makedirs(task_dir)
    return task_dir


# ----------------------------------------------------------------------------------------------------------------------
def delete_task_dir(task_dir):
    if not os.path.isdir(task_dir):
        raise RuntimeError('Directory {} does not exist'.format(task_dir))
    shutil.rmtree(task_dir)
