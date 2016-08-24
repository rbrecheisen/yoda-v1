import requests
from util import uri, login_header, token_header


# --------------------------------------------------------------------------------------------------------------------
def test_root():
    response = requests.get(uri('auth'))
    assert response.status_code == 200


# --------------------------------------------------------------------------------------------------------------------
def test_request_token():
    response = requests.post(uri('auth', '/tokens'), headers=login_header('ralph', 'secret'))
    assert response.status_code == 201
    assert response.json()['token']
    response = requests.post(uri('auth', '/tokens'), headers=login_header('x', 'xxx'))
    assert response.status_code == 403


# --------------------------------------------------------------------------------------------------------------------
def test_check_token():
    response = requests.post(uri('auth', '/tokens'), headers=login_header('ralph', 'secret'))
    assert response.status_code == 201
    response = requests.post(uri('auth', '/token-checks'), headers=token_header(response.json()['token']))
    assert response.status_code == 201
    response = requests.post(uri('auth', '/token-checks'), headers=token_header('1234'))
    assert response.status_code == 403
