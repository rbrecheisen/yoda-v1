import requests
from util import uri, login_header, token_header


def test_root():
    response = requests.get(uri('compute'))
    assert response.status_code == 200


def test_tasks():
    response = requests.post(uri('auth', '/tokens'), headers=login_header('ralph', 'secret'))
    assert response.status_code == 201
    response = requests.post(uri('compute', '/tasks'), headers=token_header(response.json()['token']))
    assert response.status_code == 201
