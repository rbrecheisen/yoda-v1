# import requests
# from lib.util import generate_string, service_uri
# from lib.authentication import login_header, token_header
#
#
# # --------------------------------------------------------------------------------------------------------------------
# def test_root():
#     response = requests.get(service_uri('auth'))
#     assert response.status_code == 200
#     pass
#
#
# # --------------------------------------------------------------------------------------------------------------------
# def test_request_token():
#     response = requests.post('{}/tokens'.format(service_uri('auth')), headers=login_header('ralph', 'secret'))
#     assert response.status_code == 201
#     assert response.json()['token']
#     response = requests.post('{}/tokens'.format(service_uri('auth')), headers=login_header('x', 'xxx'))
#     assert response.status_code == 403
#
#
# # --------------------------------------------------------------------------------------------------------------------
# def test_check_token():
#     response = requests.post('{}/tokens'.format(service_uri('auth')), headers=login_header('ralph', 'secret'))
#     assert response.status_code == 201
#     response = requests.post('{}/token-checks'.format(service_uri('auth')), headers=token_header(response.json()['token']))
#     assert response.status_code == 201
#     response = requests.post('{}/token-checks'.format(service_uri('auth')), headers=token_header('1234'))
#     assert response.status_code == 403
#     pass
#
#
# # --------------------------------------------------------------------------------------------------------------------
# def test_users():
#     response = requests.post('{}/tokens'.format(service_uri('auth')), headers=login_header('ralph', 'secret'))
#     assert response.status_code == 201
#     token = response.json()['token']
#     response = requests.get('{}/users'.format(service_uri('auth')), headers=token_header(token))
#     assert response.status_code == 200
#     assert len(response.json()) >= 4
#
#
# # --------------------------------------------------------------------------------------------------------------------
# def test_create_update_and_delete_user():
#     response = requests.post('{}/tokens'.format(service_uri('auth')), headers=login_header('ralph', 'secret'))
#     assert response.status_code == 201
#     token = response.json()['token']
#     data = {
#         'username': generate_string(),
#         'password': 'secret',
#         'email': '{}@yoda.com'.format(generate_string()),
#     }
#
#     # Create user
#     response = requests.post('{}/users'.format(service_uri('auth')), json=data, headers=token_header(token))
#     assert response.status_code == 201
#     user_id = response.json()['id']
#
#     # Update user and check update was successful
#     data['first_name'] = 'John'
#     response = requests.put('{}/users/{}'.format(service_uri('auth'), user_id), json=data, headers=token_header(token))
#     assert response.status_code == 200
#     response = requests.get('{}/users/{}'.format(service_uri('auth'), user_id), headers=token_header(token))
#     assert response.status_code == 200
#     assert response.json()['first_name'] == 'John'
#
#     # Delete user and check user no longer exists
#     response = requests.delete('{}/users/{}'.format(service_uri('auth'), user_id), headers=token_header(token))
#     assert response.status_code == 204
#     response = requests.get('{}/users/{}'.format(service_uri('auth'), user_id), headers=token_header(token))
#     assert response.status_code == 404
