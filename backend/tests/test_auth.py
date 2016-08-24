import requests
from util import uri, login_header, token_header
from lib.util import generate_string


# --------------------------------------------------------------------------------------------------------------------
def test_root():
    response = requests.get(uri('auth'))
    assert response.status_code == 200
    pass


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
    pass


# --------------------------------------------------------------------------------------------------------------------
def test_users():
    response = requests.post(uri('auth', '/tokens'), headers=login_header('ralph', 'secret'))
    assert response.status_code == 201
    token = response.json()['token']
    response = requests.get(uri('auth', '/users'), headers=token_header(token))
    assert response.status_code == 200
    assert len(response.json()) >= 4


# --------------------------------------------------------------------------------------------------------------------
def test_create_update_and_delete_user():
    response = requests.post(uri('auth', '/tokens'), headers=login_header('ralph', 'secret'))
    assert response.status_code == 201
    token = response.json()['token']
    data = {
        'username': generate_string(),
        'password': 'secret',
        'email': '{}@yoda.com'.format(generate_string()),
    }

    # Create user
    response = requests.post(uri('auth', '/users'), json=data, headers=token_header(token))
    assert response.status_code == 201
    user_id = response.json()['id']

    # Update user and check update was successful
    data['first_name'] = 'John'
    response = requests.put(uri('auth', '/users/{}'.format(user_id)), json=data, headers=token_header(token))
    assert response.status_code == 200
    response = requests.get(uri('auth', '/users/{}'.format(user_id)), headers=token_header(token))
    assert response.status_code == 200
    assert response.json()['first_name'] == 'John'

    # Delete user and check user no longer exists
    response = requests.delete(uri('auth', '/users/{}'.format(user_id)), headers=token_header(token))
    assert response.status_code == 204
    response = requests.get(uri('auth', '/users/{}'.format(user_id)), headers=token_header(token))
    assert response.status_code == 404
