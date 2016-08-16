import os
import base64
import requests
import logging


def get_uri(service):
    return 'http://{}:{}'.format(
        os.getenv('{}_SERVICE_HOST'.format(service.upper())),
        os.getenv('{}_SERVICE_PORT'.format(service.upper())))


def login_header(username, password):
    return {'Authorization': 'Basic {}'.format(base64.b64encode('{}:{}'.format(username, password)))}


def token_header(token):
    return {'Authorization': 'Basic {}'.format(base64.b64encode('{}:unused'.format(token)))}


def test_auth_service():
    response = requests.get(get_uri('auth'))
    if response.status_code != 200:
        return {'test_auth_service': 'FAIL {}'.format(response.json())}
    response = requests.post('{}/tokens'.format(get_uri('auth')), headers=login_header('ralph', 'secret'))
    if response.status_code != 201:
        return {'test_auth_service': 'FAIL {}'.format(response.json())}
    token = response.json()['token']
    response = requests.post('{}/token-checks'.format(get_uri('auth')), headers=token_header(token))
    if response.status_code != 201:
        return {'test_auth_service': 'FAIL {}'.format(response.json())}
    user = response.json()['user']
    if user['username'] != 'ralph':
        return {'test_auth_service': 'FAIL username != ralph'}
    return {'test_auth_service': 'SUCCESS'}


def test_compute_service():
    response = requests.get(get_uri('compute'))
    if response.status_code != 200:
        result = 'FAIL: {}'.format(response.json())
    else:
        result = 'SUCCESS'
    return {'test_compute_service': result}


def test_storage_service():
    response = requests.get(get_uri('storage'))
    if response.status_code != 200:
        result = 'FAIL: {}'.format(response.json())
    else:
        result = 'SUCCESS'
    return {'test_storage_service': result}


def test_storage_service_file_upload():
    response = requests.post('{}/tokens'.format(get_uri('auth')), headers=login_header('ralph', 'secret'))
    if response.status_code != 201:
        result = 'FAIL: {}'.format(response.json())
    else:
        token = response.json()['token']
        response = requests.post('{}/files'.format(get_uri('storage')), headers=token_header(token))
        if response.status_code != 201:
            result = 'FAIL: {}'.format(response.json())
        else:
            result = 'SUCCESS'
    return {'test_storage_service_file_upload': result}


TESTS = [
    test_auth_service,
    test_compute_service,
    test_storage_service,
    test_storage_service_file_upload,
]
